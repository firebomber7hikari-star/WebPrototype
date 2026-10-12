using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace FindDifferences
{
    /// <summary>
    /// One of the two pictures: static background + animated element layer + marker layer.
    /// Converts taps to texture-pixel coordinates and draws markers.
    /// </summary>
    [RequireComponent(typeof(Image))]
    public class DifferencePicture : MonoBehaviour, IPointerDownHandler
    {
        public event Action<DifferencePicture, Vector2> Tapped;

        Image _image;
        RectTransform _rect;
        RectTransform _elementLayer;
        RectTransform _markerLayer;
        Vector2 _textureSize = new Vector2(900, 600);
        Vector2 _frameHome;
        readonly List<GameObject> _markers = new List<GameObject>();

        struct LiveElement
        {
            public RectTransform rect;
            public Image image;
            public ElementAnim anim;
            public Vector2 basePosition;
            public DayNightMode dayNight;
            public int weatherMask;
            public int viewMask;
        }

        struct TrackedMarker
        {
            public Difference diff;
            public Image image;
        }
        readonly List<TrackedMarker> _tracked = new List<TrackedMarker>();
        CameraOrbit _orbit;
        List<Sprite> _frames;
        Image _frameBlend;
        int _view;
        float _turn;

        /// <summary>Main view currently shown (camera-orbit levels; 0 otherwise).</summary>
        public int CurrentView => _view;
        /// <summary>True while the camera is moving between two views.</summary>
        public bool IsTurning => _orbit != null && _turn > 0.02f && _turn < 0.98f;
        public Vector2 DiffCenter(Difference d) => _orbit != null ? d.CenterInView(_view) : d.center;
        readonly List<LiveElement> _elements = new List<LiveElement>();
        float _startTime;
        DayNightCycle _cycle;
        WeatherCycle _weather;
        readonly float[] _weatherWeights = new float[WeatherCycle.TypeCount];

        public RectTransform Rect => _rect;

        /// <param name="modified">True for the bottom picture (uses the modified sprite/anim).</param>
        public void Init(FindDifferencesLevel level, bool modified)
        {
            Sprite background = modified ? level.modified : level.original;
            _cycle = level.dayNight != null && level.dayNight.Enabled ? level.dayNight : null;
            _weather = level.weather != null && level.weather.Enabled ? level.weather : null;
            _image = GetComponent<Image>();
            _rect = (RectTransform)transform;
            if (_markerLayer == null)
            {
                var blend = CreateLayer("FrameBlend");
                _frameBlend = blend.gameObject.AddComponent<Image>();
                _frameBlend.raycastTarget = false;
                _elementLayer = CreateLayer("Elements");
                _markerLayer = CreateLayer("Markers");
                _frameHome = ((RectTransform)transform.parent).anchoredPosition;
            }
            _orbit = level.orbit != null && level.orbit.Enabled ? level.orbit : null;
            _frames = _orbit == null ? null : (modified ? _orbit.framesModified : _orbit.framesOriginal);
            if (_frames != null && _frames.Count > 0) background = _frames[0];
            _frameBlend.enabled = _orbit != null;
            _view = 0;
            _turn = 0f;
            _image.sprite = background;
            _image.color = Color.white;
            if (background != null) _textureSize = background.rect.size;
            ClearMarkers();
            BuildElements(level.elements, modified);
        }

        RectTransform CreateLayer(string name)
        {
            var rt = (RectTransform)new GameObject(name, typeof(RectTransform)).transform;
            rt.SetParent(transform, false);
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return rt;
        }

        void BuildElements(IList<AnimatedElement> elements, bool modified)
        {
            foreach (var e in _elements) Destroy(e.rect.gameObject);
            _elements.Clear();
            _startTime = Time.time;
            if (elements == null) return;

            foreach (var def in elements)
            {
                var sprite = modified ? def.spriteModified : def.spriteOriginal;
                if (sprite == null) continue;

                var go = new GameObject(def.id, typeof(RectTransform), typeof(Image));
                var rt = (RectTransform)go.transform;
                rt.SetParent(_elementLayer, false);
                rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
                rt.pivot = def.pivot;
                rt.sizeDelta = sprite.rect.size * PixelScale;
                var img = go.GetComponent<Image>();
                img.sprite = sprite;
                img.raycastTarget = false;

                var live = new LiveElement
                {
                    rect = rt,
                    image = img,
                    anim = modified ? def.animModified : def.animOriginal,
                    basePosition = def.position,
                    dayNight = def.dayNight,
                    weatherMask = def.weatherMask,
                    viewMask = def.viewMask,
                };
                _elements.Add(live);
                Animate(live, 0f, 0f, Color.white, null);
            }
        }

        void Update()
        {
            // both pictures are initialised in the same frame, so their clocks stay in sync
            float t = Time.time - _startTime;
            float night = _cycle != null ? _cycle.NightFactor(t) : 0f;
            Color tint = _cycle != null ? _cycle.Tint(night) : Color.white;
            float[] weather = null;
            if (_weather != null)
            {
                _weather.Evaluate(t, _weatherWeights);
                tint *= _weather.Tint(_weatherWeights);
                weather = _weatherWeights;
            }
            int fromView = 0;
            if (_orbit != null && _frames != null && _frames.Count > 1)
            {
                _orbit.Evaluate(t, out float yaw01, out fromView, out _turn);
                _view = _turn < 0.5f ? fromView : (fromView + 1) % _orbit.viewCount;
                float pos = Mathf.Repeat(yaw01, 1f) * _frames.Count;
                int i0 = Mathf.FloorToInt(pos) % _frames.Count;
                int i1 = (i0 + 1) % _frames.Count;
                _image.sprite = _frames[i0];
                _frameBlend.sprite = _frames[i1];
                _frameBlend.color = new Color(tint.r, tint.g, tint.b, pos - Mathf.Floor(pos));
                UpdateTrackedMarkers();
            }
            if (_image != null) _image.color = tint;
            for (int i = 0; i < _elements.Count; i++)
                Animate(_elements[i], t, night, tint, weather, fromView);
        }

        void UpdateTrackedMarkers()
        {
            bool show = !IsTurning;
            for (int i = _tracked.Count - 1; i >= 0; i--)
            {
                var m = _tracked[i];
                if (m.image == null) { _tracked.RemoveAt(i); continue; }
                m.image.rectTransform.anchoredPosition = ToLocal(DiffCenter(m.diff));
                m.image.enabled = show;
            }
        }

        void Animate(LiveElement e, float t, float night, Color tint, float[] weather, int fromView = 0)
        {
            Vector2 offset = Vector2.zero;
            Vector2 scale = Vector2.one;
            float angle = 0f, alpha = 1f, brightness = 1f;
            if (e.anim != null)
                e.anim.Evaluate(t, out offset, out angle, out scale, out alpha, out brightness);

            if (e.weatherMask != 0)
            {
                float visible = 0f;
                if (weather == null) visible = (e.weatherMask & 1) != 0 ? 1f : 0f;   // no cycle = clear sky
                else
                    for (int i = 0; i < weather.Length; i++)
                        if ((e.weatherMask & (1 << i)) != 0) visible += weather[i];
                alpha *= Mathf.Clamp01(visible);
            }

            if (e.viewMask != 0 && _orbit != null)
            {
                float w = 0f;
                for (int v = 0; v < _orbit.viewCount; v++)
                    if ((e.viewMask & (1 << v)) != 0) w += _orbit.ViewWeight(v, fromView, _turn);
                alpha *= Mathf.Clamp01(w);
            }

            switch (e.dayNight)
            {
                case DayNightMode.Tinted: break;
                case DayNightMode.NightOnly: alpha *= night; tint = Color.white; break;
                case DayNightMode.DayOnly: alpha *= 1f - night; tint = Color.white; break;
                default: tint = Color.white; break;
            }

            e.rect.anchoredPosition = ToLocal(e.basePosition + offset);
            e.rect.localEulerAngles = new Vector3(0, 0, angle);
            e.rect.localScale = new Vector3(scale.x, scale.y, 1f);
            e.image.color = new Color(brightness * tint.r, brightness * tint.g, brightness * tint.b, alpha);
        }

        public void OnPointerDown(PointerEventData eventData)
        {
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(_rect, eventData.position, eventData.pressEventCamera, out var local))
                return;
            Vector2 size = _rect.rect.size;
            Vector2 uv = new Vector2(local.x / size.x + _rect.pivot.x, local.y / size.y + _rect.pivot.y);
            if (uv.x < 0 || uv.x > 1 || uv.y < 0 || uv.y > 1) return;
            Tapped?.Invoke(this, Vector2.Scale(uv, _textureSize));
        }

        /// <summary>Texture pixels to local UI units.</summary>
        float PixelScale => _rect.rect.width / _textureSize.x;

        Vector2 ToLocal(Vector2 px)
        {
            Vector2 size = _rect.rect.size;
            return new Vector2(px.x / _textureSize.x * size.x, px.y / _textureSize.y * size.y)
                   - new Vector2(size.x * _rect.pivot.x, size.y * _rect.pivot.y);
        }

        Image CreateMarker(string name, Sprite sprite, Vector2 px, float diameterPx, Color color)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            var rt = (RectTransform)go.transform;
            rt.SetParent(_markerLayer, false);
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = ToLocal(px);
            float d = diameterPx * PixelScale;
            rt.sizeDelta = new Vector2(d, d);
            var img = go.GetComponent<Image>();
            img.sprite = sprite;
            img.color = color;
            img.raycastTarget = false;
            _markers.Add(go);
            return img;
        }

        public void ShowFound(Difference diff, Sprite ring, Color color)
        {
            var img = CreateMarker("Found_" + diff.id, ring, DiffCenter(diff), Mathf.Max(diff.radius * 2.2f, 56f), color);
            _tracked.Add(new TrackedMarker { diff = diff, image = img });
            StartCoroutine(Pop(img.rectTransform));
        }

        public void ShowWrong(Vector2 px, Sprite cross, Color color)
        {
            var img = CreateMarker("Wrong", cross, px, 70f, color);
            StartCoroutine(PopAndFade(img));
        }

        public void ShowHint(Difference diff, Sprite circle, Color color)
        {
            var img = CreateMarker("Hint_" + diff.id, circle, DiffCenter(diff), Mathf.Max(diff.radius * 2.4f, 70f), color);
            _tracked.Add(new TrackedMarker { diff = diff, image = img });
            StartCoroutine(Pulse(img));
        }

        public void Shake() => StartCoroutine(ShakeRoutine());

        public void ClearMarkers()
        {
            StopAllCoroutines();
            if (_markerLayer != null) ((RectTransform)transform.parent).anchoredPosition = _frameHome;
            foreach (var m in _markers)
                if (m != null) Destroy(m);
            _markers.Clear();
            _tracked.Clear();
        }

        static IEnumerator Pop(RectTransform rt)
        {
            const float duration = 0.35f;
            for (float t = 0; t < duration; t += Time.unscaledDeltaTime)
            {
                float k = t / duration;
                // grow with a little overshoot
                float s = Mathf.Lerp(0.2f, 1f, Mathf.Sqrt(k)) * (1f + 0.3f * Mathf.Sin(k * Mathf.PI));
                rt.localScale = Vector3.one * s;
                yield return null;
            }
            rt.localScale = Vector3.one;
        }

        IEnumerator PopAndFade(Image img)
        {
            var rt = img.rectTransform;
            Color c = img.color;
            const float duration = 0.8f;
            for (float t = 0; t < duration; t += Time.unscaledDeltaTime)
            {
                float k = t / duration;
                rt.localScale = Vector3.one * (k < 0.2f ? Mathf.Lerp(0.3f, 1.15f, k / 0.2f) : 1f);
                img.color = new Color(c.r, c.g, c.b, c.a * (k < 0.5f ? 1f : 1f - (k - 0.5f) / 0.5f));
                yield return null;
            }
            _markers.Remove(img.gameObject);
            Destroy(img.gameObject);
        }

        IEnumerator Pulse(Image img)
        {
            var rt = img.rectTransform;
            Color c = img.color;
            const float duration = 2f;
            for (float t = 0; t < duration; t += Time.unscaledDeltaTime)
            {
                float wave = 0.5f + 0.5f * Mathf.Sin(t * Mathf.PI * 3f);
                rt.localScale = Vector3.one * (0.9f + 0.2f * wave);
                float fade = t > duration - 0.4f ? (duration - t) / 0.4f : 1f;
                img.color = new Color(c.r, c.g, c.b, c.a * (0.4f + 0.6f * wave) * fade);
                yield return null;
            }
            _markers.Remove(img.gameObject);
            Destroy(img.gameObject);
        }

        IEnumerator ShakeRoutine()
        {
            var target = (RectTransform)transform.parent; // frame
            Vector2 start = _frameHome;
            const float duration = 0.25f;
            for (float t = 0; t < duration; t += Time.unscaledDeltaTime)
            {
                float amp = 12f * (1 - t / duration);
                target.anchoredPosition = start + new Vector2(Mathf.Sin(t * 90f) * amp, 0);
                yield return null;
            }
            target.anchoredPosition = start;
        }
    }
}
