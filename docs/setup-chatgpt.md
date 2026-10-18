# Set up on ChatGPT

ChatGPT features change often and depend on your plan and region. Check the current behaviour of each item below the first time you set it up.

## 1. Connect apps
**Settings → Apps / Connectors**: connect **Google Drive**, **Gmail**, **Google Calendar**, and your to-do app if one is available. You sign in to each yourself.

## 2. Create the project
1. **Projects → New project** `LifeOS`.
2. Project **instructions**: paste `prompts/project_instructions.md` (fill in the `{{...}}`).
3. Keep context files in **Google Drive** `LifeOS/context/`, not as project file uploads: scheduled tasks created in a project cannot read the project's uploaded files, but they can read Drive through the connector.

## 3. Schedule the brief
1. In a chat, ask: *"Every day at 08:55, run the following and send me the result"*, then paste `prompts/morning_brief.md` (filled in). ChatGPT creates a **scheduled task**; manage it on the **Scheduled** page.
2. Turn on notifications for tasks (push or email) in Settings.
3. Run it once and read the result.

### Known differences from Claude
- Drive writes and to-do writes depend on what the connector allows on your plan. If the task cannot save to Drive or create tasks, remove section 4 of the brief prompt and the "save a copy" line; the brief still works as a notification.
- If scheduled tasks on your plan cannot use connectors, run the brief manually each morning in the project ("run my morning brief") with the same prompt saved as a project file or custom GPT instruction.

## 4. Daily use
Same as Claude: talk to the LifeOS project, send food photos, say what you trained.
