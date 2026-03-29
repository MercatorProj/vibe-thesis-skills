## 示例 1：基础单列 + 分支

遵循 SKILL 中的**绘制规范**与**美观要点**（无重叠、端口偏移、圆角线条、清新学术配色）。下例采用统一风格：节点 `#F1F5F9`、描边 `#475569`、连线 `#64748B`、圆角线条。

下列输入为**某类「环境建模 → 决策 → 调度」链条的示意**；其他学科请将节点文案替换为你的术语（路径占位见仓库根 [README.md](../../../README.md)）。

输入（示意）：

```text
标题：端到端求解流程
方向：vertical
节点：
- start: 开始 (start)
- a: 环境/约束建模\n(状态或可行域) (process)
- b: 核心规划步骤\n(目标与代价) (process)
- c: 是否满足终止条件？ (decision)
- d: 中间结果整合 (process)
- e: 上层决策或调度 (process)
- end: 结束 (end)
连线：
- start -> a
- a -> b
- b -> c
- c(是) -> d
- d -> e
- e -> end
- c(否) -> end
```

输出（SVG 样例，可直接粘贴查看；样式与 `render_flowchart.py` 及 SKILL 输出模板一致）：

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 900 760">
  <defs>
    <style>
      .node { fill:#F1F5F9; stroke:#475569; stroke-width:1.5; }
      .node-decision { fill:#F3F5F8; stroke:#475569; stroke-width:1.5; }
      .label { fill:#1E293B; font-size:14px; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }
      .title { fill:#1E293B; font-size:16px; font-weight:600; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }
      .edge { fill:none; stroke:#64748B; stroke-width:1.5; stroke-linecap:round; stroke-linejoin:round; }
      .edge-label { fill:#475569; font-size:12px; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748B"/>
    </marker>
  </defs>

  <text class="title" x="450" y="44" text-anchor="middle">端到端求解流程</text>

  <!-- Edges (drawn first to avoid overlapping text) -->
  <path class="edge" d="M 450 120 L 450 170" marker-end="url(#arrow)"/>
  <path class="edge" d="M 450 226 L 450 276" marker-end="url(#arrow)"/>
  <path class="edge" d="M 450 332 L 450 362" marker-end="url(#arrow)"/>
  <path class="edge" d="M 450 430 L 450 452" marker-end="url(#arrow)"/>
  <path class="edge" d="M 450 430 L 290 430 L 290 642 L 450 642" marker-end="url(#arrow)"/>
  <text class="edge-label" x="462" y="448">是</text>
  <text class="edge-label" x="300" y="422">否</text>
  <path class="edge" d="M 450 508 L 450 558" marker-end="url(#arrow)"/>
  <path class="edge" d="M 450 614 L 450 664" marker-end="url(#arrow)"/>

  <!-- Nodes -->
  <rect class="node" x="290" y="80" width="320" height="56" rx="28" ry="28"/>
  <text class="label" x="450" y="114" text-anchor="middle">开始</text>
  <rect class="node" x="290" y="170" width="320" height="56" rx="12" ry="12"/>
  <text class="label" x="450" y="196" text-anchor="middle">
    <tspan x="450" dy="0">环境/约束建模</tspan>
    <tspan x="450" dy="18">(状态或可行域)</tspan>
  </text>
  <rect class="node" x="290" y="276" width="320" height="56" rx="12" ry="12"/>
  <text class="label" x="450" y="302" text-anchor="middle">
    <tspan x="450" dy="0">核心规划步骤</tspan>
    <tspan x="450" dy="18">(目标与代价)</tspan>
  </text>
  <polygon class="node-decision" points="450,362 530,402 450,442 370,402"/>
  <text class="label" x="450" y="407" text-anchor="middle">满足终止条件？</text>
  <rect class="node" x="290" y="452" width="320" height="56" rx="12" ry="12"/>
  <text class="label" x="450" y="486" text-anchor="middle">中间结果整合</text>
  <rect class="node" x="290" y="558" width="320" height="56" rx="12" ry="12"/>
  <text class="label" x="450" y="592" text-anchor="middle">上层决策或调度</text>
  <rect class="node" x="290" y="664" width="320" height="56" rx="28" ry="28"/>
  <text class="label" x="450" y="698" text-anchor="middle">结束</text>
</svg>
```

### 多列分组示例（脚本生成）

多列、分组框、端口偏移等建议使用 `render_flowchart.py` 生成；若项目中有现成 `*.spec.json` 与对应 SVG，可作为版式参考。默认保存目录为 `{{THESIS_DIR}}/figures/flows/`（见仓库根 [README.md](../../../README.md)）。脚本输出与上文一致的清新学术配色与圆角线条。

