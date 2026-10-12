using System;
using System.Collections.Generic;
using UnityEngine;

namespace FindDifferences
{
    /// <summary>One difference area, in texture pixels (origin bottom-left).</summary>
    [Serializable]
    public class Difference
    {
        public string id;
        public Vector2 center;
        public float radius = 40f;
        [Tooltip("Camera-orbit levels: centre of this difference in each main view (empty = use center).")]
        public List<Vector2> viewCenters = new List<Vector2>();

        public Vector2 CenterInView(int view) =>
            viewCenters != null && view >= 0 && view < viewCenters.Count ? viewCenters[view] : center;
    }

    /// <summary>
    /// Timed camera orbit: the scene is pre-rendered every (360 / frame count) degrees. The camera holds on each
    /// of the <see cref="viewCount"/> main views for <see cref="holdTime"/> seconds, then turns to the next one in
    /// <see cref="turnTime"/> seconds; after viewCount turns it is back at the start.
    /// </summary>
    [Serializable]
    public class CameraOrbit
    {
        public int viewCount = 3;
        public float holdTime = 5f;
        public float turnTime = 1f;
        [Tooltip("Frames of the original picture, evenly spaced over a full turn (frame 0 = view 0).")]
        public List<Sprite> framesOriginal = new List<Sprite>();
        public List<Sprite> framesModified = new List<Sprite>();

        public bool Enabled => framesOriginal != null && framesOriginal.Count > 1 && viewCount > 0;
        public float SegmentTime => holdTime + turnTime;

        /// <param name="yaw01">Camera yaw as a fraction of a full turn.</param>
        /// <param name="fromView">Main view the camera is at / leaving.</param>
        /// <param name="turn">0 while holding, 0..1 while turning to the next view.</param>
        /// <remarks>Mirrored by orbit_state() in Tools~/orbit3d.py.</remarks>
        public void Evaluate(float t, out float yaw01, out int fromView, out float turn)
        {
            float seg = Mathf.Max(0.01f, SegmentTime);
            int index = Mathf.FloorToInt(t / seg);
            float local = t - index * seg;
            fromView = ((index % viewCount) + viewCount) % viewCount;
            turn = local <= holdTime ? 0f : Mathf.SmoothStep(0f, 1f, Mathf.Clamp01((local - holdTime) / Mathf.Max(0.01f, turnTime)));
            yaw01 = (fromView + turn) / viewCount;
        }

        /// <summary>Visibility of things that belong to one main view (fade out right after leaving, in right before arriving).</summary>
        public float ViewWeight(int view, int fromView, float turn)
        {
            if (view == fromView) return turn <= 0f ? 1f : Mathf.Clamp01(1f - turn / 0.15f);
            if (view == (fromView + 1) % viewCount) return Mathf.Clamp01((turn - 0.85f) / 0.15f);
            return 0f;
        }
    }

    /// <summary>
    /// Procedural motion for an animated element. All channels add up; zero values mean "off".
    /// Speeds are cycles per second, distances are texture pixels, angles are degrees.
    /// </summary>
    [Serializable]
    public class ElementAnim
    {
        [Tooltip("0..1, shifts every oscillation and the drift loop.")]
        public float phase;

        [Header("Bob (position oscillation)")]
        public Vector2 bobAmplitude;
        public float bobSpeed;
        [Tooltip("Use |sin| on Y so the element bounces off its rest position.")]
        public bool bounce;

        [Header("Rotation")]
        public float swingAngle;
        public float swingSpeed;
        [Tooltip("Continuous spin, degrees per second (positive = counter-clockwise).")]
        public float rotateSpeed;

        [Header("Scale")]
        public float pulse;
        [Tooltip("Extra per-axis scale oscillation, e.g. (0, 0.6) for flapping wings.")]
        public Vector2 stretch;
        public float scaleSpeed;

        [Header("Alpha")]
        [Range(0, 1)] public float twinkle;
        public float twinkleSpeed;

        [Header("Drift (looping travel)")]
        public Vector2 driftVelocity;
        [Tooltip("Path length before the element wraps back.")]
        public float driftLength;
        [Tooltip("Path offset where the loop begins (negative = start before the rest position).")]
        public float driftStart;
        [Tooltip("Fade in/out along the path (smoke, bubbles).")]
        public bool driftFade;
        [Tooltip("Extra scale gained at the end of the path.")]
        public float driftGrow;

        [Header("Orbit (fake 3D: closer = bigger and brighter)")]
        [Tooltip("Ellipse radii; a flat Y radius reads as a tilted circle.")]
        public Vector2 orbitRadius;
        [Tooltip("Revolutions per second; the sign sets the direction.")]
        public float orbitSpeed;
        [Range(0, 1)] public float orbitDepth;
        [Tooltip("Rotate the element so it faces along the orbit (sprite drawn facing +X).")]
        public bool orbitAlign;

