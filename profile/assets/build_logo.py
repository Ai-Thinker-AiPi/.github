#!/usr/bin/env python3
"""生成标题左侧的 AiPi logo（浅色 / 深色两版）。

源文件 logo-aipi-source.png 是黑字白底、四周留白很大的方图，直接用会让
logo 缩成一条细缝；脚本会把留白裁掉，并把白底转成透明，这样：

- logo-aipi-light.png：黑色字形 + 透明底，浅色主题下用
- logo-aipi-dark.png ：白色字形 + 透明底，深色主题下用

README 里用 <picture> 按 prefers-color-scheme 切换两版。
换源文件或改尺寸后运行：python3 build_logo.py
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "logo-aipi-source.png")

OUT_HEIGHT = 360          # 输出高度：README 里按 120px 显示，360 够 3 倍屏
PAD = 0                   # 裁剪后额外留白（px，按输出尺寸算）
INVERT_ALPHA = False      # 源图若是白字黑底，改成 True


def load_alpha():
    """读源图，返回 (alpha, size)：alpha 255=字形，0=背景。"""
    im = Image.open(SRC).convert("L")
    alpha = im.point(lambda v: v if INVERT_ALPHA else 255 - v)
    box = alpha.getbbox()
    if not box:
        raise ValueError("源图是纯色，找不到 logo 内容")
    return alpha.crop(box), box


def save(alpha, color, name):
    w, h = alpha.size
    new_h = OUT_HEIGHT
    new_w = max(1, round(w * new_h / h))
    a = alpha.resize((new_w, new_h), Image.LANCZOS)
    rgba = Image.new("RGBA", (new_w, new_h), color + (0,))
    rgba.putalpha(a)
    if PAD:
        canvas = Image.new("RGBA", (new_w + 2 * PAD, new_h + 2 * PAD), (0, 0, 0, 0))
        canvas.alpha_composite(rgba, (PAD, PAD))
        rgba = canvas
    path = os.path.join(HERE, name)
    rgba.save(path, optimize=True)
    print("wrote", path, rgba.size)


def main():
    alpha, box = load_alpha()
    print("源内容 bbox", box, "裁剪后", alpha.size)
    save(alpha, (0, 0, 0), "logo-aipi-light.png")
    save(alpha, (255, 255, 255), "logo-aipi-dark.png")


if __name__ == "__main__":
    main()
