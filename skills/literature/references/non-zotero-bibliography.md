# 非 Zotero 与混合管线（书目与引用）

本仓库默认示例以 **Zotero + BibTeX + LaTeX** 为主；若你使用 **EndNote、Mendeley、NoteExpress** 或 **纯 Word**，可参考下列路径，并与 `docx`、`literature` 技能配合。

## EndNote / Mendeley / NoteExpress

- **与 LaTeX 协作**：在软件中将条目导出为 **BibTeX**（或先导出 RIS，再用 Zotero/JabRef 转为 `.bib`），放入 `{{THESIS_DIR}}/references/` 并在主 TeX 中 `\bibliography{...}` 引用。
- **去重**：各软件自带去重；合并多源题录后导出前建议运行一次去重。
- **citekey 规则**：导出 BibTeX 时注意 citekey 是否与 `literature` 技能中的简称规则一致；不一致时以你论文中 `\cite{}` 实际使用的 key 为准，批量替换或统一在 `.bib` 中改 key。

## 纯 Word（无 LaTeX）

- 使用 Word **引用与书目**功能或 EndNote 插件生成参考文献表；技能 **`docx`** 负责版式与修订，**不替代** Word 自带引用引擎。
- 若后期需改投 LaTeX 模板：通常需将参考文献表**导出为纯文本**或从管理器再导出 BibTeX，由 `literature`「生成 BibTeX」模式辅助清洗字段。

## 与 `literature` 技能分工

| 环节 | 建议 |
|------|------|
| 题录批量管理 | 仍以专业文献管理软件为主 |
| 综述段落、`\cite` 润色、从列表生成 Bib | 使用 `literature` 各模式 |
| PDF 全文抽取 | 使用 `pdf` 技能 |
| Word 成稿格式 | 使用 `docx` 技能 |

## 注意

- 不在技能中保存任何数据库账号密码；导出与 API 密钥仅保存在本机环境变量或软件配置中。
