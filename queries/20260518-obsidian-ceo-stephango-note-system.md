---
title: "Obsidian CEO Steph Ango 的笔记系统：File over App 哲学与极简主义实践"
created: 2026-05-18
updated: 2026-05-18T17:00
type: query
tags: [video, youtube, blog, github, obsidian, note-taking, pkm, file-over-app, minimalism]
sources: [raw/transcripts/Dq3R3uS0sQ4_transcript.md, stephango.com/vault, github.com/kepano/kepano-obsidian]
source_url:
  - https://www.youtube.com/watch?v=Dq3R3uS0sQ4
  - https://stephango.com/vault
  - https://github.com/kepano/kepano-obsidian
confidence: high
---

# Obsidian CEO Steph Ango 的笔记系统

## 核心观点

Obsidian CEO Steph Ango (Kepano) 的个人笔记系统完全反直觉：不用文件夹分类、所有笔记堆在根目录、靠 frontmatter properties 组织、几乎每篇笔记从模板开始、强制 link 每个首次提及的事物。表面看是混乱的，但底层哲学是 **"速度与懒惰优先"**——系统设计目标是降低记录的摩擦，而非追求完美组织。核心理念 **File over App**：你的笔记是纯 Markdown 文件，任何软件消亡后内容仍在。

## 关键要点

### 1. File over App — 文件高于应用
- 笔记就是文件夹里的 `.md` 文件，不依赖 Obsidian 才能读取
- "如果软件坏了，你写的东西依然存在，比软件活得更久"
- 这是 Steph 笔记哲学的第一支柱：**工具会变，文件永存**

### 2. 极简文件夹策略
```
Root (根目录)
├── 我的笔记、日记、evergreen 想法  ← 绝大部分笔记在这里
├── references/   ← 外部世界的东西（人、书、电影、播客）
├── templates/    ← 模板文件
├── attachments/  ← 图片等附件
├── daily/        ← 每日笔记（仅作为链接锚点，不写内容）
└── clippings/    ← 从网页剪藏的文章
```
- 不使用 `categories/` 文件夹——categories 作为 **properties** 存在，不是文件夹
- 不使用 `notes/` 文件夹——所有个人笔记直接堆在根目录
- 判断标准：**如果一篇笔记在根目录，我知道它是我写的或与我直接相关**

### 3. Properties 替代文件夹分类
- 在笔记顶部用 `---` 包裹 YAML frontmatter，添加 `categories: meetings` 等属性
- 每个 category 对应一个 "Base"（Obsidian 的智能表格视图），自动聚合所有标记了该 category 的笔记
- 属性的值本身可以是 **link**（如 `people: [[Aisha]]`），形成双向连接
- **关键洞察**：不预先决定笔记属于哪个分类——写完再加属性，降低动笔摩擦

### 4. 强制首次链接规则
- **"Always link the first mention of something"** — 笔记中首次出现的任何事物（电影名、人名、餐厅、引用、概念）都必须用 `[[]]` 链接
- 即使目标笔记还不存在，也要创建 unresolved link
- 效果：随着时间推移，笔记网络自动生长，你可以追溯想法的起源和分叉路径
- 这是一种 **"间接意图设定"**：不强制你现在写那条笔记，但你留了一扇门

### 5. 模板驱动 + 可组合
- "Almost every note I create starts from a template"
- 内置模板：`meeting`、`people`、`book`、`movie`、`quote`、`evergreen`、`journal`、`monthly`
- **模板可组合**：同一条笔记可以叠加多个模板（如一个人既是 `people` 又是 `author`）
- 模板自动添加对应的 properties 和关联的 Base 查询
- 快捷键：`Opt+Shift+N` 创建唯一笔记，`Opt+Shift+T` 插入模板

### 6. 评分系统 (1-7)
- 7 = 彻底改变人生的正面影响
- 1 = 负面的改变人生
- 可应用于任何事物（电影、书、事件、想法）
- 通过 `ratings` category 聚合所有已评分条目

