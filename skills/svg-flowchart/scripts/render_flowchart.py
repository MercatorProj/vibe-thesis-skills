import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def encode_entities(text: str) -> str:
    """Encode non-ascii chars to numeric entities to avoid encoding issues."""
    out = []
    for ch in text:
        if ord(ch) > 127:
            out.append(f"&#x{ord(ch):X};")
        else:
            out.append(ch)
    return "".join(out)


def split_lines(label: str, max_chars: int = 16) -> List[str]:
    if "\n" in label:
        return [s.strip() for s in label.split("\n") if s.strip()]
    s = label.strip()
    if len(s) <= max_chars:
        return [s]
    # naive wrap: keep ASCII words together, wrap CJK by chars
    lines: List[str] = []
    buf = ""
    for token in s.split(" "):
        if not buf:
            buf = token
        elif len(buf) + 1 + len(token) <= max_chars:
            buf = f"{buf} {token}"
        else:
            lines.append(buf)
            buf = token
    if buf:
        # if still too long (CJK without spaces), hard cut
        while len(buf) > max_chars:
            lines.append(buf[:max_chars])
            buf = buf[max_chars:]
        if buf:
            lines.append(buf)
    return lines


def measure_node_height(lines: List[str], base_h: int = 44, line_gap: int = 18) -> int:
    return max(base_h, 28 + len(lines) * line_gap)


@dataclass
class Node:
    id: str
    label: str
    type: str = "process"
    group: Optional[str] = None


@dataclass
class Edge:
    src: str
    dst: str
    label: Optional[str] = None


@dataclass
class Group:
    id: str
    title: str
    col: int


