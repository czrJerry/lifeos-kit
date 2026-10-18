# Apple Health → Google Drive (Health Auto Export)

Apple Health has no cloud API, so a phone app has to push the data out. Health Auto Export (iOS App Store, paid after a trial) can export every metric, including State of Mind, on a schedule.

## Why not Apple Shortcuts?
Shortcuts' "Find Health Samples" works one type at a time and cannot read several categories, so a full export is not practical.

## Set up three automations
In Health Auto Export → **Automations**, create:

| Automation | Data | Aggregation | Format | Destination |
|---|---|---|---|---|
| Metrics | All health metrics | **Hours** | JSON (v2) | Google Drive `LifeOS/health/` |
| Workouts | Workouts | default | JSON | same |
| State of Mind | State of Mind | default | JSON | same |

- Sync cadence: hourly. Date range: today (the file for each day is rewritten as data arrives).
- **Use hourly aggregation for metrics.** Without it the app exports raw samples (one per minute for energy and heart rate), around 600 KB per day, which scheduled assistant tasks cannot read. Hourly is around 15 KB and keeps overnight HRV readings. Daily aggregation loses overnight detail.
- Exports run only while the iPhone is unlocked. If the brief is generated before you pick up your phone in the morning, last night's sleep may be missing; schedule the brief after you usually wake.

## Baseline
For the first setup, do a one-off manual export of the last 90 days (daily aggregation, JSON), then:

```bash
python3 scripts/health_baseline.py HealthAutoExport-90days.json 14
```

Copy the tables into `LifeOS/context/health.md`. Re-run monthly.

## Gotchas
- Apple Watch splits a long strength session into several back-to-back "Traditional Strength Training" entries. Merge them before counting sessions.
- A bike or walking commute will show up as a workout; list it in `health.md` so it is not counted.
- `active_energy` is in kJ (÷ 4.184 for kcal).
