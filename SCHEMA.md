# Wiki Schema

## Domain
LLM / AI Agent / 知识管理方法论（可扩展）

## Conventions
- File names: lowercase, hyphens, no spaces（例：`transformer-architecture.md`）
- 每个 wiki 页面必须有 YAML frontmatter
- 使用 `[[wikilinks]]` 跨页面链接（每页至少 2 个出站链接）
- 更新页面时必须修改 `updated` 日期
- 新页面必须加入 `index.md` 对应分区
- 每次操作必须追加到 `log.md`
- **Provenance markers:** 当页面综合 3+ 来源时，在段落末尾追加 `^[raw/articles/source-file.md]`，让读者可追溯具体来源

## Frontmatter
```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [来自下方 taxonomy]
sources: [raw/articles/source-name.md]
# 可选质量标记：
confidence: high | medium | low        # 声明的可信度
contested: true                        # 存在未解决的矛盾
contradictions: [other-page-slug]      # 与本页冲突的页面
---
```

### raw/ Frontmatter
原始资料也带 frontmatter，用于重入时检测内容漂移：
```yaml
---
source_url: https://example.com/article   # 原始 URL（如有）
ingested: YYYY-MM-DD
sha256: <正文内容的 hex 摘要>
---
```
`sha256` 用于未来重入同一 URL 时跳过未变化内容，或标记已变化内容。

### 视频来源特殊字段
```yaml
---
source_url: https://youtube.com/watch?v=VIDEO_ID
video_id: VIDEO_ID
platform: youtube | bilibili
duration: "HH:MM:SS"
language: zh | en | auto
---
```

## Tag Taxonomy
- **模型:** model, architecture, benchmark, training, inference
- **技术:** optimization, fine-tuning, alignment, quantization, distillation
- **系统:** agent, tool-use, multi-modal, reasoning, memory
- **数据:** dataset, data-engineering, synthetic-data, evaluation
- **组织:** person, company, lab, open-source
- **产品:** product, platform, api, framework
- **方法:** comparison, timeline, survey, methodology
- **争议:** controversy, limitation, safety, ethics
- **来源类型:** article, paper, video, transcript, book, clipping
- **元信息:** prediction, todo, deprecated

规则：页面使用的所有 tag 必须出现在本 taxonomy 中。如需新 tag，先在此添加，再使用。

## Page Thresholds
- **新建页面**：实体/概念在 2+ 来源中出现，或在单一来源中处于核心地位
- **并入现有页面**：来源提及已有内容时，补充到对应页面
- **不建页面**：仅一笔带过、细节性内容、或超出 Domain 范围
- **拆分页面**：超过 ~200 行时，拆分为子主题并互链
- **归档页面**：内容被完全替代时，移入 `_archive/`，从 index 移除

## Directory Placement
- **单视频结构化笔记**：放入 `queries/`，用于保存一次视频 ingest 后生成的核心观点、关键要点、行动建议和来源路径。
- **明确对比分析**：放入 `comparisons/`，用于两个或多个对象、工具、模型、方案、体验的并排比较。
- **可长期复用的知识沉淀**：放入 `concepts/`，用于从多个来源或高价值单一来源中抽象出的稳定概念、方法论和主题页。
- **原始转录稿**：永远放入 `raw/transcripts/`，不与结构化笔记混放。
- **原始媒体与衍生素材**：视频、音频、图片等放入 `raw/assets/` 下对应子目录。

## Entity Pages
每页一个实体。包含：
- 概述 / 定义
- 关键事实与时间
- 与其他实体的关系（[[wikilinks]]）
- 来源引用

## Concept Pages
每页一个概念。包含：
- 定义 / 解释
- 当前知识状态
- 开放问题或争议
- 相关概念（[[wikilinks]]）

## Comparison Pages
并排分析。包含：
- 比较对象与目的
- 比较维度（表格优先）
- 结论或综合
- 来源

