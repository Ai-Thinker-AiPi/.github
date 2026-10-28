#!/usr/bin/env python3
"""生成组织主页的鱼骨时间线（浅色 / 深色两张 SVG）。

用法：
    1. 编辑同目录下的 timeline.json，按年份顺序追加 {"year", "title", "lines"}
    2. 运行：python3 build_timeline.py
    3. 提交生成的 timeline-light.svg / timeline-dark.svg

版式规则：骨刺沿脊线左右交替，年份自动均分；条目变多时卡片会自动收窄。
"""
import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Inter, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif"

W, H = 1000, 420
SPINE_Y = 210
SPINE_X0, SPINE_X1 = 56, 936
NODE_X0, MAX_SPAN = 170, 640
CARD_H = 104

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


def load():
    with open(os.path.join(HERE, "timeline.json"), encoding="utf-8") as f:
        data = json.load(f)
    items = data["milestones"]
    for it in items:
        if len(it.get("lines", [])) > 2:
            raise ValueError(f'{it["year"]}: lines 最多两行')
    return items


def build(theme, items):
    t = THEMES[theme]
    n = len(items)
    spacing = min(200, MAX_SPAN / (n - 1)) if n > 1 else 0
    card_w = min(190, 2 * spacing - 16) if n > 1 else 190

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="AiPi 小安派团队发展鱼骨时间线">',
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
        cx = nx + 52
        above = i % 2 == 0
        top = 48 if above else 268
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
            f'<text x="{card_x+16:.1f}" y="{top+36}" font-family="{FONT}" font-size="24" '
            f'font-weight="700" fill="{accent}">{escape(it["year"])}</text>',
            f'<text x="{card_x+16+len(it["year"])*13.5+10:.1f}" y="{top+35}" '
            f'font-family="{FONT}" font-size="14.5" font-weight="600" '
            f'fill="{t["text"]}">{escape(it["title"])}</text>',
        ]
        for j, line in enumerate(it["lines"]):
            out.append(
                f'<text x="{card_x+16:.1f}" y="{top+66+j*21}" font-family="{FONT}" '
                f'font-size="13" fill="{t["sub"]}">{escape(line)}</text>'
            )

    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    items = load()
    for theme in THEMES:
        path = os.path.join(HERE, f"timeline-{theme}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(theme, items))
        print("wrote", path)


if __name__ == "__main__":
    main()
