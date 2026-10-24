using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace FindDifferences
{
    /// <summary>
    /// Spot-the-difference game with the two pictures stacked vertically (original on top).
    /// Builds its whole UI at runtime so the scene only needs this one component.
    /// </summary>
    public class FindDifferencesGame : MonoBehaviour
    {
        enum State { Menu, Playing, Won, Lost }
        enum Mode { Campaign, Survival, Test }   // Test: plays releaseLevels in order with campaign rules

        /// <summary>Outcome of a survival run (to be reported to a leaderboard later).</summary>
        public struct SurvivalResult
        {
            public int levelsCleared;
            public int differencesFound;
            public float secondsPlayed;
        }

        /// <summary>Raised when a survival run ends (time out or the player ends it).</summary>
        public event System.Action<SurvivalResult> SurvivalEnded;

        // "levels" and "startLevel" keep their names and order: Tools~/diff_select.py reads the scene YAML between them
        [Header("Campaign mode (A)")]
        [Tooltip("Levels of the campaign mode, played in order (or shuffled per round when Random Order is on).")]
        [SerializeField] FindDifferencesLevel[] levels;
        [Tooltip("Campaign position to start from (debug). Ignored when the campaign order is random.")]
        [SerializeField] int startLevel;
        [Tooltip("Shuffle the campaign levels: each level appears once per round, reshuffled for the next round.")]
        [SerializeField] bool campaignRandomOrder;

        [Header("Survival mode (B)")]
        [Tooltip("Levels of the survival mode, played in order (or shuffled per round when Random Order is on); " +
                 "after the last one the run continues from the first.")]
        [SerializeField] FindDifferencesLevel[] survivalLevels;
        [Tooltip("Shuffle the survival levels: each level appears once per round, reshuffled for the next round.")]
        [SerializeField] bool survivalRandomOrder;
        [Tooltip("Seconds on the clock when a survival run starts.")]
        [SerializeField] float survivalTime = 180f;
        [Tooltip("Seconds added to the clock for every level cleared in survival mode.")]
        [SerializeField] float survivalBonusPerLevel = 10f;

        [Header("Release levels (test mode)")]
        [Tooltip("Levels planned for the release version. Played in order by the menu's test button (campaign rules).")]
        [SerializeField] FindDifferencesLevel[] releaseLevels;
        [Tooltip("Level number range for the release list: x = first, y = last (inclusive), matched against the number in the " +
                 "level asset name (Level170 = 170). Levels are taken from the campaign list, in campaign order.")]
        [SerializeField] Vector2Int releaseRange = new Vector2Int(1, 1);
        [Tooltip("When on, Release Levels is regenerated from the campaign levels in Release Range " +
                 "(the hand-edited list is replaced). When off, Release Levels is used as edited.")]
        [SerializeField] bool releaseFromRange;

        [Header("Rules")]
        [SerializeField] float wrongTapPenalty = 5f;
        [SerializeField] int hintsPerLevel = 2;
        [Tooltip("Extra radius multiplier so taps near the edge still count.")]
        [SerializeField] float hitTolerance = 1.2f;
        [SerializeField] float wrongTapCooldown = 0.35f;

        [Header("Sprites")]
        [SerializeField] Sprite ringSprite;
        [SerializeField] Sprite crossSprite;
        [SerializeField] Sprite circleSprite;
        [SerializeField] Sprite roundBoxSprite;
        [SerializeField] Sprite starSprite;

        [Header("Audio")]
        [Tooltip("Background music, looped for the whole session (menu and levels) and never restarted, so the loop stays " +
                 "seamless. Use a clip authored as a loop and keep its Load Type off Streaming (WebGL streams through an " +
                 "HTML audio element, which leaves a gap at the loop point).")]
        [SerializeField] AudioClip bgm;
        [Range(0f, 1f)]
        [SerializeField] float bgmVolume = 0.5f;

        [Header("Debug")]
        [Tooltip("Shows a \"skip level\" button on screen (can be toggled while playing).")]
        [SerializeField] bool debugMode;

        [Header("Optional")]
        [Tooltip("Leave empty to use an OS font with CJK support.")]
        [SerializeField] Font font;

        // Layout reference resolution (portrait)
        const float RefW = 1080f, RefH = 1920f;
        const float PicW = 1000f, PicH = 666.7f;

        const string BestLevelsKey = "fd.survival.bestLevels";
        const string BestDiffsKey = "fd.survival.bestDiffs";

        static readonly Color BgColor = new Color32(255, 243, 222, 255);
        static readonly Color BarColor = new Color32(255, 170, 70, 255);
        static readonly Color FrameColor = Color.white;
        static readonly Color FoundColor = new Color32(40, 200, 90, 255);
        static readonly Color WrongColor = new Color32(235, 50, 50, 255);
        static readonly Color HintColor = new Color32(255, 220, 40, 200);
        static readonly Color DotOff = new Color32(220, 205, 185, 255);
        static readonly Color TextDark = new Color32(90, 60, 40, 255);
        static readonly Color CampaignColor = new Color32(90, 170, 240, 255);
        static readonly Color SurvivalColor = new Color32(240, 110, 80, 255);
        static readonly Color TestColor = new Color32(150, 120, 210, 255);
        static readonly Color SecondaryColor = new Color32(170, 160, 150, 255);

        // runtime
        RectTransform _canvasRect, _root;
        DifferencePicture _picTop, _picBottom;
        Text _levelText, _timerText, _hintText, _progressText, _bonusText, _restartText;
        readonly List<Image> _dots = new List<Image>();
        RectTransform _dotRow;
        GameObject _overlay, _menu;
        Text _overlayTitle, _overlaySub, _overlayButtonText, _overlayButton2Text, _menuBest;
        Image[] _overlayStars;
        Button _overlayButton, _overlayButton2;
        RectTransform _overlayCard;
        GameObject _debugSkip;

        Mode _mode;
        readonly List<FindDifferencesLevel> _order = new List<FindDifferencesLevel>(); // this round's level sequence
        int _orderPos;
        int _levelSerial;   // bumped by every StartLevel, so pending coroutines can tell they are stale
        FindDifferencesLevel _level;
        bool[] _found;
        int _foundCount;
        float _timeLeft;
        int _hintsLeft;
        float _cooldownUntil;
        State _state = State.Menu;
        Coroutine _timerFlash;
        AudioSource _bgmSource;

        // survival run
        int _levelsCleared, _diffsFound;
        float _secondsPlayed;

        public FindDifferencesLevel[] ReleaseLevels => releaseLevels;
        FindDifferencesLevel[] ModeLevels => _mode == Mode.Campaign ? levels : _mode == Mode.Test ? releaseLevels : survivalLevels;
        bool ModeRandom => _mode == Mode.Campaign ? campaignRandomOrder : _mode == Mode.Survival && survivalRandomOrder;
        bool PerLevelClock => _mode != Mode.Survival;   // campaign and test: each level has its own clock, the run ends after the last

        void OnValidate()
        {
            releaseRange.x = Mathf.Max(1, releaseRange.x);
            releaseRange.y = Mathf.Max(releaseRange.x, releaseRange.y);
            ApplyReleaseRange();
            if (_bgmSource != null) _bgmSource.volume = bgmVolume;
        }

        /// <summary>releaseFromRange: rebuild releaseLevels from the campaign levels whose asset number (LevelNNN) is in releaseRange.</summary>
        void ApplyReleaseRange()
        {
            if (!releaseFromRange || levels == null)
                return;
            var list = new List<FindDifferencesLevel>();
            foreach (var l in levels)
            {
                int n = LevelNumber(l);
                if (n >= releaseRange.x && n <= releaseRange.y)
                    list.Add(l);
            }
            releaseLevels = list.ToArray();
        }

        /// <summary>Number at the end of the level asset name ("Level170" -> 170), -1 if none.</summary>
        static int LevelNumber(FindDifferencesLevel level)
        {
            if (level == null)
                return -1;
            string name = level.name;
            int i = name.Length;
            while (i > 0 && char.IsDigit(name[i - 1]))
                i--;
            return i < name.Length && int.TryParse(name.Substring(i), out int n) ? n : -1;
        }

        void Awake()
        {
            ApplyReleaseRange();
            if (font == null)
                font = Font.CreateDynamicFontFromOSFont(new[] { "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Source Han Sans SC", "Droid Sans Fallback", "SimHei", "Arial" }, 48);
            EnsureEventSystem();
            BuildUI();
            SetupBgm();
        }

        void Start()
        {
            if (_bgmSource != null) _bgmSource.Play();
            ShowMenu();
        }

        /// <summary>One 2D looping source for the background music; mode/level changes never touch it.</summary>
        void SetupBgm()
        {
            if (bgm == null) return;
            _bgmSource = gameObject.AddComponent<AudioSource>();
            _bgmSource.clip = bgm;
            _bgmSource.loop = true;
            _bgmSource.playOnAwake = false;
            _bgmSource.spatialBlend = 0f;
            _bgmSource.priority = 0;
            _bgmSource.volume = bgmVolume;
        }

        void Update()
        {
            FitRoot();
            if (_debugSkip != null)
            {
                bool show = debugMode && _state != State.Menu;
                if (_debugSkip.activeSelf != show) _debugSkip.SetActive(show);
            }
            if (_level == null || _state != State.Playing) return;

            _timeLeft -= Time.deltaTime;
            if (_mode == Mode.Survival) _secondsPlayed += Time.deltaTime;
            if (_timeLeft <= 0f)
            {
                _timeLeft = 0f;
                UpdateTimer();
                Lose();
                return;
            }
            UpdateTimer();
        }

        // ------------------------------------------------------------------ game flow
        void ShowMenu()
        {
            StopAllCoroutines();
            _timerFlash = null;
            _timerText.rectTransform.localScale = Vector3.one;
            _bonusText.gameObject.SetActive(false);
            _state = State.Menu;
            _overlay.SetActive(false);
            _menu.SetActive(true);
            int bestLevels = PlayerPrefs.GetInt(BestLevelsKey, 0);
            _menuBest.text = bestLevels > 0
                ? $"生存模式最佳：{bestLevels} 关 · {PlayerPrefs.GetInt(BestDiffsKey, 0)} 处不同"
                : "";
            StartCoroutine(PopRoutine((RectTransform)_menu.transform.GetChild(0), 0.6f));
        }

        void StartMode(Mode mode)
        {
            _mode = mode;
            if (!HasLevels(ModeLevels))
            {
                Debug.LogError($"[FindDifferences] No levels assigned for {mode} mode.");
                return;
            }
            StopAllCoroutines();
            _timerFlash = null;
            _timerText.rectTransform.localScale = Vector3.one;
            _bonusText.gameObject.SetActive(false);
            _menu.SetActive(false);
            _restartText.text = PerLevelClock ? "重来" : "结束";
            BuildOrder(null);
            _orderPos = mode == Mode.Campaign && !ModeRandom ? Mathf.Clamp(startLevel, 0, _order.Count - 1) : 0;
            if (mode == Mode.Survival)
            {
                _timeLeft = survivalTime;
                _levelsCleared = _diffsFound = 0;
                _secondsPlayed = 0f;
            }
            StartLevel();
        }

        static bool HasLevels(FindDifferencesLevel[] list)
        {
            if (list == null) return false;
            foreach (var l in list)
                if (l != null) return true;
            return false;
        }

        /// <summary>
        /// This round's sequence: the mode's level list, shuffled when its random option is on (each level once per
        /// round). A new round never opens with the level that closed the previous one.
        /// </summary>
        void BuildOrder(FindDifferencesLevel previous)
        {
            _order.Clear();
            foreach (var l in ModeLevels)
                if (l != null) _order.Add(l);
            if (!ModeRandom) return;
            for (int i = _order.Count - 1; i > 0; i--)
            {
                int j = Random.Range(0, i + 1);
                (_order[i], _order[j]) = (_order[j], _order[i]);
            }
            if (_order.Count > 1 && _order[0] == previous)
            {
                int j = Random.Range(1, _order.Count);
                (_order[0], _order[j]) = (_order[j], _order[0]);
            }
        }

        /// <summary>Plays the level at the current position; campaign levels get a fresh clock, survival keeps its own.</summary>
        void StartLevel()
        {
            _levelSerial++;
            _level = _order[_orderPos];
            _found = new bool[_level.differences.Count];
            _foundCount = 0;
            if (PerLevelClock) _timeLeft = _level.timeLimit;
            _hintsLeft = hintsPerLevel;
            _state = State.Playing;

            _picTop.Init(_level, false);
            _picBottom.Init(_level, true);
            _overlay.SetActive(false);

            int number = PerLevelClock ? _orderPos + 1 : _levelsCleared + 1;
            string prefix = _mode == Mode.Test ? $"测试 {number}/{_order.Count}" : $"第 {number} 关";
            _levelText.text = $"{prefix}\n<size=30>{_level.levelName}</size>";
            BuildDots(_found.Length);
            UpdateProgress();
            UpdateHint();
            UpdateTimer();
        }

        /// <summary>Moves to the next position; false when the campaign has no level left (survival starts a new round).</summary>
        bool Advance()
        {
            _orderPos++;
            if (_orderPos < _order.Count) return true;
            if (PerLevelClock) return false;
            BuildOrder(_order[_order.Count - 1]);
            _orderPos = 0;
            return true;
        }

        void OnPictureTapped(DifferencePicture source, Vector2 px)
        {
            if (_state != State.Playing || Time.unscaledTime < _cooldownUntil) return;
            if (source.IsTurning) return;   // camera-orbit levels: taps are ignored while the view is changing

            int best = -1;
            float bestDist = float.MaxValue;
            for (int i = 0; i < _found.Length; i++)
            {
                var d = _level.differences[i];
                float dist = Vector2.Distance(px, source.DiffCenter(d));
                if (dist <= d.radius * hitTolerance + 10f && dist < bestDist)
                {
                    best = i;
                    bestDist = dist;
                }
            }

            if (best >= 0 && !_found[best])
            {
                Found(best);
            }
            else if (best < 0)
            {
                Wrong(source, px);
            }
            // tapping an already-found difference: ignore
        }

        void Found(int index)
        {
            _found[index] = true;
            _foundCount++;
            if (_mode == Mode.Survival) _diffsFound++;
            var d = _level.differences[index];
            _picTop.ShowFound(d, ringSprite, FoundColor);
            _picBottom.ShowFound(d, ringSprite, FoundColor);
            StartCoroutine(PopRoutine(_dots[index].rectTransform, 1.6f));
            UpdateProgress();

            if (_foundCount >= _found.Length)
                StartCoroutine(PerLevelClock ? WinRoutine() : SurvivalWinRoutine());
        }

        void Wrong(DifferencePicture source, Vector2 px)
        {
            _cooldownUntil = Time.unscaledTime + wrongTapCooldown;
            source.ShowWrong(px, crossSprite, WrongColor);
            source.Shake();
            _timeLeft = Mathf.Max(0f, _timeLeft - wrongTapPenalty);
            UpdateTimer();
            if (_timerFlash != null) StopCoroutine(_timerFlash);
            _timerFlash = StartCoroutine(FlashTimer(WrongColor));
        }

        void UseHint()
        {
            if (_state != State.Playing || _hintsLeft <= 0) return;
            for (int i = 0; i < _found.Length; i++)
            {
                if (_found[i]) continue;
                var d = _level.differences[i];
                _picTop.ShowHint(d, circleSprite, HintColor);
                _picBottom.ShowHint(d, circleSprite, HintColor);
                _hintsLeft--;
                UpdateHint();
                return;
            }
        }

        IEnumerator WinRoutine()
        {
            _state = State.Won;
            int serial = _levelSerial;
            yield return new WaitForSecondsRealtime(0.7f);
            if (_state != State.Won || serial != _levelSerial) yield break; // restarted meanwhile

            float ratio = _timeLeft / Mathf.Max(1f, _level.timeLimit);
            int stars = ratio > 0.5f ? 3 : ratio > 0.2f ? 2 : 1;
            string sub = $"用时 {Mathf.CeilToInt(_level.timeLimit - _timeLeft)} 秒";
            if (_orderPos >= _order.Count - 1)
                ShowOverlay(_mode == Mode.Test ? "测试关卡已全部完成" : "恭喜，您已通关！", sub, stars, "返回模式选择", ShowMenu);
            else
                ShowOverlay("太棒了！", sub, stars, "下一关", () => { Advance(); StartLevel(); });
        }

        /// <summary>Survival: bank the time bonus and roll straight into the next level.</summary>
        IEnumerator SurvivalWinRoutine()
        {
            _state = State.Won;
            int serial = _levelSerial;
            _levelsCleared++;
            _timeLeft += survivalBonusPerLevel;
            UpdateTimer();
            if (_timerFlash != null) StopCoroutine(_timerFlash);
            _timerFlash = StartCoroutine(FlashTimer(FoundColor));
            StartCoroutine(BonusRoutine($"+{Mathf.RoundToInt(survivalBonusPerLevel)} 秒"));
            yield return new WaitForSecondsRealtime(0.9f);
            if (_state != State.Won || serial != _levelSerial) yield break;
            Advance();
            StartLevel();
        }

        void Lose()
        {
            _state = State.Lost;
            if (PerLevelClock)
                ShowOverlay("时间到！", $"找到了 {_foundCount} / {_found.Length} 处不同", 0, "重新挑战", StartLevel,
                    "返回模式选择", ShowMenu);
            else
                EndSurvival("时间到！");
        }

        void EndSurvival(string title)
        {
            _state = State.Lost;
            var result = new SurvivalResult
            {
                levelsCleared = _levelsCleared,
                differencesFound = _diffsFound,
                secondsPlayed = _secondsPlayed,
            };
            int bestLevels = PlayerPrefs.GetInt(BestLevelsKey, 0), bestDiffs = PlayerPrefs.GetInt(BestDiffsKey, 0);
            bool record = result.levelsCleared > bestLevels ||
                          (result.levelsCleared == bestLevels && result.differencesFound > bestDiffs);
            if (record)
            {
                PlayerPrefs.SetInt(BestLevelsKey, result.levelsCleared);
                PlayerPrefs.SetInt(BestDiffsKey, result.differencesFound);
                PlayerPrefs.Save();
            }
            SurvivalEnded?.Invoke(result);

            string sub = $"通过 <b>{result.levelsCleared}</b> 关 · 找到 <b>{result.differencesFound}</b> 处不同\n" +
                         $"坚持 {Mathf.FloorToInt(result.secondsPlayed)} 秒\n" +
                         (record ? "<color=#E8A020>新纪录！</color>" : $"最佳：{bestLevels} 关 · {bestDiffs} 处不同");
            ShowOverlay(title, sub, 0, "再来一次", () => StartMode(Mode.Survival), "返回模式选择", ShowMenu);
        }

        void OnRestartButton()
        {
            if (_state == State.Menu || _level == null) return;
            if (PerLevelClock) StartLevel();
            else if (_state == State.Playing) EndSurvival("挑战结束");
        }

        // ------------------------------------------------------------------ HUD updates
        void UpdateTimer()
        {
            int t = Mathf.CeilToInt(_timeLeft);
            _timerText.text = $"{t / 60:00}:{t % 60:00}";
            if (_timerFlash == null)
                _timerText.color = _timeLeft <= 10f ? WrongColor : Color.white;
        }

        void UpdateProgress()
        {
            for (int i = 0; i < _dots.Count; i++)
            {
                _dots[i].color = _found[i] ? FoundColor : DotOff;
            }
            _progressText.text = $"{_foundCount} / {_found.Length}";
        }

        void UpdateHint()
        {
            _hintText.text = $"提示 ×{_hintsLeft}";
            _hintText.transform.parent.GetComponent<Button>().interactable = _hintsLeft > 0;
        }

        IEnumerator FlashTimer(Color color)
        {
            var rt = _timerText.rectTransform;
            for (float t = 0; t < 0.5f; t += Time.unscaledDeltaTime)
            {
                _timerText.color = Color.Lerp(color, Color.white, t / 0.5f);
                rt.localScale = Vector3.one * (1f + 0.3f * (1f - t / 0.5f));
                yield return null;
            }
            rt.localScale = Vector3.one;
            _timerFlash = null;
            UpdateTimer();
        }

        /// <summary>"+10 秒" rising from under the timer and fading out.</summary>
        IEnumerator BonusRoutine(string text)
        {
            var rt = _bonusText.rectTransform;
            _bonusText.text = text;
            _bonusText.gameObject.SetActive(true);
            var start = new Vector2(-120, -70);
            for (float t = 0; t < 0.9f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.9f;
                rt.anchoredPosition = start + new Vector2(0, 40f * k);
                var c = FoundColor;
                c.a = k < 0.6f ? 1f : 1f - (k - 0.6f) / 0.4f;
                _bonusText.color = c;
                yield return null;
            }
            _bonusText.gameObject.SetActive(false);
        }

        static IEnumerator PopRoutine(RectTransform rt, float peak)
        {
            for (float t = 0; t < 0.3f; t += Time.unscaledDeltaTime)
            {
                rt.localScale = Vector3.one * Mathf.Lerp(peak, 1f, t / 0.3f);
                yield return null;
            }
            rt.localScale = Vector3.one;
        }

        /// <summary>Result card; the second (grey) button is shown only when <paramref name="label2"/> is given.</summary>
        void ShowOverlay(string title, string sub, int stars, string buttonLabel, System.Action onClick,
            string label2 = null, System.Action onClick2 = null)
        {
            _overlay.SetActive(true);
            _overlayTitle.text = title;
            _overlaySub.text = sub;
            // without stars the text moves up into their place
            _overlaySub.rectTransform.anchoredPosition = new Vector2(0, stars > 0 ? -400 : -320);
            _overlayButtonText.text = buttonLabel;
            _overlayButton.onClick.RemoveAllListeners();
            _overlayButton.onClick.AddListener(() => onClick());
            bool two = label2 != null;
            _overlayCard.sizeDelta = new Vector2(800, two ? 800 : 680);
            _overlayButton2.gameObject.SetActive(two);
            ((RectTransform)_overlayButton.transform).anchoredPosition = new Vector2(0, two ? 230 : 120);
            if (two)
            {
                _overlayButton2Text.text = label2;
                _overlayButton2.onClick.RemoveAllListeners();
                _overlayButton2.onClick.AddListener(() => onClick2?.Invoke());
            }
            for (int i = 0; i < _overlayStars.Length; i++)
            {
                _overlayStars[i].gameObject.SetActive(stars > 0);
                _overlayStars[i].color = i < stars ? new Color32(255, 200, 40, 255) : new Color32(210, 200, 190, 255);
            }
            StartCoroutine(PopRoutine((RectTransform)_overlay.transform.GetChild(0), 0.6f));
        }

        // ------------------------------------------------------------------ UI construction
        static void EnsureEventSystem()
        {
            if (EventSystem.current != null || FindAnyObjectByType<EventSystem>() != null) return;
            var es = new GameObject("EventSystem", typeof(EventSystem));
#if ENABLE_INPUT_SYSTEM
            es.AddComponent<UnityEngine.InputSystem.UI.InputSystemUIInputModule>();
#else
            es.AddComponent<StandaloneInputModule>();
#endif
        }

        void FitRoot()
        {
            if (_root == null) return;
            Vector2 size = _canvasRect.rect.size;
            float scale = Mathf.Min(size.x / RefW, size.y / RefH);
            _root.localScale = new Vector3(scale, scale, 1f);
        }

        void BuildUI()
        {
            var canvasGo = new GameObject("FindDifferencesCanvas", typeof(RectTransform), typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
            canvasGo.transform.SetParent(transform, false);
            var canvas = canvasGo.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = 10;
            canvasGo.GetComponent<CanvasScaler>().uiScaleMode = CanvasScaler.ScaleMode.ConstantPixelSize;
            _canvasRect = (RectTransform)canvasGo.transform;

            // full screen background
            var bg = CreateImage("Background", _canvasRect, null, BgColor);
            Stretch(bg.rectTransform);
            bg.raycastTarget = false;

            // portrait root, uniformly scaled to fit the screen
            _root = CreateRect("Root", _canvasRect);
            _root.anchorMin = _root.anchorMax = _root.pivot = new Vector2(0.5f, 0.5f);
            _root.sizeDelta = new Vector2(RefW, RefH);

            BuildTopBar();

            float gap = 28f;
            float topY = -200f;
            _picTop = BuildPicture("PictureTop", topY - (PicH + 20f) / 2f, "原图");
            _picBottom = BuildPicture("PictureBottom", topY - (PicH + 20f) * 1.5f - gap, "找不同");

            BuildBottomBar();
            BuildOverlay();
            BuildMenu();
            BuildDebugSkip();
            FitRoot();
        }

        void BuildTopBar()
        {
            var bar = CreateImage("TopBar", _root, roundBoxSprite, BarColor);
            SetTop(bar.rectTransform, 1040f, 160f, -20f);

            _levelText = CreateText("Level", bar.rectTransform, "", 40, TextAnchor.MiddleLeft, Color.white);
            Place(_levelText.rectTransform, new Vector2(0, 0.5f), new Vector2(40, 0), new Vector2(360, 130), new Vector2(0, 0.5f));

            _timerText = CreateText("Timer", bar.rectTransform, "00:00", 56, TextAnchor.MiddleCenter, Color.white);
            Place(_timerText.rectTransform, new Vector2(1, 0.5f), new Vector2(-120, 0), new Vector2(220, 100), new Vector2(0.5f, 0.5f));

            // survival time bonus, floats up from under the timer (see BonusRoutine)
            _bonusText = CreateText("Bonus", bar.rectTransform, "", 44, TextAnchor.MiddleCenter, FoundColor);
            Place(_bonusText.rectTransform, new Vector2(1, 0.5f), new Vector2(-120, -70), new Vector2(220, 60), new Vector2(0.5f, 0.5f));
            _bonusText.gameObject.AddComponent<Outline>().effectColor = new Color(1f, 1f, 1f, 0.9f);
            _bonusText.gameObject.SetActive(false);

            _progressText = CreateText("Progress", bar.rectTransform, "", 40, TextAnchor.MiddleCenter, Color.white);
            Place(_progressText.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 28), new Vector2(300, 60), new Vector2(0.5f, 0.5f));

            _dotRow = CreateRect("Dots", bar.rectTransform);
            Place(_dotRow, new Vector2(0.5f, 0.5f), new Vector2(0, -32), new Vector2(380, 40), new Vector2(0.5f, 0.5f));
            var layout = _dotRow.gameObject.AddComponent<HorizontalLayoutGroup>();
            layout.spacing = 14;
            layout.childAlignment = TextAnchor.MiddleCenter;
            layout.childControlWidth = layout.childControlHeight = false;
            layout.childForceExpandWidth = layout.childForceExpandHeight = false;
        }

        void BuildDots(int count)
        {
            foreach (var d in _dots) Destroy(d.gameObject);
            _dots.Clear();
            for (int i = 0; i < count; i++)
            {
                var dot = CreateImage("Dot" + i, _dotRow, circleSprite, DotOff);
                dot.rectTransform.sizeDelta = new Vector2(34, 34);
                dot.raycastTarget = false;
                _dots.Add(dot);
            }
        }

        DifferencePicture BuildPicture(string name, float centerY, string tag)
        {
            var frame = CreateImage(name + "Frame", _root, roundBoxSprite, FrameColor);
            Place(frame.rectTransform, new Vector2(0.5f, 1f), new Vector2(0, centerY), new Vector2(PicW + 20f, PicH + 20f), new Vector2(0.5f, 0.5f));
            frame.raycastTarget = false;
            frame.gameObject.AddComponent<Shadow>().effectDistance = new Vector2(0, -6);

            var pic = CreateImage(name, frame.rectTransform, null, Color.white);
            Place(pic.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(PicW, PicH), new Vector2(0.5f, 0.5f));
            pic.gameObject.AddComponent<RectMask2D>();
            var comp = pic.gameObject.AddComponent<DifferencePicture>();
            comp.Tapped += OnPictureTapped;

            var label = CreateImage("Tag", frame.rectTransform, roundBoxSprite, new Color(0, 0, 0, 0.45f));
            Place(label.rectTransform, new Vector2(0, 0), new Vector2(22, 22), new Vector2(130, 48), new Vector2(0, 0));
            label.raycastTarget = false;
            var labelText = CreateText("Text", label.rectTransform, tag, 28, TextAnchor.MiddleCenter, Color.white);
            Stretch(labelText.rectTransform);
            return comp;
        }

        /// <summary>Debug-only button, created last so it stays above the result overlay.</summary>
        void BuildDebugSkip()
        {
            var btn = CreateButton("DebugSkipButton", _root, "跳过本关 ▶", new Color32(230, 70, 90, 235),
                new Vector2(PicW / 2f - 110f, -250f), new Vector2(220, 72), SkipLevel);
            var label = btn.GetComponentInChildren<Text>();
            label.fontSize = 32;
            _debugSkip = btn.gameObject;
            _debugSkip.SetActive(debugMode);
        }

        /// <summary>Debug: on to the next level without a result screen or time bonus (the campaign wraps around).</summary>
        void SkipLevel()
        {
            if (_state == State.Menu || _level == null) return;
            StopAllCoroutines();               // cancels a pending win screen / running UI tweens
            _timerFlash = null;
            _timerText.rectTransform.localScale = Vector3.one;
            _bonusText.gameObject.SetActive(false);
            if (!Advance())
            {
                BuildOrder(_level);
                _orderPos = 0;
            }
            StartLevel();
        }

        void BuildBottomBar()
        {
            float y = -1790f;
            var hint = CreateButton("HintButton", _root, "提示", new Color32(255, 200, 40, 255), new Vector2(-230, y), new Vector2(380, 130), UseHint);
            _hintText = hint.GetComponentInChildren<Text>();
            // campaign: restart the level; survival: end the run and show the result
            var restart = CreateButton("RestartButton", _root, "重来", new Color32(90, 170, 240, 255), new Vector2(230, y), new Vector2(380, 130),
                OnRestartButton);
            _restartText = restart.GetComponentInChildren<Text>();
        }

        void BuildOverlay()
        {
            var dim = CreateImage("Overlay", _root, null, new Color(0, 0, 0, 0.6f));
            _overlay = dim.gameObject;
            var drt = dim.rectTransform;
            drt.anchorMin = drt.anchorMax = drt.pivot = new Vector2(0.5f, 0.5f);
            drt.sizeDelta = new Vector2(RefW * 4, RefH * 4); // covers letterbox area too

            var card = CreateImage("Card", drt, roundBoxSprite, Color.white);
            Place(card.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(800, 680), new Vector2(0.5f, 0.5f));
            _overlayCard = card.rectTransform;

            _overlayTitle = CreateText("Title", card.rectTransform, "", 84, TextAnchor.MiddleCenter, TextDark);
            Place(_overlayTitle.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -110), new Vector2(760, 120), new Vector2(0.5f, 0.5f));

            _overlayStars = new Image[3];
            for (int i = 0; i < 3; i++)
            {
                var s = CreateImage("Star" + i, card.rectTransform, starSprite, Color.white);
                float size = i == 1 ? 150 : 120;
                Place(s.rectTransform, new Vector2(0.5f, 1), new Vector2((i - 1) * 160, i == 1 ? -260 : -280), new Vector2(size, size), new Vector2(0.5f, 0.5f));
                s.raycastTarget = false;
                _overlayStars[i] = s;
            }

            _overlaySub = CreateText("Sub", card.rectTransform, "", 44, TextAnchor.MiddleCenter, TextDark);
            Place(_overlaySub.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -400), new Vector2(760, 70), new Vector2(0.5f, 0.5f));

            _overlayButton = CreateButton("Button", card.rectTransform, "", FoundColor, new Vector2(0, 0), new Vector2(440, 130), null);
            var brt = (RectTransform)_overlayButton.transform;
            brt.anchorMin = brt.anchorMax = new Vector2(0.5f, 0);
            brt.anchoredPosition = new Vector2(0, 120);
            _overlayButtonText = _overlayButton.GetComponentInChildren<Text>();

            _overlayButton2 = CreateButton("Button2", card.rectTransform, "", SecondaryColor, new Vector2(0, 0), new Vector2(440, 100), null);
            var b2rt = (RectTransform)_overlayButton2.transform;
            b2rt.anchorMin = b2rt.anchorMax = new Vector2(0.5f, 0);
            b2rt.anchoredPosition = new Vector2(0, 85);
            _overlayButton2Text = _overlayButton2.GetComponentInChildren<Text>();
            _overlayButton2Text.fontSize = 40;
            _overlay.SetActive(false);
        }

        /// <summary>Mode selection shown before playing: campaign (A), survival (B) or test (release levels in order).</summary>
        void BuildMenu()
        {
            var dim = CreateImage("ModeMenu", _root, null, new Color(0, 0, 0, 0.6f));
            _menu = dim.gameObject;
            var drt = dim.rectTransform;
            drt.anchorMin = drt.anchorMax = drt.pivot = new Vector2(0.5f, 0.5f);
            drt.sizeDelta = new Vector2(RefW * 4, RefH * 4); // covers letterbox area too

            var card = CreateImage("Card", drt, roundBoxSprite, Color.white);
            Place(card.rectTransform, new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(860, 1120), new Vector2(0.5f, 0.5f));

            var title = CreateText("Title", card.rectTransform, "选择模式", 84, TextAnchor.MiddleCenter, TextDark);
            Place(title.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -110), new Vector2(800, 120), new Vector2(0.5f, 0.5f));

            float campaignTime = levels != null && levels.Length > 0 && levels[0] != null ? levels[0].timeLimit : 60f;
            MenuButton(card.rectTransform, -320, CampaignColor, "通关模式",
                $"每关限时 {Mathf.RoundToInt(campaignTime)} 秒，挑战全部关卡", () => StartMode(Mode.Campaign));
            MenuButton(card.rectTransform, -580, SurvivalColor, "生存模式",
                $"总计 {Mathf.RoundToInt(survivalTime)} 秒，每过一关 +{Mathf.RoundToInt(survivalBonusPerLevel)} 秒", () => StartMode(Mode.Survival));
            int releaseCount = 0;
            if (releaseLevels != null)
                foreach (var l in releaseLevels)
                    if (l != null) releaseCount++;
            MenuButton(card.rectTransform, -840, TestColor, "测试关卡",
                $"按顺序试玩正式版关卡（共 {releaseCount} 关）", () => StartMode(Mode.Test));

            _menuBest = CreateText("Best", card.rectTransform, "", 34, TextAnchor.MiddleCenter, TextDark);
            Place(_menuBest.rectTransform, new Vector2(0.5f, 1), new Vector2(0, -1035), new Vector2(800, 60), new Vector2(0.5f, 0.5f));
            _menu.SetActive(false);
        }

        void MenuButton(RectTransform card, float y, Color color, string label, string detail, UnityEngine.Events.UnityAction onClick)
        {
            var btn = CreateButton(label, card, $"{label}\n<size=32>{detail}</size>", color, new Vector2(0, y), new Vector2(720, 210), onClick);
            btn.GetComponentInChildren<Text>().lineSpacing = 1.2f;
        }

        // ------------------------------------------------------------------ helpers
        static RectTransform CreateRect(string name, Transform parent)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        Image CreateImage(string name, Transform parent, Sprite sprite, Color color)
        {
            var rt = CreateRect(name, parent);
            var img = rt.gameObject.AddComponent<Image>();
            img.sprite = sprite;
            img.color = color;
            if (sprite != null && sprite.border != Vector4.zero) img.type = Image.Type.Sliced;
            return img;
        }

        Text CreateText(string name, Transform parent, string content, int size, TextAnchor anchor, Color color)
        {
            var rt = CreateRect(name, parent);
            var text = rt.gameObject.AddComponent<Text>();
            text.font = font;
            text.fontSize = size;
            text.alignment = anchor;
            text.color = color;
            text.text = content;
            text.supportRichText = true;
            text.raycastTarget = false;
            text.horizontalOverflow = HorizontalWrapMode.Overflow;
            text.verticalOverflow = VerticalWrapMode.Overflow;
            if (color == Color.white)
                rt.gameObject.AddComponent<Shadow>().effectDistance = new Vector2(2, -3);
            return text;
        }

        Button CreateButton(string name, Transform parent, string label, Color color, Vector2 pos, Vector2 size, UnityEngine.Events.UnityAction onClick)
        {
            var img = CreateImage(name, parent, roundBoxSprite, color);
            Place(img.rectTransform, new Vector2(0.5f, 1), pos, size, new Vector2(0.5f, 0.5f));
            img.gameObject.AddComponent<Shadow>().effectDistance = new Vector2(0, -6);
            var btn = img.gameObject.AddComponent<Button>();
            var colors = btn.colors;
            colors.pressedColor = new Color(0.85f, 0.85f, 0.85f);
            colors.disabledColor = new Color(0.6f, 0.6f, 0.6f, 0.7f);
            btn.colors = colors;
            if (onClick != null) btn.onClick.AddListener(onClick);
            var text = CreateText("Label", img.rectTransform, label, 52, TextAnchor.MiddleCenter, Color.white);
            Stretch(text.rectTransform);
            return btn;
        }

        static void Place(RectTransform rt, Vector2 anchor, Vector2 pos, Vector2 size, Vector2 pivot)
        {
            rt.anchorMin = rt.anchorMax = anchor;
            rt.pivot = pivot;
            rt.anchoredPosition = pos;
            rt.sizeDelta = size;
        }

        static void SetTop(RectTransform rt, float width, float height, float y)
        {
            Place(rt, new Vector2(0.5f, 1f), new Vector2(0, y), new Vector2(width, height), new Vector2(0.5f, 1f));
        }

        static void Stretch(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
        }
    }
}
