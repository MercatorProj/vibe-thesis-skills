---
name: academic-writing
description: 学术写作一体化技能，含两种模式。(1) 格式化/润色：段落级学术润色、术语统一、公式规范化、逻辑优化，输出到草稿目录；(2) 人味化：中英文人味化改写、减弱模板化表述，可选检测脚本。对论文正文进行润色或改写时，**默认应用 humanizer-zh 风格规则**。默认输出目录见仓库根 README.md；学术诚信见 DISTRIBUTION.md。
---

# 学术写作技能（格式化润色 + 人味化）

输出路径默认值见仓库根目录 [README.md](../../../README.md)（`{{DRAFT_DIR}}`，默认 `my-thesis/`）。**学术诚信与正当使用**见 [DISTRIBUTION.md](../../../DISTRIBUTION.md)。

## 模式选择

| 模式 | 适用场景 | 输出 |
|------|----------|------|
| **格式化/润色** | 「润色这段」「改写成学术段落」「术语统一」「公式规范」 | 规范学术段落，保存为 `my-thesis/第X章_主题_年月日.md` |
| **人味化** | 「降 AI 味」「人味化」「去 AI 痕迹」「改写得更自然」 | 工学/运筹风格改写，可选运行 ai_detector/text_analyzer，保存到 my-thesis |

根据用户表述选择模式；未明确时，若用户给的是草稿段落且要求“润色/规范”，走格式化/润色；若强调“人味/自然/去 AI”，走人味化。

---

## 一、格式化/润色模式

### 核心要点

- **段落级润色**：输出可直接插入论文的连续文本段落，不含 Markdown 标题（#、##）。
- **每次输出 MD 文件**：命名 `第X章_主题_年月日.md`，保存到工作目录 `my-thesis/`。
- **学术风格**：符合学位论文规范，术语见 [references/terminology.md](references/terminology.md)，公式见 [references/formula-templates.md](references/formula-templates.md)。
- **人类写作倾向**：适当长短句、多样过渡（鉴于此、反观之）、学术限定（在多数情况下、现有证据表明），避免“首先、其次、最后”式模板与典型 AI 句式。
- **默认 humanizer-zh 自检**：输出前对段落做一次去 AI 痕迹自检，对照 [references/humanizer-zh-patterns.md](references/humanizer-zh-patterns.md)（删除填充短语、打破公式结构、变化节奏、信任读者、删除金句；用快速检查清单扫一遍）。

### 工作流程

1. 接收草稿段落或技术要点  
2. 语义分析，识别章节归属与润色需求  
3. 术语规范化（查阅 terminology.md）、公式规范化（查阅 formula-templates.md）、逻辑优化  
4. **humanizer-zh 自检**：按 [references/humanizer-zh-patterns.md](references/humanizer-zh-patterns.md) 快速检查清单过一遍，修正 AI 痕迹  
5. 输出纯段落 Markdown 并保存到 `my-thesis/`

详细步骤与示例见 [references/workflow.md](references/workflow.md)。

### 论文章节适配

- 第3章：通行性分析（车辆动力性、土壤力学、通行性量化）  
- 第4章：路径规划（A*、启发函数、代价函数）  
- 第5章：运输调度（VRP/PDP、数学模型、优化方法）  
- 第6章：实验验证（实验设计、结果分析、性能对比）

---

## 二、人味化模式（工学/运筹中英文）

### 学术诚信

- 目的：提升基于本人研究与想法、经 AI 辅助起草后的文本的自然度与学术感。  
- 正当使用：在本人观点基础上修订 AI 起草文本；不提交不能代表本人智力贡献的内容。  
- 原则：真实学术表达，而非规避检测。

### 工作流

1. **分析文本**：可选运行 `scripts/ai_detector.py`（`--lang zh` 或 `en`），检测句长均匀度、机械过渡词、抽象套话、词汇多样性等。  
2. **应用改写策略**：**先**按 [references/humanizer-zh-patterns.md](references/humanizer-zh-patterns.md) 的模式与 5 条核心规则做一遍去痕迹与自然化，**再**叠加本技能的工学/运筹术语与 [references/rewriting-principles.md](references/rewriting-principles.md)（句子节奏、减少抽象脚手架、消除机械过渡、学术语气与限定、落到具体性）；术语与 [references/terminology.md](references/terminology.md)、[references/engineering-patterns.md](references/engineering-patterns.md) 对齐。  
3. **改写并说明**：中文可附【修改说明】3–5 条；默认保存到 `my-thesis/`，命名同格式化模式。

### 学科规范摘要

- 通行性：VCI/CI、沉陷、坡度、地质灾害风险等，表述可量化。  
- 路径规划：A*、启发函数、代价函数、栅格地图等。  
- 车辆调度：CVRP、PDP、容量约束、时间窗等。  
- 实验与仿真：基准算法、对比实验、MAE/RMSE、计算时间等。

详见 [references/engineering-patterns.md](references/engineering-patterns.md)、[references/rewriting-examples.md](references/rewriting-examples.md)。

### 脚本与工具

- **ai_detector.py**：AI 写作模式检测，`python scripts/ai_detector.py input.txt --lang zh`（或 `en`），支持 `--detailed`、`--json`。  
- **text_analyzer.py**：句长分布、TTR、过渡词密度等，`python scripts/text_analyzer.py input.txt`，或 `original.txt revised.txt --compare`。  
- 中文可选依赖：`jieba`（见 `scripts/requirements.txt`）。

### 自检清单（人味化后）

- [ ] 句长有变化（短/中/长结合）  
- [ ] 机械过渡词已减少或替换  
- [ ] 抽象套话已替换为具体概念或术语  
- [ ] 至少一处具体方法/参数/场景或学术限定  
- [ ] 原意与引用、数据完整保留  
- [ ] 学科用语符合工学/运筹习惯  
- [ ] **humanizer-zh**：无连续三句同长、破折号不过多、无三段式堆砌、连接词（此外/然而等）未堆砌；已按 [references/humanizer-zh-patterns.md](references/humanizer-zh-patterns.md) 快速检查清单自检

---

## 输出约定（两模式通用）

- 润色/改写结果**必须**输出到 `my-thesis/`，命名格式 `第X章_主题_年月日.md`。  
- 不改变原意与关键数据、引用；不捏造文献或数据。

---

## 参考文档

- [references/terminology.md](references/terminology.md)：术语标准化  
- [references/formula-templates.md](references/formula-templates.md)：公式模板  
- [references/workflow.md](references/workflow.md)：格式化润色流程与示例  
- [references/rewriting-principles.md](references/rewriting-principles.md)：人味化改写原则（工学/运筹）
- [references/engineering-patterns.md](references/engineering-patterns.md)：工学/运筹用语与写作惯例
- [references/rewriting-examples.md](references/rewriting-examples.md)：人味化 before/after 示例
- [references/formatting-examples.md](references/formatting-examples.md)：格式化润色示例（可选）
- [references/humanizer-zh-patterns.md](references/humanizer-zh-patterns.md)：**默认去 AI 痕迹与人味化规则**（论文润色与审查共用）
- [references/humanizer-inspiration.md](references/humanizer-inspiration.md)：人味化与 AI 痕迹检测增强参考（推荐 Pass 顺序、检测层次、检查清单、速查表；执行改写或 Part C 时查阅）