### 7. Evergreen Notes — 将想法对象化
- 来自 Andy Matuschak 的概念
- 将一个反直觉的洞察/想法写成独立笔记，标记为 `evergreen`
- 目的：**"Turn ideas into objects that you can manipulate"** — 在其他笔记中反复引用这个想法
- 示例：`death-is-sanity` 是一条 evergreen，其他笔记可以通过 `[[death-is-sanity]]` 引用它

### 8. 节奏系统：日→周→月→年
| 频率 | 动作 |
|------|------|
| **每日** | 有任何想法 → 创建 unique note → 写下来 → link first mentions → 加模板属性 |
| **每周** | 回顾过去几天的 notes，聚合相关想法写成编译笔记；用简单 checklist 写周待办 |
| **每月** | 回顾本月的"想法聚合"笔记，做更高层次的反思 |
| **每几个月** | 用 "Open Random Note" 随机漫步，偶然发现旧想法，获得新灵感 |
| **每年** | 回顾所有月度反思 + Steph 的 40 个年度问题 |

### 9. Property 命名约定（Blog 补充）
- **短名优先**：`start` 而非 `start-date`，`rating` 而非 `rating-score`
- **跨 category 复用**：`genre` 同时用于 books、movies、shows
- **默认 list 类型**：只要有可能出现多个值，就用 list 而非 text
- **Categories 必须用 link 且永远复数**：`categories: [[Books]]` 而非 `category: book`

### 10. 九条个人规则（Blog 原文）
1. 不要把内容分散到多个 vault
2. 不要用文件夹组织内容
3. 不用非标准 Markdown（确保跨工具可移植）
4. **Categories 和 tags 永远用复数**
5. 日期统一 `YYYY-MM-DD` 格式
6. 大量使用内部链接——即使目标页面还不存在
7. 用 1-7 评分体系
8. 每周只维护**一个**待办清单
9. "一致风格把未来的几百个决策压缩成一个"

### 11. GitHub 模板结构（kepano/kepano-obsidian）
- README 极度精简：描述 + 3 步上手（下载 → 解压 → Open folder as vault）
- 明确标注 **non-dogmatic**：用户被鼓励只取自己喜欢的部分
- 随 Obsidian 版本迭代更新（已迁移到 Core Bases 插件替代 Dataview）
- Community 已知问题：Step 3 原写 "create a new vault" 会误导新人，正确操作是 "Open folder as vault"

## 与你的 Wiki 系统的关联

- **File over App** ≈ 你的 `.md` 文件在 `queries/`、`concepts/` 里，Git 版本控制，不依赖任何特定工具
- **Evergreen Notes** ≈ 你的 `concepts/`（跨来源可复用的方法论概念页）
- **Categories via properties** ≈ 你的 YAML frontmatter `type: query/concept` + `tags: [...]`
- **Templates** ≈ 你的笔记输出格式模板（`---\ntitle:\ncreated:\ntype: query\n...`）
- **Daily notes as link anchors** ≈ 你的 `log.md`（时序记录所有操作，仅追加）
- **References folder** ≈ 你的 `raw/` 目录（外部来源原文存放）
- **Clippings** ≈ 根本就是同名概念，你也在用

**可能值得借鉴的：**
- **首次链接规则**：你在 wiki 笔记之间几乎没有内部交叉引用。考虑在蒸馏笔记时对关键概念加 `[[wikilinks]]`
- **随机回顾**：`log.md` 可以随机抽取一条旧条目重新审视
- **评分系统**：给 ingest 的内容打分（"这个 X thread 有多值得回顾？"）

## 相关笔记
- [[20260512-the-next-great-moat]] — AI 时代的下一个护城河：公司组织形态本身
- [[20260512-perplexity-agent-skills-design]] — Perplexity Agent Skills 设计与维护方法论
- [[20260515-raycast-v2-technical-deep-dive]] — Raycast v2 跨平台重写技术深潜：自建 Hybrid 栈的决策与细节

## 来源

- 视频：[[raw/assets/video/Dq3R3uS0sQ4/Dq3R3uS0sQ4.mp4]]
- 转录稿：[[raw/transcripts/Dq3R3uS0sQ4_transcript.md]]
- Blog：https://stephango.com/vault
- GitHub 模板：https://github.com/kepano/kepano-obsidian
