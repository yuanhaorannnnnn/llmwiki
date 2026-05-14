# Mistakes

> 重复犯错记录。每条包含错误现象、根因、修复方式和防止再犯的规则。

## 2026-04-28 | 笔记正文中出现指向不存在页面的 [[wikilinks]]

**现象：** 结构化笔记正文中使用了 `[[agent]]`、`[[tool-use]]`、`[[kimi-k2-5]]`、`[[prompt-engineering]]` 等 wikilinks，点击后在 Obsidian 中创建空文件（如 `multi-modal-prompting.md`、`prompt-engineering.md`）。共发现 9 个死链 + 2 个空文件。

**根因：** video-ingest SKILL.md 的 Wikilink Convention 只规定了来源链（笔记↔转录稿↔媒体文件）的 wikilinks 格式，未明确禁止在正文中使用指向不存在页面的 `[[wikilinks]]`。

**修复：**
- 2 个空文件已删除
- 9 个死链已转为纯文本
- SKILL.md 补充了 3 条强制规则：wikilinks 仅限来源链、正文禁止无目标页面的 wikilinks、相关链接段不列空目标
- SCHEMA.md 新增 Wikilink Graph Convention 章节
- `transcribe_audio.py` 自动生成转录稿的媒体文件 wikilinks 和笔记占位符

**规则：** 写结构化笔记时，`[[wikilinks]]` 只用于指向确实存在的文件（转录稿、媒体文件、已有 wiki 页面）。概念/实体引用在没有对应页面前使用纯文本。