## Update Policy
新信息与既有内容冲突时：
1. 检查日期 — 较新来源通常优先
2. 若确实矛盾，记录双方立场并标注日期与来源
3. 在 frontmatter 标记：`contradictions: [page-name]`
4. 在 lint 报告中向用户提示待审

## Wikilink Graph Convention

为确保 Obsidian 图视图能追踪 raw → 转录 → 笔记的完整链路，所有文件必须双向链接：

```
┌──────────────────┐     [[wikilink]]      ┌──────────────────────┐
│  raw/assets/      │◄──────────────────────│  queries/xxx.md      │
│  video/<id>.mp4   │                       │  comparisons/xxx.md  │
│  audio/<id>.wav   │                       └────────┬─────────────┘
└────────┬──────────┘                                │
         │                                           │
         │[[wikilink]]          [[wikilink]]          │
         ▼                                           ▼
┌──────────────────┐                        ┌──────────────────────┐
│  raw/transcripts/│◄───────────────────────│  queries/xxx.md      │
│  <id>_transcript │                        │  (## 来源 段)        │
│  (## 相关笔记 段) │                        └──────────────────────┘
└──────────────────┘
```

**规则：**
- 笔记页面在 `## 来源` 段使用 `[[wikilinks]]` 指向其转录稿和媒体文件
- 转录稿在 `## 相关笔记` 段使用 `[[wikilinks]]` 回链其结构化笔记和媒体文件
- `transcribe_audio.py` 脚本自动生成转录稿中的媒体文件 wikilinks 和占位符，笔记链接需在笔记创建后回填
- `[[wikilinks]]` 路径从文件所在目录出发，使用相对路径（如 `../queries/xxx.md`）

## Ingest Pipeline

### 文章 / 网页
1. `web_extract(url)` 获取 markdown → 保存到 `raw/articles/`
2. 添加 raw frontmatter（source_url, ingested, sha256）
3. 分析内容，识别实体/概念
4. 检查 `index.md` 是否已有对应页面
5. 新建或更新 wiki 页面 → 更新 `index.md` → 追加 `log.md`

### 论文 / PDF
1. `web_extract(pdf_url)` 或 `ocr-and-documents` 提取全文
2. 保存到 `raw/papers/`，添加 raw frontmatter
3. 提取关键发现、方法、实验结果
4. 更新相关实体/概念页面，添加引用关系

### 视频 / 访谈
1. `youtube-content` 提取字幕（YouTube）
   - 或 `yt-dlp --write-auto-subs --sub-langs zh,en --skip-download` 获取字幕文件
2. 保存到 `raw/transcripts/`，添加视频专用 frontmatter
3. 按章节/主题分段，提取关键论点
4. 单视频结构化笔记保存到 `queries/`
5. 若视频产物是明确对比分析，保存到 `comparisons/`
6. 若内容可长期复用，再抽象或补充到 `concepts/`

### Bilibili
- 使用 `yt-dlp` 提取字幕：`yt-dlp --list-subs URL` 查看可用字幕
- 若只有 CC 字幕，用 `--write-auto-subs` 提取
- 若无字幕，提取音频后用 FunASR 转录（`iic/SenseVoiceSmall`）
- 其余流程同 YouTube

### RSS / 博客订阅
1. `blogwatcher` 扫描订阅源
2. 新文章 → `web_extract` 提取 → `raw/articles/`
3. 批量 ingest，减少重复索引操作

### 批量 Ingest
- 先读取所有来源
- 一次性识别所有实体/概念
- 单次搜索检查现有页面
- 统一创建/更新页面
- 最后统一更新 `index.md` 和 `log.md`

### Clippings / 剪藏
1. Obsidian Web Clipper 收藏的网页内容 → `Clippings/`
2. 添加 raw frontmatter（source_url, clipped, clipper_type）
3. 分析内容，识别实体/概念
4. 检查 `index.md` 是否已有对应页面
5. 新建或更新 wiki 页面 → 更新 `index.md` → 追加 `log.md`
