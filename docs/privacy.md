# Privacy and safety

- **Where data lives**: your Google Drive (`LifeOS/`), your assistant account and your to-do app. Nothing in this kit sends data anywhere else.
- **Keep context out of Git.** If you version your own LifeOS, use a private repository and keep raw health exports out of it (`.gitignore` them). This public kit contains templates only.
- **Least privilege**: the prompts are read-only for email and calendar. Only grant write tools you are comfortable with; the brief works without them.
- **Prompt injection**: emails and web pages can contain text aimed at AI assistants. The prompts treat all such content as data. Keep that rule if you edit them.
- **Secrets**: never paste API keys, bot tokens or passwords into a chat. If you do, revoke and replace them.
- **Health**: baselines are personal trends, not diagnoses. See a doctor for persistent changes.
- **Region availability**: Claude, ChatGPT and Google services are not available in every country. A scheduled task keeps running in the cloud wherever you are, but reading the result and logging from your phone needs access to the service. Check the provider's supported-regions list and terms before you travel.