def render_svg(spec: dict) -> str:
    # Layout defaults (academic + fresh)
    W = int(spec.get("width", 1200))
    pad = int(spec.get("pad", 28))
    col_gap = int(spec.get("col_gap", 78))
    gap_y = int(spec.get("gap_y", 42))
    node_w = int(spec.get("node_w", 280))
    rx = int(spec.get("rx", 12))

    nodes = [Node(**n) for n in spec["nodes"]]
    edges = [Edge(**e) for e in spec.get("edges", [])]
    groups = [Group(**g) for g in spec.get("groups", [])]
    group_by_id: Dict[str, Group] = {g.id: g for g in groups}

    # Determine columns
    cols = max((g.col for g in groups), default=0) + 1
    col_xs = [pad + i * (node_w + col_gap) for i in range(cols)]

    # Order nodes in each column by spec.order if provided, else as they appear
    order_map: Dict[str, int] = {nid: i for i, nid in enumerate(spec.get("order", []))}
    def node_sort_key(n: Node) -> Tuple[int, int]:
        col = group_by_id.get(n.group).col if n.group in group_by_id else 0
        return (col, order_map.get(n.id, 10_000))

    nodes_sorted = sorted(nodes, key=node_sort_key)

    # Assign vertical positions per column
    col_items: Dict[int, List[Node]] = {i: [] for i in range(cols)}
    for n in nodes_sorted:
        col = group_by_id.get(n.group).col if n.group in group_by_id else 0
        col_items[col].append(n)

    node_pos: Dict[str, Tuple[int, int, int, int, List[str]]] = {}
    col_heights: Dict[int, int] = {}
    for c in range(cols):
        y = pad + 44  # reserve title space inside group box
        for n in col_items[c]:
            lines = split_lines(n.label, max_chars=int(spec.get("wrap", 16)))
            h = measure_node_height(lines)
            x = col_xs[c]
            node_pos[n.id] = (x, y, node_w, h, lines)
            y += h + gap_y
        col_heights[c] = y

    H = max(col_heights.values(), default=pad) + pad

    # Incoming edge offsets (ports)
    incoming: Dict[str, List[str]] = {}
    for e in edges:
        incoming.setdefault(e.dst, []).append(e.src)
    port_offset: Dict[Tuple[str, str], int] = {}
    for dst, srcs in incoming.items():
        if len(srcs) == 1:
            port_offset[(srcs[0], dst)] = 0
        elif len(srcs) == 2:
            port_offset[(srcs[0], dst)] = -10
            port_offset[(srcs[1], dst)] = +10
        else:
            # spread evenly
            spread = 22
            mid = (len(srcs) - 1) / 2.0
            for i, s in enumerate(srcs):
                port_offset[(s, dst)] = int(round((i - mid) * spread))

    # Outgoing offsets (avoid overlapping edges from same node)
    outgoing: Dict[str, List[str]] = {}
    for e in edges:
        outgoing.setdefault(e.src, []).append(e.dst)
    out_offset: Dict[Tuple[str, str], int] = {}
    for src, dsts in outgoing.items():
        if len(dsts) == 1:
            out_offset[(src, dsts[0])] = 0
        elif len(dsts) == 2:
            out_offset[(src, dsts[0])] = -12
            out_offset[(src, dsts[1])] = +12
        else:
            spread = 24
            mid = (len(dsts) - 1) / 2.0
            for i, d in enumerate(dsts):
                out_offset[(src, d)] = int(round((i - mid) * spread))

    def same_col(a: str, b: str) -> bool:
        return node_pos[a][0] == node_pos[b][0]

    def node_anchor_bottom(nid: str, dst: str) -> Tuple[int, int]:
        x, y, w, h, _ = node_pos[nid]
        dx = out_offset.get((nid, dst), 0)
        return (x + w // 2 + dx, y + h)

    def node_anchor_top(nid: str, src: str) -> Tuple[int, int]:
        x, y, w, _h, _ = node_pos[nid]
        dx = port_offset.get((src, nid), 0) // 2
        return (x + w // 2 + dx, y)

    def node_anchor_right(nid: str, dst: str) -> Tuple[int, int]:
        x, y, w, h, _ = node_pos[nid]
        dy = out_offset.get((nid, dst), 0)
        return (x + w, y + h // 2 + dy)

    def node_anchor_left(nid: str, src: str) -> Tuple[int, int]:
        x, y, _w, h, _ = node_pos[nid]
        dy = port_offset.get((src, nid), 0)
        return (x, y + h // 2 + dy)

    def vertical_detour_needed(src: str, dst: str) -> bool:
        if not same_col(src, dst):
            return False
        sx, sy, _sw, sh, _ = node_pos[src]
        _dx, dy, _dw, _dh, _ = node_pos[dst]
        if dy <= sy:
            return False
        y0 = sy + sh
        y1 = dy
        for nid, (x, y, _w, h, _lines) in node_pos.items():
            if nid in (src, dst):
                continue
            if x != sx:
                continue
            if y >= y0 and (y + h) <= y1:
                return True
        return False

    # Group boxes bounds (generous padding to avoid overlap)
    group_bounds: Dict[str, Tuple[int, int, int, int]] = {}
    group_pad = 26
    for g in groups:
        xs, ys, xe, ye = [], [], [], []
        for n in nodes:
            if n.group != g.id:
                continue
            x, y, w, h, _ = node_pos[n.id]
            xs.append(x)
            ys.append(y)
            xe.append(x + w)
            ye.append(y + h)
        if not xs:
            continue
        x0 = min(xs) - group_pad
        y0 = min(ys) - 34  # title area
        x1 = max(xe) + group_pad
        y1 = max(ye) + group_pad
        group_bounds[g.id] = (x0, y0, x1 - x0, y1 - y0)

    # SVG header (academic + fresh style)
    svg: List[str] = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {W} {H}">')
    svg.append("  <defs>")
    svg.append("    <style>")
    svg.append("      .node { fill:#F1F5F9; stroke:#475569; stroke-width:1.5; }")
    svg.append("      .label { fill:#1E293B; font-size:14px; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }")
    svg.append("      .label-sub { fill:#64748B; font-size:12px; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }")
    svg.append("      .edge { fill:none; stroke:#64748B; stroke-width:1.5; stroke-linecap:round; stroke-linejoin:round; }")
    svg.append("      .group { fill:#F8FAFC; stroke:#E2E8F0; stroke-width:1.2; }")
    svg.append("      .group-title { fill:#475569; font-size:13px; font-weight:600; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }")
    svg.append("    </style>")
    svg.append('    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">')
    svg.append('      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748B"/>')
    svg.append("    </marker>")
    svg.append("  </defs>")

    # Groups
    svg.append("")
    svg.append("  <!-- Groups -->")
    for g in groups:
        if g.id not in group_bounds:
            continue
        x, y, w, h = group_bounds[g.id]
        svg.append(f'  <rect class="group" x="{x}" y="{y}" width="{w}" height="{h}" rx="16" ry="16"/>')
        svg.append(f'  <text class="group-title" x="{x+16}" y="{y+22}">{encode_entities(g.title)}</text>')

    # Edges
    svg.append("")
    svg.append("  <!-- Edges -->")
    for e in edges:
        if same_col(e.src, e.dst):
            x1, y1 = node_anchor_bottom(e.src, e.dst)
            x2, y2 = node_anchor_top(e.dst, e.src)
            if vertical_detour_needed(e.src, e.dst):
                detour = 28
                x3 = min(x1, x2) - detour
                d = f"M {x1} {y1} L {x3} {y1} L {x3} {y2} L {x2} {y2}"
            else:
                d = f"M {x1} {y1} L {x2} {y2}"
            elbow_x = (x1 + x2) // 2
        else:
            x1, y1 = node_anchor_right(e.src, e.dst)
            x2, y2 = node_anchor_left(e.dst, e.src)
            elbow_x = (x1 + x2) // 2
            d = f"M {x1} {y1} L {elbow_x} {y1} L {elbow_x} {y2} L {x2} {y2}"
        svg.append(f'  <path class="edge" d="{d}" marker-end="url(#arrow)"/>')
        if e.label:
            svg.append(f'  <text class="label-sub" x="{elbow_x+6}" y="{y2-6}">{encode_entities(e.label)}</text>')

    # Nodes
    svg.append("")
    svg.append("  <!-- Nodes -->")
    for n in nodes_sorted:
        x, y, w, h, lines = node_pos[n.id]
        svg.append(f'  <rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}"/>')
        cx = x + w // 2
        # center vertically
        line_gap = 18
        start_y = y + h // 2 - (len(lines)-1) * line_gap / 2 + 5
        svg.append(f'  <text class="label" x="{cx}" y="{int(start_y)}" text-anchor="middle">')
        for i, line in enumerate(lines):
            dy = 0 if i == 0 else line_gap
            if "_" in line and any(tok in line for tok in ("v_max", "τ_ij", "tau_ij")):
                parts = line.split(" ")
                segs: List[str] = []
                for p in parts:
                    if p == "v_max":
                        segs.append('v<tspan baseline-shift="sub" font-size="11">max</tspan>')
                    elif p in ("τ_ij", "tau_ij"):
                        segs.append('&#x03C4;<tspan baseline-shift="sub" font-size="11">ij</tspan>')
                    else:
                        segs.append(encode_entities(p))
                inner = " ".join(segs)
                svg.append(f'    <tspan x="{cx}" dy="{dy}">{inner}</tspan>')
            else:
                svg.append(f'    <tspan x="{cx}" dy="{dy}">{encode_entities(line)}</tspan>')
        svg.append("  </text>")

    svg.append("</svg>")
    svg.append("")
    return "\n".join(svg)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="Path to JSON spec file")
    ap.add_argument("--out", required=True, help="Output SVG path")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    out_path = Path(args.out)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    svg = render_svg(spec)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

