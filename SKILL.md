---
name: obsidian-daily-recap
description: Generate structured daily recap notes from Telegram chatlogs into Obsidian KnowledgeInbox, including grouped topics and fixed fields (结论/例子/可复用做法/TODO) plus 3 明日复盘问题. Use when user asks to summarize yesterday chats, backfill missing days, fix recap quality, or produce long-range recap files for self-review.
---

# Obsidian Daily Recap

Generate daily recap markdown files from chatlogs and write them into Obsidian vault.

## Runbook

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
3. Verify generated files exist in `KnowledgeInbox/`.
4. If user asks for a long-range summary (e.g., “这周/这个月总复盘”), run `--all` first, then generate one extra merged recap file manually.

## Output Constraints

- Keep output in Chinese.
- Group by topic.
- Every item must include:
  - 结论
  - 例子（如有）
  - 可复用做法
  - 待办(TODO)
- End with exactly 3 条“明日复盘问题”.
- If source log missing, still create placeholder recap and explicitly mention missing path.

## Quality Rules

- Prefer actionability over narrative.
- Avoid generic conclusions; include concrete signals from chatlog body.
- Keep each field concise and reusable.
- Preserve links if found in source text.

## GitHub Publish (when requested)

1. Validate skill locally (run the script once).
2. Package skill:
   - `python3 /Users/mac/Library/pnpm/global/5/.pnpm/openclaw@2026.3.8_@napi-rs+canvas@0.1.96_@types+express@5.0.6_hono@4.12.7_node-llama-cpp@3.16.2/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py /Users/mac/.openclaw/workspace/github/obsidian-daily-recap-skill`
3. Commit changed files:
   - `SKILL.md`
   - `scripts/build_recap.py`
   - `obsidian-daily-recap.skill`
4. Push to user repo/branch.
5. Report commit hash + release file name.