        [Header("3D spin around the vertical axis")]
        public float spinSpeed;
        [Tooltip("How much darker the element gets when seen edge-on.")]
        [Range(0, 1)] public float spinShade;
        [Tooltip("0 = smooth turn; towards 1 the element stays flat and flips quickly (paper cut-out turning around).")]
        [Range(0, 1)] public float spinSnap;

        [Header("Blink (lightning, flashes)")]
        [Tooltip("Seconds between flashes; 0 = off.")]
        public float blinkInterval;
        [Tooltip("How long one flash lasts (it fades out with a short double flicker).")]
        public float blinkDuration = 0.3f;

        /// <remarks>Mirrored by eval_anim() in Tools~/fdcore.py (used for the animated previews).</remarks>
        public void Evaluate(float t, out Vector2 offset, out float angle, out Vector2 scale, out float alpha, out float brightness)
        {
            const float Tau = Mathf.PI * 2f;
            float ph = phase * Tau;

            float bob = Mathf.Sin(t * bobSpeed * Tau + ph);
            offset = bobAmplitude * bob;
            if (bounce) offset.y = Mathf.Abs(bob) * bobAmplitude.y;

            angle = rotateSpeed * t + swingAngle * Mathf.Sin(t * swingSpeed * Tau + ph);

            float w = Mathf.Sin(t * scaleSpeed * Tau + ph);
            float s = 1f + pulse * w;
            scale = new Vector2(s * (1f + stretch.x * w), s * (1f + stretch.y * w));

            alpha = 1f - twinkle * (0.5f + 0.5f * Mathf.Sin(t * twinkleSpeed * Tau + ph));
            brightness = 1f;

            if (orbitSpeed != 0f && orbitRadius != Vector2.zero)
            {
                float a = t * orbitSpeed * Tau + ph;
                offset += new Vector2(Mathf.Cos(a) * orbitRadius.x, Mathf.Sin(a) * orbitRadius.y);
                float depth = -Mathf.Sin(a); // lower half of the tilted orbit is closer to the viewer
                scale *= 1f + orbitDepth * depth;
                brightness *= 1f - orbitDepth * 0.8f * (1f - depth) * 0.5f;
                if (orbitAlign)
                {
                    float dir = Mathf.Sign(orbitSpeed);
                    angle += Mathf.Atan2(Mathf.Cos(a) * orbitRadius.y * dir, -Mathf.Sin(a) * orbitRadius.x * dir) * Mathf.Rad2Deg;
                }
            }

            if (spinSpeed != 0f)
            {
                float c = Mathf.Cos(t * spinSpeed * Tau + ph);
                if (spinSnap > 0f) c = Mathf.Sign(c) * Mathf.Pow(Mathf.Abs(c), 1f - 0.9f * spinSnap);
                scale.x *= c;
                brightness *= 1f - spinShade * (1f - Mathf.Abs(c));
            }

            if (blinkInterval > 0f)
            {
                float local = Mathf.Repeat(t + phase * blinkInterval, blinkInterval);
                float d = Mathf.Max(0.01f, blinkDuration);
                float k = local < d ? 1f - local / d : 0f;
                if (local > d * 0.3f && local < d * 0.45f) k *= 0.25f;   // double flicker
                alpha *= k;
            }

            float speed = driftVelocity.magnitude;
            if (driftLength > 0f && speed > 0f)
            {
                float d = Mathf.Repeat(phase * driftLength + t * speed, driftLength);
                offset += driftVelocity / speed * (driftStart + d);
                float p = d / driftLength;
                if (driftFade) alpha *= Mathf.Sin(p * Mathf.PI);
                scale *= 1f + driftGrow * p;
            }
        }
    }

    /// <summary>How an element reacts to the level's day/night cycle.</summary>
    public enum DayNightMode
    {
        [Tooltip("Darkened with the scene at night.")] Tinted = 0,
        [Tooltip("Only visible at night, not darkened (moon, stars, lit windows).")] NightOnly = 1,
        [Tooltip("Fades out at night, not darkened (sun).")] DayOnly = 2,
        [Tooltip("Ignores the cycle.")] Untinted = 3,
    }

    /// <summary>Day/night cycle shared by both pictures of a level.</summary>
    [Serializable]
    public class DayNightCycle
    {
        [Tooltip("Seconds for a full day + night; 0 disables the cycle.")]
        public float period;
        [Tooltip("0..1 offset into the cycle at level start (0 = middle of the day).")]
        public float phase;
        [Tooltip("Multiplier applied to the scene in the middle of the night.")]
        public Color nightTint = new Color(0.33f, 0.37f, 0.62f, 1f);

        public bool Enabled => period > 0f;

        /// <summary>0 = full day, 1 = full night. Days and nights hold for a while, dusk/dawn blend smoothly.</summary>
        /// <remarks>Mirrored by night_factor() in Tools~/fdcore.py.</remarks>
        public float NightFactor(float t)
        {
            if (period <= 0f) return 0f;
            float raw = 0.5f - 0.5f * Mathf.Cos((t / period + phase) * Mathf.PI * 2f);
            return Mathf.SmoothStep(0f, 1f, Mathf.InverseLerp(0.25f, 0.75f, raw));
        }

