#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# SVG → PDF 转换脚本（供 LaTeX 使用）
# 优先尝试 cairosvg；若无则提示使用 Inkscape 命令行。
# 用法: python svg2pdf.py <input.svg> [output.pdf]
# ---------------------------------------------------------------------------
from pathlib import Path
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python svg2pdf.py <input.svg> [output.pdf]", file=sys.stderr)
        print("  未指定 output 时，生成与 input 同名的 .pdf", file=sys.stderr)
        sys.exit(1)

    src = Path(sys.argv[1]).resolve()
    if not src.exists():
        print(f"错误: 文件不存在: {src}", file=sys.stderr)
        sys.exit(1)
    if src.suffix.lower() != ".svg":
        print("警告: 输入建议为 .svg 文件", file=sys.stderr)

    if len(sys.argv) >= 3:
        dest = Path(sys.argv[2]).resolve()
    else:
        dest = src.with_suffix(".pdf")

    dest.parent.mkdir(parents=True, exist_ok=True)

    # 优先使用 cairosvg（需 pip install cairosvg；Windows 上可能缺 cairo 库）
    try:
        import cairosvg
        cairosvg.svg2pdf(url=str(src), write_to=str(dest))
        print(f"已生成: {dest}")
        return
    except ImportError:
        pass
    except Exception as e:
        print(f"cairosvg 转换失败: {e}", file=sys.stderr)

    # 未安装 cairosvg 或转换失败时，提示 Inkscape
    print("未安装 cairosvg 或转换失败。请任选其一：", file=sys.stderr)
    print("  1. 安装 cairosvg: pip install cairosvg（Windows 可能需额外安装 cairo 运行库）", file=sys.stderr)
    print("  2. 使用 Inkscape 命令行：", file=sys.stderr)
    print(f'     inkscape --export-type=pdf "{src}" -o "{dest}"', file=sys.stderr)
    print("  3. 用 Inkscape / 浏览器打开 SVG 后另存为 PDF", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
