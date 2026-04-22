# Wiki Log

> 所有 wiki 操作的时序记录。仅追加，不修改。
> 格式：`## [YYYY-MM-DD] action | subject`
> action 取值：ingest, update, query, lint, create, archive, delete
> 超过 500 条时轮换：重命名为 log-YYYY.md，新建空白 log.md。

## [2026-04-22] create | Wiki 初始化
- Domain: LLM / AI Agent / 知识管理方法论
- 创建目录：raw/articles, raw/papers, raw/transcripts, raw/assets, entities, concepts, comparisons, queries, _templates
- 创建文件：SCHEMA.md, index.md, log.md, README.md
- 创建模板：_templates/concept-template.md, _templates/query-template.md

## [2026-04-22] update | SCHEMA.md 扩展
- 添加 tag: video, transcript, book（来源类型分类）
- 添加视频来源 frontmatter 规范
- 添加 Ingest Pipeline 章节（文章/论文/视频/Bilibili/RSS/批量）
