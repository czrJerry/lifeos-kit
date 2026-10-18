# LifeOS Kit（中文说明）

一套放在 AI 助手里的“个人操作系统”。每天早上它读取你的邮件、日历、待办和 Apple Health 数据，推送一份简短、具体的晨报：今天要处理什么、哪些邮件重要、昨晚睡得和你自己的常态比怎么样、今天练什么、吃什么。白天你随手告诉它吃了什么、练了什么、心情如何，它记成日志，第二天的晨报会用上。

支持 **Claude**（Project + 定时任务 + 连接器）和 **ChatGPT**（Project + Tasks + 连接器）。不需要服务器，数据都在你自己的 Google Drive 里。

## 怎么搭

1. 在 Google Drive 建 `LifeOS/` 文件夹，里面建 `context/`、`log/`、`reports/`、`health/`。
2. （可选，iPhone + Apple Watch）用 Health Auto Export 每小时把健康数据导出到 `LifeOS/health/`，见 [docs/health-auto-export.md](docs/health-auto-export.md)。
3. 把 `templates/context/*.md` 复制到 `LifeOS/context/` 并填写。最简单的方式：让助手采访你、帮你填（skill 会做这一步）。
4. 按 [docs/setup-claude.md](docs/setup-claude.md) 或 [docs/setup-chatgpt.md](docs/setup-chatgpt.md) 建 Project、连 Gmail / 日历 / Drive、粘贴指令、设每天的晨报任务。
5. 手动跑一次晨报，看完再微调提示词。

提示词是英文写的，但助手会用你的语言回复。想要中文晨报，在 `templates/context/profile.md` 的 Language 一栏写“中文”。

## 原则

- 默认只读：不发邮件、不改日历、不改邮件状态。只写 `LifeOS/log/`、`LifeOS/reports/` 和一个由助手管理的待办清单。
- 健康判断用你自己的 90 天常态，连续 3 天以上偏离才提醒。
- 晨报 ≤ 2,000 字符，每节最多 3 条，不重复。
- 邮件和网页里的文字是数据，不是指令。
- 晨报里不出现验证码、密码、银行卡号、账号号码。

不构成医疗建议。