        public Color Tint(float night) => Color.Lerp(Color.white, nightTint, night);
    }

    public enum WeatherType { Clear = 0, Overcast = 1, Rain = 2, Snow = 3, Fog = 4, Thunder = 5, Heat = 6 }

    [Serializable]
    public class WeatherStep
    {
        public WeatherType type;
        public float duration = 10f;
    }

    /// <summary>
    /// Looping weather sequence shared by both pictures. Each step cross-fades into the next one
    /// during its last <see cref="blend"/> seconds.
    /// </summary>
    [Serializable]
    public class WeatherCycle
    {
        public const int TypeCount = 7;

        public List<WeatherStep> steps = new List<WeatherStep>();
        public float blend = 3f;
        [Header("Scene tint per weather (Clear = white)")]
        public Color overcastTint = new Color(0.80f, 0.82f, 0.88f, 1f);
        public Color rainTint = new Color(0.64f, 0.69f, 0.80f, 1f);
        public Color snowTint = new Color(0.90f, 0.93f, 1.00f, 1f);
        public Color fogTint = new Color(0.90f, 0.92f, 0.95f, 1f);
        public Color thunderTint = new Color(0.46f, 0.49f, 0.64f, 1f);
        public Color heatTint = new Color(1.00f, 0.90f, 0.72f, 1f);

        public bool Enabled => steps != null && steps.Count > 0;

        /// <summary>Fills weights[type] (0..1, summing to 1) for time t.</summary>
        /// <remarks>Mirrored by weather_weights() in Tools~/fdcore.py.</remarks>
        public void Evaluate(float t, float[] weights)
        {
            Array.Clear(weights, 0, weights.Length);
            if (!Enabled) { weights[0] = 1f; return; }
            float total = 0f;
            foreach (var s in steps) total += Mathf.Max(0.01f, s.duration);
            float tau = Mathf.Repeat(t, total);
            float start = 0f;
            for (int i = 0; i < steps.Count; i++)
            {
                float d = Mathf.Max(0.01f, steps[i].duration);
                if (tau < start + d || i == steps.Count - 1)
                {
                    int cur = (int)steps[i].type;
                    int next = (int)steps[(i + 1) % steps.Count].type;
                    float b = Mathf.Min(blend, d);
                    float into = tau - (start + d - b);
                    if (b > 0f && into > 0f)
                    {
                        float k = Mathf.SmoothStep(0f, 1f, into / b);
                        weights[cur] += 1f - k;
                        weights[next] += k;
                    }
                    else weights[cur] += 1f;
                    return;
                }
                start += d;
            }
        }

        public Color Tint(float[] w)
        {
            Color c = Color.white * w[0]
                      + overcastTint * w[1] + rainTint * w[2] + snowTint * w[3]
                      + fogTint * w[4] + thunderTint * w[5] + heatTint * w[6];
            c.a = 1f;
            return c;
        }
    }

    /// <summary>A sprite layered on top of the background that moves procedurally.</summary>
    [Serializable]
    public class AnimatedElement
    {
        public string id;
        [Tooltip("Sprite shown in the original (top) picture; empty = hidden there.")]
        public Sprite spriteOriginal;
        [Tooltip("Sprite shown in the modified (bottom) picture; empty = hidden there.")]
        public Sprite spriteModified;
        [Tooltip("Pivot position in texture pixels (origin bottom-left).")]
        public Vector2 position;
        [Tooltip("Normalized pivot inside the sprite (rotation / scale center).")]
        public Vector2 pivot = new Vector2(0.5f, 0.5f);
        public ElementAnim animOriginal = new ElementAnim();
        public ElementAnim animModified = new ElementAnim();
        public DayNightMode dayNight = DayNightMode.Tinted;
        [Tooltip("Bit mask of WeatherType (1 << type) in which the element is visible; 0 = always.")]
        public int weatherMask;
        [Tooltip("Camera-orbit levels: bit mask of main views the element belongs to; 0 = all.")]
        public int viewMask;
    }

    [CreateAssetMenu(menuName = "Find Differences/Level", fileName = "Level")]
    public class FindDifferencesLevel : ScriptableObject
    {
        public string levelName;
        [Tooltip("Static background of the original picture.")]
        public Sprite original;
        [Tooltip("Static background of the modified picture.")]
        public Sprite modified;
        [Tooltip("Seconds available to finish the level.")]
        public float timeLimit = 90f;
        public List<Difference> differences = new List<Difference>();
        [Tooltip("Animated layers, drawn in list order on top of the backgrounds.")]
        public List<AnimatedElement> elements = new List<AnimatedElement>();
        public DayNightCycle dayNight = new DayNightCycle();
        public WeatherCycle weather = new WeatherCycle();
        public CameraOrbit orbit = new CameraOrbit();

        public Vector2 TextureSize => original != null ? original.rect.size : new Vector2(900, 600);
    }
}
