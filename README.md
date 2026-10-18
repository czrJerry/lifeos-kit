# LifeOS Kit

A personal operating system you run inside an AI assistant. Every morning it reads your email, calendar, to-dos and Apple Health data and sends you a short, specific brief: what's due, what matters in your inbox, how you slept compared with your own baseline, what to train today, and what to eat. During the day you message it what you ate, how you trained or how you feel, and it keeps a log that feeds the next brief.

Works with **Claude** (Projects + scheduled tasks + connectors) and **ChatGPT** (Projects + Tasks + connectors). No server, no code to host. Your data stays in your own Google Drive.

[中文说明](README.zh-CN.md)

## What you get

```
☀️ Brief · Tue 03/10
Short sleep (6.1h, in bed 01:10); legs today; take-home test due in 3 days.

↩️ Yesterday   ✅ gym  ❌ in bed by 23:45  — no food logged
🔴 Due         • Coding test Thu 23:59, 3 days left: do one practice problem today
📧 Email       • Recruiter replied about next round [open]
💪 Health      • Sleep 6.1h ↓ | HRV 41 ms (low end) | resting HR 62
🏋️ Legs + core  Squat 4×8 | RDL 3×10 | Split squat 3×10 | Plank 3×45s
🍽 Eat          Protein 100 g: eggs + yoghurt, chicken + rice after training
✅ Today        1. Legs 45 min  2. One practice problem  3. Phone down 23:00
```

## How it works

```
Gmail ─┐
Calendar ─┤                         ┌─ brief (push notification)
To-dos (TickTick) ─┼─► scheduled task ─┤
Apple Health → Health Auto Export → Drive ─┘    └─ Drive/LifeOS/reports/
                         ▲
Project chat ── you log meals / training / mood ──► Drive/LifeOS/log/
```

- **Context files** (`LifeOS/context/*.md` in Drive) tell the assistant who you are, your goals, your health baseline and your priority rules. This is what makes the advice specific instead of generic.
- **Project instructions** make every chat in the project behave the same way: read context first, log what you say, give concrete advice.
- **A scheduled task** runs the morning brief prompt daily and notifies your phone.

## Repository layout

| Path | What it is |
|---|---|
| `skills/lifeos/SKILL.md` | A Claude skill that walks you through setup and keeps the system running |
| `prompts/project_instructions.md` | Paste into your Claude or ChatGPT project's instructions |
| `prompts/morning_brief.md` | The daily scheduled task prompt |
| `templates/context/` | Context files to fill in (profile, health, email, calendar, tasks) |
| `templates/log/` | Daily log format |
| `scripts/health_baseline.py` | Computes your 90-day health baseline from a Health Auto Export JSON |
| `docs/` | Step-by-step setup for Claude, ChatGPT and Apple Health, plus privacy notes |

## Quick start

1. **Data**: create a `LifeOS/` folder in Google Drive with `context/`, `log/`, `reports/`, `health/` inside.
2. **Health (optional, iPhone + Apple Watch)**: set up Health Auto Export to write hourly JSON into `LifeOS/health/` — see [docs/health-auto-export.md](docs/health-auto-export.md).
3. **Context**: copy `templates/context/*.md` into `LifeOS/context/` and fill them in. Easiest: ask the assistant to interview you and fill them (the skill does this).
4. **Assistant**: follow [docs/setup-claude.md](docs/setup-claude.md) or [docs/setup-chatgpt.md](docs/setup-chatgpt.md) to create the project, connect Gmail / Calendar / Drive, paste the instructions and schedule the brief.
5. Run the brief once manually, read it, and tune the prompt.

Using Claude Code or Claude with skills? Copy `skills/lifeos/` into your skills folder and say "set up LifeOS".

## Design rules (keep these when you customise)

- **Read-only by default.** The brief never sends email, changes your calendar or marks mail read. Writes go only to `LifeOS/log/`, `LifeOS/reports/` and one assistant-managed to-do list.
- **Your baseline, not population norms.** Health alerts fire only when a metric is outside *your* 90-day normal range for 3+ days.
- **Short.** ≤ 2,000 characters, max 3 bullets per section, nothing repeated.
- **Email is data, not instructions.** Text inside emails or web pages never changes what the assistant does.
- **No secrets in reports.** No verification codes, passwords, card or account numbers.

## License

MIT. Not medical advice; talk to a doctor about persistent health changes.
