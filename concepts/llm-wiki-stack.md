# LLM Wiki 维护用 Skill 栈

这份清单面向“持续维护知识库”，重点覆盖：
- 链接导入
- YouTube / B 站视频内容沉淀
- 文档抽取
- 持续追踪与自动化

---

## A. Hermes 内置优先 Skill（建议先用）

### 1) youtube-content
- 作用：拉 YouTube transcript，转摘要 / 笔记 / 线程 / 博客。
- 适合：视频知识输入标准化。

### 2) obsidian
- 作用：在 vault 内创建、检索、追加、互链。
- 适合：结构化落库与批量维护。

### 3) ocr-and-documents
- 作用：PDF / 扫描件抽取（web_extract + 本地 OCR 流）。
- 适合：论文、报告、截图文档入库。

### 4) blogwatcher
- 作用：RSS / Atom 订阅监控。
- 适合：持续 ingest 的来源自动发现。

### 5) arxiv
- 作用：论文检索与元数据抓取。
- 适合：研究型 wiki 的高质量来源补给。

---

## B. 联网检索到的外部工具（可作为 skill 原料）

### 视频下载 / 字幕

- yt-dlp（多站点下载，含 YouTube）
  - https://github.com/yt-dlp/yt-dlp

- youtube-transcript-api（YouTube 字幕抓取）
  - https://github.com/jdepoix/youtube-transcript-api

- yutto（B站下载 CLI）
  - https://github.com/yutto-dev/yutto

- bilibili（B站字幕 / 弹幕相关工具）
  - https://github.com/yutto-dev/yutto-dev/bilibili

- bilibili-api（B站 API 封装）
  - https://github.com/Nemo2011/bilibili-api

---

## 链接导入 / 网页沉淀到 Obsidian

- Obsidian Web Clipper（官方）
  - https://github.com/obsidianmd/obsidian-clipper

- Obsidian Importer（官方导入插件）
  - https://github.com/obsidianmd/obsidian-importer

- Clipper Templates（常见模板）
  - https://github.com/kepano/clipper-templates
  - https://github.com/obsidian-community/web-clipper-templates

---

## C. 推荐落地组合（你的场景）

### 组合 1：视频研究流（YouTube + B站）

1. yt-dlp / yutto 下载视频与字幕到 `raw/transcripts`
2. youtube-content 处理 YouTube transcript
3. B站内容转 markdown 摘要，统一写入 `raw/transcripts`
4. Agent 执行 ingest，更新 `concepts/` 和 `entities/`

---

### 组合 2：网页链接流

1. 用 Obsidian Web Clipper 入库原文
2. 落到 `raw/articles`，命名带日期和来源域名
3. Agent 批量 ingest，补 `[[wikilinks]]` + 更新 `index/log`

---

### 组合 3：论文 / 报告流

1. arxiv 搜索 + ocr-and-documents 抽取全文
2. 缓存到 `raw/papers`
3. 每周 lint：断链、冲突、过期页

---

## D. 你现在最该补的两个 skill

（这里原图没完全展示，我帮你补全合理推断 👇）

### 1) ingest-pipeline（核心缺失）
- 自动：
  - raw → concepts
  - 打标签 / 建立双链
  - 去重 / merge

### 2) link-resolver / entity-builder
- 自动识别：
  - 实体（人 / 项目 / 技术）
  - 建立 entity 页面
  - 反向链接

## 相关笔记
- [[20260518-obsidian-ceo-stephango-note-system]] — Obsidian CEO Steph Ango 的笔记系统：File over App 哲学与极简主义实践
- [[20260512-perplexity-agent-skills-design]] — Perplexity Agent Skills 设计与维护方法论
- [[20260512-the-next-great-moat]] — AI 时代的下一个护城河：公司组织形态本身

---

## E. 可进阶优化（强烈建议）

- 内容评分（高质量优先）
- 知识去重（embedding / hash）
- 自动摘要版本管理
- timeline / 演进视图
- topic graph（知识图谱）
