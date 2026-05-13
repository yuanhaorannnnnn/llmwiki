# LLM Wiki

基于 Karpathy LLM Wiki 模式的知识库。

## 快速开始

1. 用 Obsidian 打开本目录作为 Vault
2. 阅读 `SCHEMA.md` 了解规范
3. 阅读 `index.md` 查看内容目录
4. 阅读 `log.md` 了解最近操作

## 目录结构

```
raw/          — 原始资料（只读，不覆盖）
  articles/   — 网页文章、剪报
  papers/     — PDF、arxiv 论文
  transcripts/— 原始转录稿
  assets/     — 图片、音频、视频
entities/     — 实体页面（人、组织、产品、模型）
concepts/     — 可长期复用的概念/主题沉淀
comparisons/  — 明确对比分析
queries/      — 单视频结构化笔记和一次性查询结果
_templates/   — 页面模板
```

视频内容默认遵循：原始转录稿放 `raw/transcripts/`；单视频结构化笔记放 `queries/`；明确对比分析放 `comparisons/`；可长期复用的知识沉淀放 `concepts/`。

## 规范

- 所有 wiki 页面使用 YAML frontmatter
- 使用 `[[wikilinks]]` 建立链接
- 标签必须来自 SCHEMA.md 的 taxonomy
- 更新时修改 `updated` 日期
- 操作后追加 log.md
