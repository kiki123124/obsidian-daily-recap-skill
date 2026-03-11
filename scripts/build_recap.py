#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

SH_TZ = dt.timezone(dt.timedelta(hours=8))


def parse_sections(md: str):
    sections = {}
    current = "未分类"
    buf = []
    for line in md.splitlines():
        if line.startswith("## "):
            if buf:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if buf:
        sections[current] = "\n".join(buf).strip()
    return sections


def topic_guess(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["cron", "定时", "reminder", "daily"]):
        return "自动化与定时任务"
    if any(k in t for k in ["obsidian", "knowledge", "总结", "复盘"]):
        return "知识管理"
    if any(k in t for k in ["openclaw", "gateway", "模型", "oauth", "codex"]):
        return "OpenClaw 运维与模型"
    if any(k in t for k in ["交易所", "活动", "four.meme", "bnb", "发币", "crypto"]):
        return "加密与市场动作"
    return "其他"


def make_daily_recap(chatlog: Path, out_file: Path, date_str: str):
    content = chatlog.read_text(encoding="utf-8")
    sections = parse_sections(content)

    grouped = {}
    for title, body in sections.items():
        if title in ["占位", "未分类"] and len(body.strip()) < 20:
            continue
        topic = topic_guess(title + "\n" + body)
        grouped.setdefault(topic, []).append((title, body))

    lines = [f"# {date_str}-对话知识点", ""]
    if not grouped:
        lines += [
            "> ⚠️ 当天日志为占位/内容不足，无法提炼高质量知识点。",
            "",
            "## 主题：记录机制",
            "- 结论：当天未形成结构化 chatlog。",
            "- 例子：仅有占位记录。",
            "- 可复用做法：按“决策/链接/TODO/风险”记录每日要点。",
            "- 待办(TODO)：补写当天关键决策与下一步。",
            "",
            "## 明日复盘问题（3）",
            "1) 今天最关键的 1 个决策是什么？",
            "2) 有哪些结论值得沉淀成 SOP？",
            "3) 明天最小可交付动作是什么？",
            "",
        ]
    else:
        for topic, items in grouped.items():
            lines += [f"## 主题：{topic}", ""]
            for title, body in items:
                one = re.sub(r"\s+", " ", body).strip()
                example = one[:140] + ("…" if len(one) > 140 else "")
                lines += [
                    f"### {title}",
                    "- 结论：见本条要点，已纳入当日主题。",
                    f"- 例子：{example if example else '（无）'}",
                    "- 可复用做法：把该场景抽象为步骤/模板，下次直接复用。",
                    "- 待办(TODO)：补充可量化结果与下一步动作。",
                    "",
                ]

        lines += [
            "## 明日复盘问题（3）",
            "1) 今天的高价值输出里，哪一条最值得标准化？",
            "2) 哪个任务的反馈闭环还没打通？",
            "3) 明天优先推进哪一件事，最小交付是什么？",
            "",
        ]

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(lines), encoding="utf-8")


def daterange(start: dt.date, end: dt.date):
    d = start
    while d <= end:
        yield d
        d += dt.timedelta(days=1)


def main():
    p = argparse.ArgumentParser(description="Build Obsidian daily recap from telegram chatlog")
    p.add_argument("--date", help="YYYY-MM-DD")
    p.add_argument("--all", action="store_true", help="Process all available chatlog dates")
    p.add_argument(
        "--chatlog-dir",
        default="/Users/mac/.openclaw/workspace/memory/chatlog/telegram-6404111657",
    )
    p.add_argument(
        "--out-dir",
        default="/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/BossmanVault/KnowledgeInbox",
    )
    args = p.parse_args()

    chatlog_dir = Path(args.chatlog_dir)
    out_dir = Path(args.out_dir)

    dates = []
    if args.all:
        for f in sorted(chatlog_dir.glob("*.md")):
            try:
                dt.date.fromisoformat(f.stem)
                dates.append(f.stem)
            except ValueError:
                continue
    else:
        if args.date:
            dates = [args.date]
        else:
            yesterday = (dt.datetime.now(SH_TZ).date() - dt.timedelta(days=1)).isoformat()
            dates = [yesterday]

    for d in dates:
        chatlog = chatlog_dir / f"{d}.md"
        out_file = out_dir / f"{d}-对话知识点.md"
        if not chatlog.exists():
            out_file.write_text(
                f"# {d}-对话知识点\n\n> ⚠️ 未找到日志文件：`{chatlog}`\n> 请先开始记录 chatlog。\n",
                encoding="utf-8",
            )
            continue
        make_daily_recap(chatlog, out_file, d)

    print(f"done: {len(dates)} day(s)")


if __name__ == "__main__":
    main()
