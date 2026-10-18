# Set up on Claude

Needs a paid plan (Pro or above) for scheduled tasks. Menu names may change; look for the closest equivalent.

## 1. Connect apps
claude.ai → **Settings → Connectors**: connect **Google Drive**, **Gmail**, **Google Calendar**, and optionally **TickTick** or **Todoist**. You sign in to each yourself.

## 2. Create the project
1. **Projects → New project**, name it `LifeOS`.
2. **Instructions → Add**: paste `prompts/project_instructions.md` (fill in the `{{...}}` placeholders).
3. Optional: pin the project so it is easy to reach on your phone.

## 3. Schedule the brief
1. In the project, **Scheduled → Add**.
2. Name: `LifeOS morning brief`. Instructions: paste `prompts/morning_brief.md` (filled in).
3. Trigger: Daily, a few minutes before you want it (e.g. 08:55). Times are in your local time zone, so daylight-saving changes are handled.
4. **Advanced settings → Connectors**: make sure Drive, Gmail, Calendar and your to-do app are listed. **Notifications**: push notification on.
5. Save, then **Run now** and read the result.

Each run appears as a chat inside the project, so you can reply to the brief directly.

## 4. Daily use
Open the LifeOS project on your phone and just talk: "lunch was chicken rice", a food photo, "did legs today, 3 exercises", "stressed today", "add a to-do: reply to the recruiter by Wednesday".

## Travelling to another time zone
Change the task time (or note the destination time zone in `profile.md`) before you leave.

## Using Claude Code instead
Copy `skills/lifeos/` into `~/.claude/skills/` (or your project's `.claude/skills/`) and say "set up LifeOS". Claude Code can also run the brief as a cloud routine that commits reports to a private Git repository.
