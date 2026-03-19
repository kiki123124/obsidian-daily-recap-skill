#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

SH_TZ = dt.timezone(dt.timedelta(hours=8))


TOPIC_RULES = [
    ("自动化与定时任务", ["cron", "定时", "reminder", "daily", "自愈", "重启", "job"]),
    ("知识管理与复盘", ["obsidian", "knowledge", "总结", "复盘", "知识点", "日报"]),
    ("OpenClaw 运维与模型", ["openclaw", "gateway", "模型", "oauth", "codex", "telegram", "配置", "doctor"]),
    ("学习与语言", ["西语", "spanish", "ielts", "单词", "语音", "跟读", "发音"]),
    ("加密与市场动作", ["交易所", "活动", "four.meme", "bnb", "发币", "crypto", "usdc", "盘口"]),
]


def parse_sections(md: str) -> list[tuple[str, str]]:
    """Split markdown by level-2 headings. Return [(title, body), ...]."""
    sections: list[tuple[str, str]] = []
    current = "未分类"
    buf: list[str] = []

    for line in md.splitlines():
        if line.startswith("## "):
            body = "\n".join(buf).strip()
            if body:
                sections.append((current, body))
            current = line[3:].strip() or "未命名"
            buf = []
        else:
            buf.append(line)

    tail = "\n".join(buf).strip()
    if tail:
        sections.append((current, tail))
    return sections


def topic_guess(text: str) -> str:
    t = text.lower()
    for topic, keys in TOPIC_RULES:
        if any(k in t for k in keys):
            return topic
    return "其他"


def clean_line(line: str) -> str:
    line = re.sub(r"^\s*[-*]\s*", "", line.strip())
    line = re.sub(r"\s+", " ", line)
    return line


def extract_signal(body: str) -> tuple[str, str, str]:
    """Return (conclusion, example, todo) inferred from content."""
    lines = [clean_line(x) for x in body.splitlines() if clean_line(x)]
    if not lines:
        return (
            "该条记录信息较少，保留为待补充条目。",
            "（无）",
            "补充关键上下文、决策与结果。",
        )

    # Prefer explicit markers if present.
    conclusion = next((x for x in lines if any(m in x for m in ["结论", "决定", "最终", "已确认"])) , lines[0])
    todo = next((x for x in lines if any(m in x.lower() for m in ["todo", "待办", "下一步", "follow-up", "跟进"])) , "将此主题沉淀为可复用 checklist，并安排下次检查。")

    example = "（无）"
    for x in lines:
        if x == conclusion:
            continue
        if "http" in x or any(m in x for m in ["例如", "比如", "案例", "示例", "问题", "报错", "输出"]):
            example = x
            break

    if example == "（无）":
        merged = "；".join(lines[:2])
        example = merged[:140] + ("…" if len(merged) > 140 else "")

    return conclusion, example, todo


def compact(text: str, max_len: int = 140) -> str:
    s = re.sub(r"\s+", " ", text).strip()
    return s[:max_len] + ("…" if len(s) > max_len else "")


def make_daily_recap(chatlog: Path, out_file: Path, date_str: str):
    content = chatlog.read_text(encoding="utf-8")
    section_items = parse_sections(content)

    grouped: dict[str, list[tuple[str, str]]] = {}
    for title, body in section_items:
        body_trim = body.strip()
        if title in ["占位", "未分类"] and len(body_trim) < 20:
            continue
        topic = topic_guess(title + "\n" + body_trim)
        grouped.setdefault(topic, []).append((title, body_trim))

    lines: list[str] = [f"# {date_str}-对话知识点", ""]

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
        total_items = sum(len(v) for v in grouped.values())
        lines += [f"> 共提炼 {total_items} 条记录，按主题聚合如下：", ""]

        for topic, items in grouped.items():
            lines += [f"## 主题：{topic}", ""]
            for idx, (title, body) in enumerate(items, start=1):
                conclusion, example, todo = extract_signal(body)
                reusable = "将该场景抽象为『触发条件 → 执行动作 → 验证标准 → 回执模板』并写入固定流程。"
                lines += [
                    f"### {idx}. {compact(title, 60)}",
                    f"- 结论：{compact(conclusion, 180)}",
                    f"- 例子：{compact(example, 180)}",
                    f"- 可复用做法：{reusable}",
                    f"- 待办(TODO)：{compact(todo, 180)}",
                    "",
                ]

        lines += [
            "## 明日复盘问题（3）",
            "1) 今天哪一条动作最值得沉淀成模板并长期复用？",
            "2) 哪个任务还缺『完成定义（DoD）』，导致推进效率低？",
            "3) 明天优先推进哪一件事，最小可交付是什么？",
            "",
        ]

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(lines), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description="Build Obsidian daily recap from Telegram chatlogs")
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

    if args.all:
        dates = []
        for f in sorted(chatlog_dir.glob("*.md")):
            try:
                dt.date.fromisoformat(f.stem)
                dates.append(f.stem)
            except ValueError:
                continue
    elif args.date:
        dates = [args.date]
    else:
        dates = [(dt.datetime.now(SH_TZ).date() - dt.timedelta(days=1)).isoformat()]

    for d in dates:
        chatlog = chatlog_dir / f"{d}.md"
        out_file = out_dir / f"{d}-对话知识点.md"
        if not chatlog.exists():
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(
                "\n".join(
                    [
                        f"# {d}-对话知识点",
                        "",
                        f"> ⚠️ 未找到日志文件：`{chatlog}`",
                        "> 昨日日志缺失，需要开始/恢复记录。",
                        "",
                        "## 主题：日志缺失处理",
                        "- 结论：当天无法从原始对话提炼知识点。",
                        "- 例子：源 chatlog 文件不存在。",
                        "- 可复用做法：每天固定时段检查日志文件是否生成。",
                        "- 待办(TODO)：修复 chatlog 记录链路并补录关键决策。",
                        "",
                        "## 明日复盘问题（3）",
                        "1) 日志为什么缺失，在哪个环节断了？",
                        "2) 如何给日志记录增加自动告警？",
                        "3) 明天先补哪 3 条关键决策？",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            continue
        make_daily_recap(chatlog, out_file, d)

    print(f"done: {len(dates)} day(s)")


if __name__ == "__main__":
    main()
