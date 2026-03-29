#!/usr/bin/env python3
"""
SVG 流程图样式检测脚本（与 svg-flowchart 技能规范一致）.
检测项：配色、线条圆角、viewBox、字体、禁止项（渐变/阴影等）.
支持灰色系与清新淡雅淡彩色；允许的配色见 SKILL.md「配色与字体」与下方 ALLOWED_* 集合。

用法：python validate_flowchart_style.py [--strict] <file.svg> [<file2.svg> ...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# 技能规范中的允许值（小写，不含 #）；含灰色系与清新淡彩
ALLOWED_NODE_FILLS = {
    # 灰色系
    "f1f5f9", "f7f8fa", "f3f5f8", "f8fafc", "f4f6f8", "e8eef7", "e8f4f0", "dbeafe", "c7d2fe", "fff8e8", "e8f7f4",
    # 淡蓝 / 淡青
    "e0f2fe", "bae6fd", "cffafe", "a5f3fc", "f0f9ff",
    # 淡绿
    "dcfce7", "bbf7d0", "d1fae5",
    # 淡紫
    "ede9fe", "ddd6fe", "e0e7ff",
    # 淡杏/橙
    "ffedd5", "fed7aa", "fef9c3", "fef3c7",
}
ALLOWED_NODE_STROKES = {
    # 灰色
    "475569", "2f3a45", "374151", "4b5563",
    # 蓝/青
    "0ea5e9", "0284c7", "0891b2", "0e7490", "7dd3fc", "4f46e5",
    # 绿
    "16a34a", "15803d", "047857",
    # 紫
    "7c3aed", "6d28d9",
    # 橙
    "ea580c", "c2410c", "a16207",
}
ALLOWED_EDGE_STROKES = {
    "64748b", "94a3b8", "5b7280", "6b7280", "2f3a45",
    "0ea5e9", "0284c7", "7dd3fc", "16a34a", "7c3aed", "ea580c", "0891b2",
}
ALLOWED_LABEL_FILLS = {"1e293b", "111827", "374151", "475569", "4b5563", "6b7280", "64748b", "0369a1"}
ALLOWED_GROUP_FILL = {"f8fafc", "f4f6f8", "f0f9ff", "e0f2fe", "ecfdf5", "f5f3ff", "fff7ed"}
ALLOWED_GROUP_STROKE = {"e2e8f0", "9ca3af", "7dd3fc", "bae6fd", "a7f3d0", "c4b5fd", "fed7aa"}
ALLOWED_MARKER_FILL = {"64748b", "94a3b8", "2f3a45", "0ea5e9", "0284c7", "7dd3fc", "16a34a", "7c3aed", "ea580c", "0891b2"}

RE_COLOR = re.compile(r"#([0-9a-fA-F]{6})\b")
RE_STYLE_BLOCK = re.compile(r"<style[^>]*>([\s\S]*?)</style>")
RE_STROKE_LINECAP = re.compile(r"stroke-linecap\s*:\s*(\S+)")
RE_STROKE_LINEJOIN = re.compile(r"stroke-linejoin\s*:\s*(\S+)")
RE_VIEWBOX = re.compile(r'viewBox\s*=\s*["\']?\s*([0-9.eE+\-\s]+)\s*["\']?')
RE_WIDTH = re.compile(r'<svg[^>]*\bwidth\s*=\s*["\']([^"\']+)["\']')
RE_FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;}]+)")
RE_MARKER_PATH_FILL = re.compile(r"<marker[\s\S]*?<path[^>]*\bfill\s*=\s*[\"']#?([0-9a-fA-F]{6})[\"']")
RE_GRADIENT = re.compile(r"<linearGradient|<radialGradient|<defs[^>]*>[\s\S]*?gradient")
RE_FILTER_SHADOW = re.compile(r"filter\s*:\s*|drop-shadow|box-shadow")


def normalize_hex(s: str) -> str:
    return s.lower().replace("#", "").strip()[:6]


def extract_style_rules(css: str) -> List[Tuple[str, str]]:
    """从 CSS 中提取 选择器 { 属性: 值 } 的简化列表（按规则块）."""
    rules: List[Tuple[str, str]] = []
    for block in re.finditer(r"([.#\w\-]+)\s*\{([^}]*)\}", css):
        selector, body = block.group(1).strip(), block.group(2)
        rules.append((selector, body))
    return rules


def _get_prop_value(body: str, prop: str) -> List[str]:
    """在 CSS body 中取 prop 对应的值（支持多个，如 fill 与 stroke）。"""
    out: List[str] = []
    for m in re.finditer(rf"{re.escape(prop)}\s*:\s*#([0-9a-fA-F]{{6}})\b", body):
        out.append(normalize_hex(m.group(1)))
    return out


def check_svg(path: Path, strict: bool) -> List[str]:
    errors: List[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [f"无法读取文件: {e}"]

    # 1. viewBox
    m = RE_VIEWBOX.search(text)
    if not m:
        errors.append("缺少 viewBox")
    else:
        parts = m.group(1).split()
        if len(parts) < 4:
            errors.append("viewBox 格式应为 '0 0 W H'")

    # 2. width 可缩放
    w = RE_WIDTH.search(text)
    if w and "100%" not in w.group(1) and "%" not in w.group(1):
        errors.append("建议根 <svg> width 为 100% 以支持缩放")

    # 3. <style> 内规范
    style_match = RE_STYLE_BLOCK.search(text)
    if not style_match:
        errors.append("未找到 <style> 块")
    else:
        css = style_match.group(1)
        rules = extract_style_rules(css)

        for selector, body in rules:
            selector_lower = selector.lower()
            if "node" in selector_lower and "group" not in selector_lower:
                for h in _get_prop_value(body, "fill"):
                    if h not in ALLOWED_NODE_FILLS:
                        errors.append(f"[{selector}] 节点填充色 #{h} 不在规范允许列表中")
                for h in _get_prop_value(body, "stroke"):
                    if h not in ALLOWED_NODE_STROKES:
                        errors.append(f"[{selector}] 节点描边 #{h} 不在规范允许列表中")

            if "edge" in selector_lower and "label" not in selector_lower:
                for h in _get_prop_value(body, "stroke"):
                    if h not in ALLOWED_EDGE_STROKES:
                        errors.append(f"[{selector}] 连线颜色 #{h} 不在规范允许列表中")
                if "stroke-linecap" in body:
                    cap = RE_STROKE_LINECAP.search(body)
                    if cap and "round" not in cap.group(1).lower():
                        errors.append(f"[{selector}] 连线应为 stroke-linecap:round")
                else:
                    errors.append(f"[{selector}] 连线缺少 stroke-linecap:round")
                if "stroke-linejoin" in body:
                    join = RE_STROKE_LINEJOIN.search(body)
                    if join and "round" not in join.group(1).lower():
                        errors.append(f"[{selector}] 连线应为 stroke-linejoin:round")
                else:
                    errors.append(f"[{selector}] 连线缺少 stroke-linejoin:round")

            if "group" in selector_lower and "title" not in selector_lower:
                for h in _get_prop_value(body, "fill"):
                    if h not in ALLOWED_GROUP_FILL:
                        errors.append(f"[{selector}] 分组框填充 #{h} 建议为 #F8FAFC")
                for h in _get_prop_value(body, "stroke"):
                    if h not in ALLOWED_GROUP_STROKE:
                        errors.append(f"[{selector}] 分组框描边 #{h} 建议为 #E2E8F0")

            if "label" in selector_lower or "title" in selector_lower:
                for h in _get_prop_value(body, "fill"):
                    if h not in ALLOWED_LABEL_FILLS:
                        errors.append(f"[{selector}] 文字颜色 #{h} 不在规范允许列表中")

        # 全局：是否包含中文字体
        if "Microsoft YaHei" not in css and "PingFang" not in css and "font-family" in css:
            errors.append("字体栈中建议包含 Microsoft YaHei 或 PingFang SC")

    # 4. marker 箭头填充
    for m in RE_MARKER_PATH_FILL.finditer(text):
        h = normalize_hex(m.group(1))
        if h not in ALLOWED_MARKER_FILL:
            errors.append(f"marker 箭头填充 #{h} 建议为 #64748B")

    # 5. 禁止项
    if RE_GRADIENT.search(text):
        errors.append("不建议使用 linearGradient/radialGradient，保持纯色")
    if strict and RE_FILTER_SHADOW.search(text):
        errors.append("不建议使用 filter/drop-shadow/box-shadow")

    return errors


def main() -> None:
    ap = argparse.ArgumentParser(description="SVG 流程图样式规范检测（svg-flowchart 技能）")
    ap.add_argument("files", nargs="+", type=Path, help="待检测的 .svg 文件")
    ap.add_argument("--strict", action="store_true", help="严格模式：禁止阴影/滤镜")
    args = ap.parse_args()

    exit_code = 0
    for path in args.files:
        if not path.exists():
            print(f"{path}: 文件不存在", file=sys.stderr)
            exit_code = 1
            continue
        errs = check_svg(path, args.strict)
        if not errs:
            print(f"{path}: OK")
        else:
            exit_code = 1
            print(f"{path}: {len(errs)} 项不符合规范")
            for e in errs:
                print(f"  - {e}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
