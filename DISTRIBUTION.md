# 学术技能包：分发与合规说明

本文档说明本仓库内 **`.opencode/skills/`** 技能的许可状况、再分发限制与学术诚信使用约定。随包分发时请保留本文件及各技能目录下的 `LICENSE.txt`（如有）。

## 第三方技能许可摘要

| 技能目录 | 许可文件 | 再分发与使用要点 |
|----------|----------|------------------|
| `pdf/` | [`.opencode/skills/pdf/LICENSE.txt`](.opencode/skills/pdf/LICENSE.txt) | **Anthropic 专有条款**：限制从服务中提取材料、复制、衍生、向第三方分发等。公开再分发或商用打包前**必须**自行对照全文条款与 [Anthropic 服务条款](https://www.anthropic.com/legal/consumer-terms)；若条款不允许对外分发，应从分发包中**排除**该技能或引导用户从官方渠道单独获取。 |
| `docx/` | [`.opencode/skills/docx/LICENSE.txt`](.opencode/skills/docx/LICENSE.txt) | 同上（与 `pdf` 相同结构的 Anthropic 附加限制）。 |
| `mcp-builder/` | [`.opencode/skills/mcp-builder/LICENSE.txt`](.opencode/skills/mcp-builder/LICENSE.txt) | **Apache License 2.0**：允许再分发；需保留许可副本、NOTICE（如有）、修改声明等，详见许可证第四节。 |
| `skill-creator/` | [`.opencode/skills/skill-creator/LICENSE.txt`](.opencode/skills/skill-creator/LICENSE.txt) | **Apache License 2.0**：同上。 |

其余未单独列出 `LICENSE.txt` 的技能，视为本仓库维护内容；对外分发时仍建议保留作者说明并遵守适用平台（如 Cursor、OpenCode）的开源/使用政策。

## 路径与课题无关性

仓库内默认目录名（如 `论文章节/`、`my-thesis/`）与占位符约定见根目录 [README.md](README.md)。分发通用技能包时，应要求使用者按自身项目替换 `{{THESIS_DIR}}` 等占位符。

## 学术诚信与「人味化 / 去 AI 痕迹」类能力

以下技能涉及写作风格润色、可读性提升或「减弱模板化表述」：**`academic-writing`**、**`thesis-reviewer`**（含 Part C 等）。

**正当用途包括**：提高中文/英文学术表达的清晰度与一致性；减少口语化与冗余；使符号、术语与结构符合学位论文或期刊规范。

**不得将此类能力用于**：规避所在院校或期刊的学术诚信政策；在禁止使用生成式辅助的提交场景中隐瞒工具使用；伪造或掩盖未经验证的研究贡献。

使用者有责任遵守本单位学术规范与出版方政策。技能说明中的「人味化」「去 AI 痕迹」仅指**文风与结构层面的编辑**，不表示可代替原创研究与诚实披露。

## 文档索引

- 路径占位符与环境变量：[README.md](README.md)
- 文献多源检索与合并：`.opencode/skills/literature/references/multi-source-retrieval.md`
- 非 Zotero / Word 书目说明：`.opencode/skills/literature/references/non-zotero-bibliography.md`
- 系统综述与 PRISMA 轻量工作流：`systematic-review-lite/SKILL.md`（方法学以 [PRISMA 官网](http://www.prisma-statement.org/) 为准，非法律或医学建议）
- 跨章审查自定义清单模板：`thesis-reviewer/references/review-checklist.md`
