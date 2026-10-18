"""Compute health baselines from a Health Auto Export JSON (daily-grouped, summarized).

Usage: python3 health_baseline.py <export.json> [recent_days=14]
Prints a markdown-friendly summary: per-metric median/IQR, recent vs. baseline,
sleep timing, and workout patterns.
"""
import collections
import json
import statistics as st
import sys
from datetime import datetime, timedelta

KJ_PER_KCAL = 4.184

KEY_METRICS = [
    # name, label, transform, decimals
    ("resting_heart_rate", "Resting HR (bpm)", None, 0),
    ("heart_rate_variability", "HRV SDNN (ms)", None, 0),
    ("step_count", "Steps", None, 0),
    ("active_energy", "Active energy (kcal)", lambda v: v / KJ_PER_KCAL, 0),
    ("apple_exercise_time", "Exercise minutes", None, 0),
    ("apple_stand_hour", "Stand hours", None, 0),
    ("walking_running_distance", "Walk + run (km)", None, 1),
    ("time_in_daylight", "Time in daylight (min)", None, 0),
    ("respiratory_rate", "Respiratory rate (/min)", None, 1),
    ("blood_oxygen_saturation", "Blood oxygen (%)", None, 1),
    ("apple_sleeping_wrist_temperature", "Sleeping wrist temp (°C)", None, 2),
    ("walking_heart_rate_average", "Walking HR avg (bpm)", None, 0),
    ("vo2_max", "VO2max (ml/kg/min)", None, 1),
    ("breathing_disturbances", "Breathing disturbances (/h)", None, 1),
]


def day(s):
    return datetime.strptime(s[:10], "%Y-%m-%d").date()


def q(vals):
    vals = sorted(vals)
    if len(vals) < 4:
        return st.median(vals), min(vals), max(vals)
    qs = st.quantiles(vals, n=4)
    return qs[1], qs[0], qs[2]


def fmt(v, dec):
    return f"{v:.{dec}f}"


def main(path, recent_days=14):
    data = json.load(open(path))["data"]
    metrics = {m["name"]: m for m in data["metrics"]}
    all_days = [day(p["date"]) for m in data["metrics"] for p in m["data"]]
    end = max(all_days)
    cutoff = end - timedelta(days=recent_days)
    print(f"Range: {min(all_days)} → {end}; recent window: last {recent_days} days (>{cutoff})\n")

    print("| Metric | Baseline median | Normal range (IQR) | Recent median | Change | Days |")
    print("|---|---|---|---|---|---|")
    for name, label, tf, dec in KEY_METRICS:
        m = metrics.get(name)
        if not m:
            continue
        pts = [(day(p["date"]), p["qty"]) for p in m["data"] if "qty" in p]
        if tf:
            pts = [(d, tf(v)) for d, v in pts]
        base = [v for d, v in pts if d <= cutoff]
        recent = [v for d, v in pts if d > cutoff]
        if len(base) < 3:
            base = [v for _, v in pts]
        med, lo, hi = q(base)
        rmed = st.median(recent) if recent else None
        delta = f"{(rmed - med) / med * 100:+.0f}%" if rmed is not None and med else "—"
        print(f"| {label} | {fmt(med, dec)} | {fmt(lo, dec)}–{fmt(hi, dec)} | "
              f"{fmt(rmed, dec) if rmed is not None else '—'} | {delta} | {len(pts)} |")

    # Sleep
    sl = metrics.get("sleep_analysis", {}).get("data", [])
    if sl:
        print("\n### Sleep")
        rows = []
        for p in sl:
            s, e = p.get("sleepStart"), p.get("sleepEnd")
            if not s or not e:
                continue
            sd = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
            ed = datetime.strptime(e[:19], "%Y-%m-%d %H:%M:%S")
            rows.append(dict(
                night=day(p["date"]), total=p.get("totalSleep") or p.get("asleep") or 0,
                deep=p.get("deep", 0), rem=p.get("rem", 0), core=p.get("core", 0), awake=p.get("awake", 0),
                bed=sd.hour + sd.minute / 60 + (24 if sd.hour < 12 else 0),
                wake=ed.hour + ed.minute / 60, wd=ed.weekday()))
        rows = [r for r in rows if r["total"] > 2]

        def hhmm(h):
            h %= 24
            return f"{int(h):02d}:{int(round((h - int(h)) * 60)) % 60:02d}"

        def summarize(rs, tag):
            if not rs:
                return
            tot = [r["total"] for r in rs]
            print(f"- {tag} ({len(rs)} nights): total sleep median {st.median(tot):.1f} h (IQR {q(tot)[1]:.1f}–{q(tot)[2]:.1f}), "
                  f"deep {st.median([r['deep'] for r in rs]):.1f} h, REM {st.median([r['rem'] for r in rs]):.1f} h, "
                  f"awake {st.median([r['awake'] for r in rs]):.1f} h; bedtime {hhmm(st.median([r['bed'] for r in rs]))}, "
                  f"wake {hhmm(st.median([r['wake'] for r in rs]))}; nights under 6 h: {sum(t < 6 for t in tot)}")

        summarize(rows, "All")
        summarize([r for r in rows if r["wd"] < 5], "Waking on weekdays")
        summarize([r for r in rows if r["wd"] >= 5], "Waking on weekends")
        summarize([r for r in rows if r["night"] > cutoff], f"Last {recent_days} days")

    # Workouts
    wos = data.get("workouts", [])
    if wos:
        print("\n### Workouts")
        by_type = collections.defaultdict(list)
        hours = collections.Counter()
        weeks = collections.Counter()
        for w in wos:
            start = datetime.strptime(w["start"][:19], "%Y-%m-%d %H:%M:%S")
            dur = w.get("duration", 0) / 60
            hr = (w.get("heartRate") or {}).get("avg", {}).get("qty") or (w.get("avgHeartRate") or {}).get("qty")
            kj = (w.get("activeEnergyBurned") or {}).get("qty")
            by_type[w.get("name", "?")].append((start, dur, hr, kj))
            hours["morning (<10)" if start.hour < 10 else "day (10–17)" if start.hour < 17 else "evening (≥17)"] += 1
            weeks[start.isocalendar()[:2]] += 1
        span_weeks = max(1, (end - min(all_days)).days / 7)
        print(f"- {len(wos)} workouts, {len(wos) / span_weeks:.1f} per week; time of day: {dict(hours)} (raw entries; merge back-to-back strength segments yourself)")
        print("\n| Type | Count | Median min | Median avg HR | Median kcal | Last |")
        print("|---|---|---|---|---|---|")
        for t, xs in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
            durs = [x[1] for x in xs]
            hrs = [x[2] for x in xs if x[2]]
            kcal = [x[3] / KJ_PER_KCAL for x in xs if x[3]]
            print(f"| {t} | {len(xs)} | {st.median(durs):.0f} | {st.median(hrs):.0f} | "
                  f"{st.median(kcal):.0f} | {max(x[0] for x in xs):%m-%d} |" if hrs and kcal else
                  f"| {t} | {len(xs)} | {st.median(durs):.0f} | — | — | {max(x[0] for x in xs):%m-%d} |")
        recent_n = sum(1 for xs in by_type.values() for x in xs if x[0].date() > cutoff)
        print(f"\n- Last {recent_days} days: {recent_n} workouts (baseline about {len(wos) / span_weeks * recent_days / 7:.1f} per {recent_days} days)")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 14)
