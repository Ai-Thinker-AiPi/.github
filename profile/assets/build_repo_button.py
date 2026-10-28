#!/usr/bin/env python3
"""生成「GitHub 主仓库」跳转按钮（中文 / 英文两张 SVG，内嵌安信可 logo）。

用深色胶囊样式：浅色和深色主题下都清晰可读，因此 README 里直接
<a><img></a> 即可，不需要 <picture>（GitHub 会把包住 <picture> 的链接吃掉）。

修改按钮文字或尺寸后运行：python3 build_repo_button.py
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Inter, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif"

W, H = 440, 72

STYLE = dict(fill="#24292f", stroke="#4a5560", text="#ffffff", sub="#a6b0bb")

# 文件名 -> 副标题（英文页面用 repo-button-en.svg）
LABELS = {
    "repo-button.svg": "GitHub 主仓库",
    "repo-button-en.svg": "Main GitHub Repository",
}


def build(logo_b64, sub):
    t = STYLE
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="安信可科技 GitHub 主仓库">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{t['fill']}" stroke="{t['stroke']}"/>
<image x="22" y="19" width="34" height="34" href="data:image/png;base64,{logo_b64}"/>
<text x="70" y="33" font-family="{FONT}" font-size="17" font-weight="700" fill="{t['text']}">安信可科技 · Ai-Thinker</text>
<text x="70" y="53" font-family="{FONT}" font-size="13" fill="{t['sub']}">{sub}</text>
<path d="M404 30 L416 36 L404 42" fill="none" stroke="{t['sub']}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def main():
    with open(os.path.join(HERE, "logo-mark.png"), "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    for name, sub in LABELS.items():
        path = os.path.join(HERE, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(logo_b64, sub))
        print("wrote", path)


if __name__ == "__main__":
    main()
