#!/usr/bin/env python3
"""生成组织主页的鱼骨时间线（中 / 英 × 浅色 / 深色 四张 SVG）。

用法：
    1. 编辑 timeline.json（中文）或 timeline.en.json（英文），按年份顺序追加
       {"year": "2027", "title": "主题", "lines": ["第一行", "第二行"]}
    2. 运行：python3 build_timeline.py
    3. 提交生成的 timeline-*.svg / timeline-en-*.svg

版式规则：骨刺沿脊线左右交替，年份自动均分；每行文字手动控制换行，
脚本会检查行宽是否超出卡片，超出会直接报错。
"""
import json
import os
import unicodedata
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Inter, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif"

W = 880
CARD_W = 300
PAD = 14
DESC_SIZE = 14
LINE_H = 21
GAP = 30
NODE_X0, SPACING = 150, 160
SPINE_X0, SPINE_X1 = 44, 840
MAX_LINES = 6

THEMES = {
    "light": dict(
        bg="#f6f8fa", border="#d8dee4", line="#c9d1d9", text="#1f2328", sub="#57606a",
        accents=["#2f5d8a", "#2f6b57", "#7a5a24", "#4b3f7a"], fill_opacity="0.05",
        stroke_opacity="0.30",
    ),
    "dark": dict(
        bg="#161b22", border="#30363d", line="#3d444d", text="#e6edf3", sub="#8b949e",
        accents=["#6ea8d8", "#5fb89a", "#d8b45f", "#a08fd8"], fill_opacity="0.10",
        stroke_opacity="0.40",
    ),
}

LOCALES = {
    "zh": dict(data="timeline.json", suffix="", aria="AiPi 小安派团队发展鱼骨时间线"),
    "en": dict(data="timeline.en.json", suffix="-en", aria="AiPi team milestone timeline"),
}


def char_em(ch):
    """粗略字宽：中日韩全宽字符按 1em，拉丁字符按 0.55em。"""
    return 1.0 if unicodedata.east_asian_width(ch) in ("W", "F", "A") else 0.55


def text_width(s, size):
    return sum(char_em(c) for c in s) * size


def load(locale):
    path = os.path.join(HERE, LOCALES[locale]["data"])
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = data["milestones"]
    limit = CARD_W - 2 * PAD
    for it in items:
        lines = it.get("lines", [])
        if not 1 <= len(lines) <= MAX_LINES:
            raise ValueError(f'{it["year"]}: lines 需要 1~{MAX_LINES} 行')
        for line in lines:
            w = text_width(line, DESC_SIZE)
            if w > limit:
                raise ValueError(
                    f'{it["year"]}: 「{line}」宽 {w:.0f}px，超出 {limit}px，请拆成两行')
    return items


def build(theme, items, aria):
    t = THEMES[theme]
    n = len(items)
    spacing = min(SPACING, (SPINE_X1 - SPINE_X0 - 2 * 46) / (n - 1)) if n > 1 else 0
    max_lines = max(len(it["lines"]) for it in items)
    card_h = 66 + (max_lines - 1) * LINE_H + 16
    spine_y = GAP + card_h + 18
    h = spine_y + GAP + card_h + 18

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
        f'viewBox="0 0 {W} {h}" role="img" '
        f'aria-label="{aria}">',
        f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="20" '
        f'fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<line x1="{SPINE_X0}" y1="{spine_y}" x2="{SPINE_X1-16}" y2="{spine_y}" '
        f'stroke="{t["line"]}" stroke-width="2.5" stroke-linecap="round"/>',
        f'<path d="M{SPINE_X1-16} {spine_y-8} L{SPINE_X1} {spine_y} '
        f'L{SPINE_X1-16} {spine_y+8} Z" fill="{t["line"]}"/>',
    ]

    for i, it in enumerate(items):
        accent = t["accents"][i % len(t["accents"])]
        nx = NODE_X0 + i * spacing
        cx = nx + 46
        above = i % 2 == 0
        top = spine_y - GAP - card_h if above else spine_y + GAP
        card_x = cx - CARD_W / 2
        rib_end_y = top + card_h if above else top

        out += [
            f'<line x1="{nx:.1f}" y1="{spine_y}" x2="{cx:.1f}" y2="{rib_end_y}" '
            f'stroke="{accent}" stroke-opacity="0.45" stroke-width="1.8" stroke-linecap="round"/>',
            f'<circle cx="{nx:.1f}" cy="{spine_y}" r="12" fill="{accent}" fill-opacity="0.12"/>',
            f'<circle cx="{nx:.1f}" cy="{spine_y}" r="5.5" fill="{accent}"/>',
            f'<rect x="{card_x:.1f}" y="{top}" width="{CARD_W}" height="{card_h}" rx="12" '
            f'fill="{accent}" fill-opacity="{t["fill_opacity"]}" stroke="{accent}" '
            f'stroke-opacity="{t["stroke_opacity"]}"/>',
            f'<text x="{card_x+PAD:.1f}" y="{top+34}" font-family="{FONT}" font-size="30" '
            f'font-weight="700" fill="{accent}">{escape(it["year"])}</text>',
            f'<text x="{card_x+PAD+len(it["year"])*16.5+10:.1f}" y="{top+33}" '
            f'font-family="{FONT}" font-size="17" font-weight="600" '
            f'fill="{t["text"]}">{escape(it["title"])}</text>',
        ]
        for j, line in enumerate(it["lines"]):
            out.append(
                f'<text x="{card_x+PAD:.1f}" y="{top+66+j*LINE_H}" font-family="{FONT}" '
                f'font-size="{DESC_SIZE}" fill="{t["sub"]}">{escape(line)}</text>'
            )

    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    for locale, cfg in LOCALES.items():
        items = load(locale)
        for theme in THEMES:
            path = os.path.join(HERE, f"timeline{cfg['suffix']}-{theme}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(build(theme, items, cfg["aria"]))
            print("wrote", path)


if __name__ == "__main__":
    main()
