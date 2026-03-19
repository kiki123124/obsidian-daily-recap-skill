# 🧠 obsidian-daily-recap-skill

> ✨ 把 Telegram 聊天日志自动整理成 Obsidian 每日复盘笔记。

Generate structured daily recap notes from Telegram chatlogs into Obsidian `KnowledgeInbox`.

## 🚀 Why this skill

For each day, it generates one recap markdown file with:

- 🗂️ Topic grouping
- ✅ `结论 / 例子 / 可复用做法 / 待办(TODO)` for each item
- 🔁 Exactly 3 `明日复盘问题`
- 🛟 Placeholder recap when chatlog is missing (pipeline never breaks)

---

## 📦 Install (OpenClaw / Claude Code)

### Option A — npx + ClawHub (recommended)

```bash
npx -y clawhub install <your-skill-slug>
```

Then start a new session (or restart gateway) to load newly installed skills.

> Tip: if `clawhub` isn’t configured yet:
>
> ```bash
> npx -y clawhub login
> npx -y clawhub search "obsidian daily recap"
> ```

### Option B — local install from GitHub repo

```bash
git clone https://github.com/kiki123124/obsidian-daily-recap-skill.git
mkdir -p ~/.openclaw/workspace/skills
cp -R obsidian-daily-recap-skill ~/.openclaw/workspace/skills/obsidian-daily-recap
```

Then restart OpenClaw / start a new chat session.

---

## ⚙️ Requirements

- Python 3.9+
- Chatlog files in markdown format

You can configure paths by flags **or env vars**:

- `RECAP_CHATLOG_DIR`
- `RECAP_OUT_DIR`

Defaults (author environment):

- Chatlog dir: `/Users/mac/.openclaw/workspace/memory/chatlog/telegram-6404111657`
- Output dir: `/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/BossmanVault/KnowledgeInbox`

---

## 🧪 Usage

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

### 5) Using env vars

```bash
export RECAP_CHATLOG_DIR=/path/to/chatlogs
export RECAP_OUT_DIR=/path/to/KnowledgeInbox
python3 scripts/build_recap.py --date 2026-03-19
```

---

## 📁 Repository structure

```text
.
├── SKILL.md
├── obsidian-daily-recap.skill
└── scripts/
    └── build_recap.py
```

---

## 🏷️ Output naming

Generated file name:

```text
YYYY-MM-DD-对话知识点.md
```

---

## 🛠️ Repackage `.skill`

```bash
python3 /Users/mac/Library/pnpm/global/5/.pnpm/openclaw@2026.3.8_@napi-rs+canvas@0.1.96_@types+express@5.0.6_hono@4.12.7_node-llama-cpp@3.16.2/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py .
```

Then ensure distributable file name is `obsidian-daily-recap.skill`.

---

## 🔐 Privacy note

This repo only contains skill logic and package files.

- ❌ No personal chatlogs
- ❌ No vault content
- ✅ Safe to publish as open-source template
