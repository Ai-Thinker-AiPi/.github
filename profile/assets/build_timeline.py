#!/usr/bin/env python3
"""生成组织主页的鱼骨时间线（中 / 英 × 浅色 / 深色 四张 SVG）。

用法：
    1. 编辑 timeline.json（中文）或 timeline.en.json（英文），按年份顺序追加
       {"year", "title", "lines"}
    2. 运行：python3 build_timeline.py
    3. 提交生成的 timeline-*.svg / timeline-en-*.svg

版式规则：骨刺沿脊线左右交替，年份自动均分；条目变多时卡片会自动收窄。
"""
import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Inter, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif"

W, H = 880, 332
SPINE_Y = 166
SPINE_X0, SPINE_X1 = 44, 840
NODE_X0, MAX_SPAN = 150, 480
CARD_H, GAP = 104, 34

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
    "zh": dict(data="timeline.json", suffix="", max_lines=2, desc_size=15,
               aria="AiPi 小安派团队发展鱼骨时间线"),
    "en": dict(data="timeline.en.json", suffix="-en", max_lines=2, desc_size=13.5,
               aria="AiPi team milestone timeline"),
}


def load(locale):
    with open(os.path.join(HERE, LOCALES[locale]["data"]), encoding="utf-8") as f:
        data = json.load(f)
    items = data["milestones"]
    for it in items:
        if len(it.get("lines", [])) > LOCALES[locale]["max_lines"]:
            raise ValueError(f'{it["year"]}: lines 超出上限')
    return items


def build(theme, items, aria, desc_size=15):
    t = THEMES[theme]
    n = len(items)
    spacing = min(160, MAX_SPAN / (n - 1)) if n > 1 else 0
    card_w = min(200, 2 * spacing - 16) if n > 1 else 200

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="{aria}">',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" '
        f'fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<line x1="{SPINE_X0}" y1="{SPINE_Y}" x2="{SPINE_X1-16}" y2="{SPINE_Y}" '
        f'stroke="{t["line"]}" stroke-width="2.5" stroke-linecap="round"/>',
        f'<path d="M{SPINE_X1-16} {SPINE_Y-8} L{SPINE_X1} {SPINE_Y} '
        f'L{SPINE_X1-16} {SPINE_Y+8} Z" fill="{t["line"]}"/>',
    ]

    for i, it in enumerate(items):
        accent = t["accents"][i % len(t["accents"])]
        nx = NODE_X0 + i * spacing
        cx = nx + 46
        above = i % 2 == 0
        top = SPINE_Y - GAP - CARD_H if above else SPINE_Y + GAP
        card_x = cx - card_w / 2
        rib_end_y = top + CARD_H if above else top

        out += [
            f'<line x1="{nx:.1f}" y1="{SPINE_Y}" x2="{cx:.1f}" y2="{rib_end_y}" '
            f'stroke="{accent}" stroke-opacity="0.45" stroke-width="1.8" stroke-linecap="round"/>',
            f'<circle cx="{nx:.1f}" cy="{SPINE_Y}" r="12" fill="{accent}" fill-opacity="0.12"/>',
            f'<circle cx="{nx:.1f}" cy="{SPINE_Y}" r="5.5" fill="{accent}"/>',
            f'<rect x="{card_x:.1f}" y="{top}" width="{card_w:.1f}" height="{CARD_H}" rx="12" '
            f'fill="{accent}" fill-opacity="{t["fill_opacity"]}" stroke="{accent}" '
            f'stroke-opacity="{t["stroke_opacity"]}"/>',
            f'<text x="{card_x+14:.1f}" y="{top+34}" font-family="{FONT}" font-size="30" '
            f'font-weight="700" fill="{accent}">{escape(it["year"])}</text>',
            f'<text x="{card_x+14+len(it["year"])*16.5+10:.1f}" y="{top+33}" '
            f'font-family="{FONT}" font-size="17" font-weight="600" '
            f'fill="{t["text"]}">{escape(it["title"])}</text>',
        ]
        for j, line in enumerate(it["lines"]):
            out.append(
                f'<text x="{card_x+14:.1f}" y="{top+66+j*22}" font-family="{FONT}" '
                f'font-size="{desc_size}" fill="{t["sub"]}">{escape(line)}</text>'
            )

    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    for locale, cfg in LOCALES.items():
        items = load(locale)
        for theme in THEMES:
            path = os.path.join(HERE, f"timeline{cfg['suffix']}-{theme}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(build(theme, items, cfg["aria"], cfg["desc_size"]))
            print("wrote", path)


if __name__ == "__main__":
    main()
