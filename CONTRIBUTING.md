# Contributing

Thanks for contributing to `obsidian-daily-recap-skill`.

## Development flow

1. Fork this repo
2. Create a branch (`feat/...` or `fix/...`)
3. Make changes
4. Run a quick local test:

```bash
python3 scripts/build_recap.py --date 2026-03-19 --chatlog-dir ./sample-chatlog --out-dir ./out
```

5. Repackage skill file (if SKILL.md or scripts changed):

```bash
python3 /Users/mac/Library/pnpm/global/5/.pnpm/openclaw@2026.3.8_@napi-rs+canvas@0.1.96_@types+express@5.0.6_hono@4.12.7_node-llama-cpp@3.16.2/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py .
```

6. Ensure `obsidian-daily-recap.skill` is updated
7. Open a PR

## Commit convention

Recommended prefixes:

- `feat:` new feature
- `fix:` bug fix
- `docs:` docs change
- `refactor:` code cleanup with no behavior change

## Scope

Please keep this repo focused on:

- Skill definition (`SKILL.md`)
- Recap builder script (`scripts/build_recap.py`)
- Skill package (`obsidian-daily-recap.skill`)

Avoid committing personal chatlogs or private vault files.
