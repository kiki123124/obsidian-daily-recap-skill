---
name: obsidian-daily-recap
description: Generate daily conversation knowledge recaps from Telegram chatlog files into Obsidian KnowledgeInbox. Use when user asks to summarize yesterday/all past chats, backfill missing recap files, or produce structured recap docs with sections: 结论/例子/可复用做法/TODO and 3 明日复盘问题.
---

# Obsidian Daily Recap

Build recap markdown files from chatlog files and write them into Obsidian vault.

## Workflow

1. Confirm source and output paths:
   - Source: `/Users/mac/.openclaw/workspace/memory/chatlog/telegram-6404111657/YYYY-MM-DD.md`
   - Output: `/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/BossmanVault/KnowledgeInbox/YYYY-MM-DD-对话知识点.md`
2. Run script:
   - Yesterday (default):
     - `python3 scripts/build_recap.py`
   - Specific date:
     - `python3 scripts/build_recap.py --date 2026-03-10`
   - Backfill all existing chatlogs:
     - `python3 scripts/build_recap.py --all`
3. Verify files exist in `KnowledgeInbox/`.
4. If user asks "all conversations", also create one range summary file manually after backfill (e.g., `YYYY-MM-DD_to_YYYY-MM-DD-总复盘.md`).

## Rules

- Keep output in Chinese.
- Group by topic when possible.
- Each item must include:
  - 结论
  - 例子（如有）
  - 可复用做法
  - 待办(TODO)
- End with exactly 3 条“明日复盘问题”.
- If source log missing, write a short placeholder and explicitly mention missing chatlog path.

## GitHub upload checklist (when requested)

1. Ensure git repo and remote exist.
2. Commit skill files only:
   - `.agents/skills/obsidian-daily-recap/SKILL.md`
   - `.agents/skills/obsidian-daily-recap/scripts/build_recap.py`
3. Push to user-specified branch/repo.
4. If no remote/auth, ask for repo URL + token/SSH access.
