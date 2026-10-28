#!/usr/bin/env python3
"""生成中英文切换小卡片（中文 / English 各两张：选中态、未选中态）。

选中态用品牌蓝实心，未选中态用深灰底浅字，浅色、深色页面下都清晰。
修改后运行：python3 build_lang_switch.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Inter, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif"

W, H = 96, 34

ACTIVE = dict(fill="#2f5d8a", stroke="#2f5d8a", text="#ffffff", weight="700")
IDLE = dict(fill="#30363d", stroke="#4a5560", text="#c9d1d9", weight="600")


def build(label, active):
    t = ACTIVE if active else IDLE
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{t['fill']}" stroke="{t['stroke']}"/>
<text x="{W/2}" y="22" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="{t['weight']}" fill="{t['text']}">{label}</text>
</svg>
"""


def main():
    for slug, label in (("zh", "中文"), ("en", "English")):
        for active in (True, False):
            name = f"lang-{slug}{'-active' if active else ''}.svg"
            path = os.path.join(HERE, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(build(label, active))
            print("wrote", path)


if __name__ == "__main__":
    main()
