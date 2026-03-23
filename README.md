# obsidian-daily-recap-skill

> Telegram chatlogs → Obsidian daily recap notes, fully automated.
>
> 把 Telegram 聊天日志自动整理成 Obsidian 每日复盘笔记。

Auto-summarize your Telegram conversations into structured Obsidian knowledge notes with topic grouping, actionable takeaways, and daily review questions. Works as an OpenClaw / Claude Code skill.

---

## Features

- **Topic grouping** — conversations organized by subject
- **Structured output** — 结论 / 例子 / 可复用做法 / 待办(TODO) for each item
- **Review questions** — 3 daily review questions for spaced repetition
- **Fault-tolerant** — placeholder recap when chatlog is missing (pipeline never breaks)
- **Backfill** — generate recaps for any past date or all available dates

---

## Install

### OpenClaw / Claude Code (recommended)

```bash
npx skills add kiki123124/obsidian-daily-recap-skill -g -y
```

### Manual install

```bash
git clone https://github.com/kiki123124/obsidian-daily-recap-skill.git
mkdir -p ~/.openclaw/workspace/skills
cp -R obsidian-daily-recap-skill ~/.openclaw/workspace/skills/obsidian-daily-recap
```

Restart your agent session after installing.

---

## Requirements

- Python 3.9+
- Chatlog files in markdown format

Configure paths via flags or env vars:

```bash
export RECAP_CHATLOG_DIR=/path/to/chatlogs
export RECAP_OUT_DIR=/path/to/obsidian/KnowledgeInbox
```

---

## Usage

```bash
# Yesterday's recap (default)
python3 scripts/build_recap.py

# Specific date
python3 scripts/build_recap.py --date 2026-03-19

# Backfill all available dates
python3 scripts/build_recap.py --all

# Custom paths
python3 scripts/build_recap.py \
  --date 2026-03-19 \
  --chatlog-dir /path/to/chatlogs \
  --out-dir /path/to/obsidian/KnowledgeInbox
```

Output file: `YYYY-MM-DD-对话知识点.md`

---

## Project structure

```
├── SKILL.md                        # Skill definition
├── obsidian-daily-recap.skill      # Distributable package
└── scripts/
    └── build_recap.py              # Main script
```

---

## Privacy

This repo only contains skill logic and package files — no personal chatlogs or vault content. Safe to publish as open-source template.

---

## License

[MIT](LICENSE)
