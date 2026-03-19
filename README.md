# obsidian-daily-recap-skill

Generate structured daily recap notes from Telegram chatlogs into Obsidian `KnowledgeInbox`.

## What it does

For each day, this skill creates a markdown recap file with:

- Topic grouping
- `结论 / 例子 / 可复用做法 / 待办(TODO)` for each item
- Exactly 3 `明日复盘问题`

If the source chatlog is missing, it still creates a placeholder recap so your daily review pipeline does not break.

---

## Repository structure

```text
.
├── SKILL.md
├── obsidian-daily-recap.skill
└── scripts/
    └── build_recap.py
```

---

## Requirements

- Python 3.9+
- Telegram chatlog files in markdown format

Default paths used by `build_recap.py`:

- Chatlog dir: `/Users/mac/.openclaw/workspace/memory/chatlog/telegram-6404111657`
- Output dir: `/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/BossmanVault/KnowledgeInbox`

You can override both via CLI flags.

---

## Usage

### 1) Build yesterday recap

```bash
python3 scripts/build_recap.py
```

### 2) Build one specific date

```bash
python3 scripts/build_recap.py --date 2026-03-19
```

### 3) Backfill all available dates

```bash
python3 scripts/build_recap.py --all
```

### 4) Custom input/output paths

```bash
python3 scripts/build_recap.py \
  --date 2026-03-19 \
  --chatlog-dir /path/to/chatlogs \
  --out-dir /path/to/obsidian/KnowledgeInbox
```

---

## Output file naming

Generated file name:

```text
YYYY-MM-DD-对话知识点.md
```

---

## Packaging as `.skill`

If you want to republish/update the distributable package:

```bash
python3 /Users/mac/Library/pnpm/global/5/.pnpm/openclaw@2026.3.8_@napi-rs+canvas@0.1.96_@types+express@5.0.6_hono@4.12.7_node-llama-cpp@3.16.2/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py .
```

Then copy/rename generated archive to `obsidian-daily-recap.skill` if needed.

---

## Notes

- This repo contains skill logic and package only (no personal chatlogs included).
- Keep private data out of commits.
