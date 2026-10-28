#!/usr/bin/env python3
"""生成组织主页的鱼骨时间线（中 / 英 × 浅色 / 深色 四张 SVG）。

用法：
    1. 编辑 timeline.json（中文）或 timeline.en.json（英文），按年份顺序追加
       {"year": "2027", "title": "主题", "lines": ["第一行", "第二行"]}
    2. 运行：python3 build_timeline.py
    3. 提交生成的 timeline-*.svg / timeline-en-*.svg

版式规则：骨刺沿脊线左右交替，年份自动均分；每行文字手动控制换行，
脚本会检查行宽是否超出卡片，超出会直接报错。
中文标题与年份同行（短标题），英文标题独立成行（标题较长）。
"""
import json
import os
import unicodedata
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Inter, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif"

GAP = 30
PAD = 14
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
    "zh": dict(
        data="timeline.json", suffix="", aria="AiPi 小安派团队发展鱼骨时间线",
        w=880, card_w=300, node_x0=150, spacing=160, spine=(44, 840),
        title_inline=True, title_size=17, desc_size=14, line_h=21, desc_top=66,
    ),
    "en": dict(
        data="timeline.en.json", suffix="-en", aria="AiPi team milestone timeline",
        w=940, card_w=336, node_x0=150, spacing=180, spine=(44, 900),
        title_inline=False, title_size=14, desc_size=14, line_h=20, desc_top=84,
    ),
}


def char_em(ch):
    """粗略字宽：中日韩全宽字符按 1em，拉丁字符按 0.55em。"""
    return 1.0 if unicodedata.east_asian_width(ch) in ("W", "F", "A") else 0.55


def text_width(s, size):
    return sum(char_em(c) for c in s) * size


def load(locale):
    cfg = LOCALES[locale]
    with open(os.path.join(HERE, cfg["data"]), encoding="utf-8") as f:
        data = json.load(f)
    items = data["milestones"]
    limit = cfg["card_w"] - 2 * PAD
    for it in items:
        lines = it.get("lines", [])
        if not 1 <= len(lines) <= MAX_LINES:
            raise ValueError(f'{it["year"]}: lines 需要 1~{MAX_LINES} 行')
        for line in lines:
            w = text_width(line, cfg["desc_size"])
            if w > limit:
                raise ValueError(
                    f'{it["year"]}: 「{line}」宽 {w:.0f}px，超出 {limit}px，请拆成两行')
        tw = text_width(it["title"], cfg["title_size"])
        if cfg["title_inline"]:
            tw += text_width(it["year"], 30)
            tw += 10  # 标题左边距
        if tw > limit:
            raise ValueError(f'{it["year"]}: 标题「{it["title"]}」过宽')
    return items


def build(theme, items, cfg):
    t = THEMES[theme]
    n = len(items)
    spine_x0, spine_x1 = cfg["spine"]
    spacing = min(cfg["spacing"], (spine_x1 - spine_x0 - 2 * 46) / (n - 1)) if n > 1 else 0
    max_lines = max(len(it["lines"]) for it in items)
    card_h = cfg["desc_top"] + (max_lines - 1) * cfg["line_h"] + 16
    spine_y = GAP + card_h + 18
    h = spine_y + GAP + card_h + 18
    w = cfg["w"]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="{cfg["aria"]}">',
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" '
        f'fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<line x1="{spine_x0}" y1="{spine_y}" x2="{spine_x1-16}" y2="{spine_y}" '
        f'stroke="{t["line"]}" stroke-width="2.5" stroke-linecap="round"/>',
        f'<path d="M{spine_x1-16} {spine_y-8} L{spine_x1} {spine_y} '
        f'L{spine_x1-16} {spine_y+8} Z" fill="{t["line"]}"/>',
    ]

    for i, it in enumerate(items):
        accent = t["accents"][i % len(t["accents"])]
        nx = cfg["node_x0"] + i * spacing
        cx = nx + 46
        above = i % 2 == 0
        top = spine_y - GAP - card_h if above else spine_y + GAP
        card_x = cx - cfg["card_w"] / 2
        rib_end_y = top + card_h if above else top

        out += [
            f'<line x1="{nx:.1f}" y1="{spine_y}" x2="{cx:.1f}" y2="{rib_end_y}" '
            f'stroke="{accent}" stroke-opacity="0.45" stroke-width="1.8" stroke-linecap="round"/>',
            f'<circle cx="{nx:.1f}" cy="{spine_y}" r="12" fill="{accent}" fill-opacity="0.12"/>',
            f'<circle cx="{nx:.1f}" cy="{spine_y}" r="5.5" fill="{accent}"/>',
            f'<rect x="{card_x:.1f}" y="{top}" width="{cfg["card_w"]}" height="{card_h}" rx="12" '
            f'fill="{accent}" fill-opacity="{t["fill_opacity"]}" stroke="{accent}" '
            f'stroke-opacity="{t["stroke_opacity"]}"/>',
        ]
        if cfg["title_inline"]:
            out += [
                f'<text x="{card_x+PAD:.1f}" y="{top+34}" font-family="{FONT}" font-size="30" '
                f'font-weight="700" fill="{accent}">{escape(it["year"])}</text>',
                f'<text x="{card_x+PAD+len(it["year"])*16.5+10:.1f}" y="{top+33}" '
                f'font-family="{FONT}" font-size="{cfg["title_size"]}" font-weight="600" '
                f'fill="{t["text"]}">{escape(it["title"])}</text>',
            ]
        else:
            out += [
                f'<text x="{card_x+PAD:.1f}" y="{top+38}" font-family="{FONT}" font-size="30" '
                f'font-weight="700" fill="{accent}">{escape(it["year"])}</text>',
                f'<text x="{card_x+PAD:.1f}" y="{top+64}" font-family="{FONT}" '
                f'font-size="{cfg["title_size"]}" font-weight="700" '
                f'fill="{t["text"]}">{escape(it["title"])}</text>',
            ]
        for j, line in enumerate(it["lines"]):
            out.append(
                f'<text x="{card_x+PAD:.1f}" y="{top+cfg["desc_top"]+j*cfg["line_h"]}" '
                f'font-family="{FONT}" font-size="{cfg["desc_size"]}" '
                f'fill="{t["sub"]}">{escape(line)}</text>'
            )

    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    for locale, cfg in LOCALES.items():
        items = load(locale)
        for theme in THEMES:
            path = os.path.join(HERE, f"timeline{cfg['suffix']}-{theme}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(build(theme, items, cfg))
            print("wrote", path)


if __name__ == "__main__":
    main()
