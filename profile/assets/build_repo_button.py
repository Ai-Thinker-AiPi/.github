#!/usr/bin/env python3
"""生成「GitHub 主仓库」跳转按钮（浅色 / 深色两张 SVG，内嵌安信可 logo）。

修改按钮文字或尺寸后运行：python3 build_repo_button.py
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Inter, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif"

W, H = 440, 72

THEMES = {
    "light": dict(fill="#ffffff", stroke="#d0d7de", text="#1f2328", sub="#57606a"),
    "dark": dict(fill="#21262d", stroke="#30363d", text="#e6edf3", sub="#8b949e"),
}


def build(theme, logo_b64):
    t = THEMES[theme]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="安信可科技 GitHub 主仓库">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{t['fill']}" stroke="{t['stroke']}"/>
<image x="22" y="19" width="34" height="34" href="data:image/png;base64,{logo_b64}"/>
<text x="70" y="33" font-family="{FONT}" font-size="17" font-weight="700" fill="{t['text']}">安信可科技 · Ai-Thinker</text>
<text x="70" y="53" font-family="{FONT}" font-size="13" fill="{t['sub']}">GitHub 主仓库</text>
<path d="M404 30 L416 36 L404 42" fill="none" stroke="{t['sub']}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def main():
    with open(os.path.join(HERE, "logo-mark.png"), "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    for theme in THEMES:
        path = os.path.join(HERE, f"repo-button-{theme}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(theme, logo_b64))
        print("wrote", path)


if __name__ == "__main__":
    main()
