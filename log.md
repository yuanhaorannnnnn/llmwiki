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
- 添加 tag: video, transcript, book, clipping（来源类型分类）
- 添加视频来源 frontmatter 规范
- 添加 Ingest Pipeline 章节（文章/论文/视频/Bilibili/RSS/剪藏/批量）
- 修正剪藏目录为 Clippings/（Obsidian Web Clipper 配置路径）
- 细分 raw/assets/ 为 audio/video/

## [2026-04-28] create | Kimi K2.5 与 Claude Opus 4.6 编码体验对比
- 来源：raw/transcripts/bv1h1pxzpejim_transcript.md
- 视频：raw/assets/video/bv1h1pxzpejim.mp4
- 创建笔记：comparisons/kimi-k2-5-vs-claude-opus-4-6-coding-experience.md

## [2026-04-28] ingest | X 视频 2048301694665330770
- 原始链接：https://x.com/i/status/2048301694665330770
- 下载视频：raw/assets/video/2048301259434962944/2048301259434962944.mp4
- 缩略图：raw/assets/video/2048301259434962944/2048301259434962944.jpg
- 元数据：raw/assets/video/2048301259434962944/2048301259434962944.info.json
- 抽取音频：raw/assets/audio/2048301259434962944.wav
- FunASR JSON：raw/transcripts/2048301259434962944.funasr.json
- 转录稿：raw/transcripts/2048301259434962944_transcript.md
- ASR 后端：FunASR iic/SenseVoiceSmall
- 质量标记：low（平台无字幕，BGM/歌曲式音频导致 ASR 仍需人工复核）

## [2026-04-28] create | 军号 X 视频宣传叙事笔记
- 来源：raw/transcripts/2048301259434962944_transcript.md
- 视频：raw/assets/video/2048301259434962944/2048301259434962944.mp4
- 创建笔记：queries/junhao-x-video-propaganda-note.md

## [2026-04-28] ingest | 本地 X 视频 x-2048592344552010061
- 视频：raw/assets/video/x-2048592344552010061.mp4
- 抽取音频：raw/assets/audio/x-2048592344552010061.wav
- FunASR JSON：raw/transcripts/x-2048592344552010061.funasr.json
- 转录稿：raw/transcripts/x-2048592344552010061_transcript.md
- ASR 后端：FunASR iic/SenseVoiceSmall
- 分段数：81
- 时间戳模式：approximate

## [2026-04-28] create | Anthropic Prompting 101 结构化笔记
- 来源：raw/transcripts/x-2048592344552010061_transcript.md
- 视频：raw/assets/video/x-2048592344552010061.mp4
- 创建笔记：queries/anthropic-prompting-101-note.md

## [2026-04-28] update | 视频笔记目录规范
- 更新 SCHEMA.md：明确单视频结构化笔记放 queries/，明确对比分析放 comparisons/，长期知识沉淀放 concepts/，原始转录稿放 raw/transcripts/
- 更新 README.md：同步目录结构说明

## [2026-04-28] ingest | X 视频 2048698399961289011
- 原始链接：https://x.com/i/status/2048698399961289011
- 下载视频：raw/assets/video/2048628829753835521/2048628829753835521.mp4
- 缩略图：raw/assets/video/2048628829753835521/2048628829753835521.jpg
- 元数据：raw/assets/video/2048628829753835521/2048628829753835521.info.json
- 抽取音频：raw/assets/audio/2048628829753835521.wav
- FunASR JSON：raw/transcripts/2048628829753835521.funasr.json
- 转录稿：raw/transcripts/2048628829753835521_transcript.md
- ASR 后端：FunASR iic/SenseVoiceSmall
- 分段数：241
- 时间戳模式：approximate

## [2026-04-28] ingest | X 视频 2047877250184618248
- 原始链接：https://x.com/i/status/2047877250184618248
- 下载视频：raw/assets/video/2047876749925683200/2047876749925683200.mp4
- 缩略图：raw/assets/video/2047876749925683200/2047876749925683200.jpg
- 元数据：raw/assets/video/2047876749925683200/2047876749925683200.info.json
- 抽取音频：raw/assets/audio/2047876749925683200.wav
- FunASR JSON：raw/transcripts/2047876749925683200.funasr.json
- 转录稿：raw/transcripts/2047876749925683200_transcript.md
- ASR 后端：FunASR iic/SenseVoiceSmall
- 分段数：130
- 时间戳模式：approximate
- 质量标记：medium

## [2026-04-28] create | Claude Code 实用技巧结构化笔记
- 来源：raw/transcripts/2047876749925683200_transcript.md
- 视频：raw/assets/video/2047876749925683200/2047876749925683200.mp4
- 创建笔记：queries/claude-code-practical-tips-note.md

## [2026-04-28] ingest | YouTube 视频 n905xN3R9UQ
- 原始链接：https://youtu.be/n905xN3R9UQ
- 下载视频：raw/assets/video/n905xN3R9UQ/n905xN3R9UQ.mp4
- 缩略图：raw/assets/video/n905xN3R9UQ/n905xN3R9UQ.webp
- 元数据：raw/assets/video/n905xN3R9UQ/n905xN3R9UQ.info.json
- 抽取音频：raw/assets/audio/n905xN3R9UQ.wav
- FunASR JSON：raw/transcripts/n905xN3R9UQ.funasr.json
- 转录稿：raw/transcripts/n905xN3R9UQ_transcript.md
- ASR 后端：FunASR iic/SenseVoiceSmall
- 分段数：142
- 时间戳模式：approximate
- 质量标记：medium
- 备注：YouTube 视频无字幕，为播客格式音频

## [2026-04-28] create | 唐玄宗与开天盛世崩溃结构化笔记
- 来源：raw/transcripts/n905xN3R9UQ_transcript.md
- 视频：raw/assets/video/n905xN3R9UQ/n905xN3R9UQ.mp4
- 创建笔记：queries/tang-xuanzong-kaiyuan-collapse-note.md

## [2026-04-30] create | 3D Gaussian Splatting 技术栈概念页
- 来源：6 篇论文 Denote 笔记（~/Documents/notes/）
- PDF 路径：raw/papers/paper/E-神经渲染/ 及 TargetWorks/3DGS路线/
- 创建概念页：concepts/3d-gaussian-splatting.md
- 涵盖：3DGRT、3DGUT、OmniRe、4DGS、FreeTimeGS、Prompt Depth Anything
- 论文笔记保持原样在 ~/Documents/notes/，概念页提取可复用知识

## [2026-04-30] create | Sim-ready Asset Generation 概念页
- 来源：PhysX-Anything Denote 笔记（~/Documents/notes/20260428T155315--paper-physx-anything__paper.md）
- PDF 路径：raw/papers/paper/E-物理仿真/2025-PhysX-Anything-Generative-Sim-Ready-3D-Assets-with-Physical-Properties-from-a-Single-Image.pdf
- 创建概念页：concepts/sim-ready-asset-generation.md
- 核心内容：sim-ready 定义、Global→Local 多轮生成、193x 体素压缩、物理正确性评估范式

## [2026-04-30] create | Redundancy-based Reliability Estimation 概念页
- 来源：Exploiting Redundancy Denote 笔记（~/Documents/notes/20260429T181244--paper-sensor-redundancy-reliability__paper.md）
- PDF 路径：raw/papers/paper/E-自动驾驶/2019-Exploiting Redundancy for Reliability Analysis of Sensor Perception.pdf
- 创建概念页：concepts/redundancy-based-reliability-estimation.md
- 核心内容：无 ground truth 概率估计、高斯 Copula + 单因子近似、最少传感器数、迁移场景

## [2026-05-13] article-ingest | UE5 Multi-Process Rendering（3篇合成） → queries/20260512-ue-multi-process-rendering.md
- 来源：3 篇 Clippings（Epic Dev Community + UE 5.7 Docs）
- 核心内容：MPR vs mGPU 架构差异、双进程分工、ADA Lovelace 迁移路径

## [2026-05-13] article-ingest | nDisplay 技术总览（2篇合成） → queries/20260512-ue-ndisplay-overview.md
- 来源：2 篇 Clippings（UE 5.7 Docs + Epic Tech Blog）+ nDisplay 白皮书 PDF
- 核心内容：主节点+二级节点架构、帧同步、LED 幕墙/穹顶/军事训练用例

## [2026-05-13] article-ingest | GPU 通信技术全景（2篇合成） → queries/20260512-gpu-communication-tech.md
- 来源：2 篇 Clippings（知乎 + NVIDIA GameWorks Docs）
- 核心内容：GPUDirect 四件套、NVLink vs SLI、RDMA 跨节点通信、SLI 的历史终结

## [2026-05-12] discussion-digest | HN: /handoff skill & AI 词汇影响力 → queries/20260512-hn-handoff-skill-discussion.html
- 来源：https://news.ycombinator.com/item?id=47581897
- 三条主线：handoff 实践分享、AI 词汇滤镜效应、LLM agency 哲学辩论

## [2026-05-12] podcast-ingest | 忽左忽右 472：港英政治部轶闻 → queries/20260512-huzuohuyou-472-hk-political-department.md
- 来源：Apple Podcasts RSS → m4a 下载 → ffmpeg 转 wav → FunASR 转录（84min）
- 核心内容：Special Branch 的殖民情报术本质（伦敦→上海→香港复制链路）、冷战谍都角色、九七解散轨迹

## [2026-05-12] discussion-digest | AirSim 外部物理引擎讨论 → queries/20260512-airsim-physics-engine-discussion.html
- 来源：https://github.com/microsoft/AirSim/discussions/3284
- 首次使用 discussion-digest skill · 输出为交互式 HTML（参与方卡片+时间线+结论面板）

## [2026-05-12] article-ingest | Wayland 协议与架构详解 → queries/20260512-wayland-protocol-architecture.md
- 来源：Clippings（微信公众号文章，52KB）
- 核心内容：X11 架构过时根因、Wayland Every frame is perfect 设计哲学、协议面向对象模型、生态迁移阻力

## [2026-05-12] article-ingest | Alpha 融合技术详解 → queries/20260512-alpha-compositing-guide.md
- 来源：Clippings（CSDN 博客，38KB）
- 核心内容：公式发展史、premultiplied alpha、Porter-Duff 融合模式、mask 二值化陷阱

## [2026-05-12] video-ingest | OpenAI Founders Core Memory 访谈 → queries/20260512-openai-founders-podcast-core-memory.md
- 来源：https://www.youtube.com/watch?v=NCKQL0op30E（82min，zh-Hans 字幕）
- 核心内容：SA & GB 十年合作、安全哲学的迭代部署诞生、公共叙事失败、真实影响故事

## [2026-05-12] article-ingest | AI 时代的下一个护城河 → queries/20260512-the-next-great-moat.md
- 来源：https://www.linkedin.com/pulse/next-great-moat-jaya-gupta-6onwc
- 核心内容：组织形态即护城河、被选中vs被看见、情感承诺须结构兑现

## [2026-05-12] create | Neural Radiance Field (NeRF) 技术栈概念页 → concepts/neural-radiance-field.md
- 来源：3 篇 Clippings（知乎×2 + CSDN×1），从 query 升级为 concept
- 核心内容：逆渲染→体渲染→Plenoxel→NeRF 四步认知链，与 3DGS 对比，可迁移洞见

## [2026-05-12] video-ingest | NVIDIA DRIVE Sim 神经重建引擎 → queries/20260512-nvidia-drive-sim-neural-reconstruction.md
- 来源：https://www.youtube.com/watch?v=vgot-CK1xRk
- 字幕：YouTube 自动中文字幕，102秒技术demo
- 核心内容：传感器数据→AI重建→3D数字孪生→Omniverse→闭环模拟链路

## [2026-05-12] video-ingest | Jensen Huang CMU 2026 毕业演讲 → queries/20260512-jensen-huang-cmu-2026-commencement.md
- 来源：https://www.youtube.com/watch?v=FZh_0uRgrg4
- 字幕：YouTube 自动中文字幕（zh-Hans），跳过 ASR
- 核心内容：计算范式变革、失败哲学、AI 时代的恐惧与责任

## [2026-05-12] article-ingest | Perplexity Agent Skills 设计方法论 → queries/20260512-perplexity-agent-skills-design.md
- 来源：https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
- 核心内容：Skill 四本质、三级渐进加载、description 路由触发器、gotchas 维护飞轮、构建五步流程

## [2026-05-12] article-ingest | TDD 反而不是 AI 时代的答案 → queries/20260512-tdd-not-ai-native.md
- 来源：https://yage.ai/share/tdd-not-ai-native-20260508.html
- 核心内容：AI 时代 TDD 失效的根因（Goodhart's Law），替代方案：property-based testing + E2E invariants + verify state not behavior

## [2026-05-12] update | 合并 video-ingest + article-ingest → content-ingest v2.0.0
- 合并原因：两者输出结构同构（均为 queries/ 结构化笔记），差异仅在输入模态
- 新 skill：`~/.agents/repos/agent-skills/skills/content-ingest/`，自动路由视频/文章/本地三种输入
- 删除旧 skill：video-ingest、article-ingest、bilibili-video-ingest
- B站视频 bv1h1pxzpejim 重新用 FunASR 转录，替换旧 Whisper 转录稿
- 清理 Whisper：删除 JSON 文件 + 更新旧 SKILL.md / SCHEMA.md / download-notes.md 共 7 处引用
- FunASR `iic/SenseVoiceSmall` 为统一 ASR 后端

## [2026-04-28] create | Codex + GPT-5.5 完整教程结构化笔记
- 来源：raw/transcripts/2048628829753835521_transcript.md
- 视频：raw/assets/video/2048628829753835521/2048628829753835521.mp4
- 创建笔记：queries/codex-gpt55-complete-guide-note.md

## [2026-04-30] paper-to-concept | Split4D → 3d-gaussian-splatting, 4d-scene-decomposition
- 论文：不用视频追踪器也能做4D分割——让高斯粒子自己"流动"着学特征
- 归属现有：3d-gaussian-splatting（动态场景扩展）
- 新建：4d-scene-decomposition（4D 场景分解：动态场景重建 + 实例分割 + 时序一致性）
- 更新：3d-gaussian-splatting.md 添加 Split4D 链接

## [2026-04-30] paper-to-concept | InfiniDepth → 3d-gaussian-splatting, depth-estimation, neural-implicit-fields
- 论文：InfiniDepth: Arbitrary-Resolution and Fine-Grained Depth Estimation with Neural Implicit Fields
- 归属现有：3d-gaussian-splatting（NVS 应用，Gaussian Splatting Head 渲染）
- 新建：depth-estimation（深度估计方法论，离散网格 vs 隐式场表示）
- 新建：neural-implicit-fields（神经隐式场通论，覆盖 NeRF/SDF/深度场）
- 新建笔记：~/Documents/notes/20260430T184500--paper-infinidepth__paper.md

## [2026-04-30] update | 修复 Prompt Depth Anything 分类错误
- 从 3d-gaussian-splatting.md 摘除：深度先验段落、表格行、可迁移洞见、来源引用、frontmatter sources
- 移入 depth-estimation.md：主要流派（提示增强路线补充细节）、关键概念（稀疏锚点定尺度）、洞见（稀疏提示+稠密基础模型）

## [2026-05-11] paper-to-concept | 给 Deep Research Agent 配一份可验证的待办清单加一个证据审计员，不换模型就做到第一 → deep-research-agents

## [2026-05-11] article-ingest | Anthropic 多 Agent 研究系统的工程实战经验 → queries/20260511-how-we-built-our-multi-agent-research-system.md
## [2026-05-11] article-ingest | Kimi K2.5 Agent Swarm 的 PARL 训练方法论 → queries/kimi-k2-5-tech-blog-visual-agentic-intelligence.md
## [2026-05-15] article-ingest | Raycast v2 跨平台重写：自建 Hybrid 栈的架构决策与 WebView 原生感技巧 → queries/20260515-raycast-v2-technical-deep-dive.md
## [2026-05-18] video-ingest | Obsidian CEO Steph Ango 笔记系统：File over App、极简文件夹、properties 替代分类、首次链接规则 → queries/20260518-obsidian-ceo-stephango-note-system.md
## [2026-05-18] article-ingest | Claude Code 大代码库工作方式与五层 Harness 体系 → queries/20260518-claude-code-large-codebases-best-practices.md
## [2026-05-18] wechat-ingest | Fourier Opacity Map：傅里叶级数解顺序无关透明 → queries/20260518-fourier-opacity-map.md
## [2026-05-19] clipping-ingest | Codex Goals：持久化目标合约替代反复提示 → queries/20260519-codex-goals-guide.md
## [2026-05-19] clipping-ingest | 多智能体协作工程调查：触发/拓扑/调用链/四大系统对比 → queries/20260519-multi-agent-collaboration-survey.md
## [2026-05-19] clipping-ingest | Karpathy CLAUDE.md：82K Star 21 条规则 65%→94% → queries/20260519-karpathy-claude-md-viral.md
## [2026-05-19] clipping-ingest | Codex-maxxing：Jason Liu 持久化线程 + Obsidian Vault + Heartbeats → queries/20260519-codex-maxxing-jason-liu.md
## [2026-05-18] clipping-ingest | 基于 Clippings 重整 Fourier Opacity Map → queries/20260518-fourier-opacity-map.md
- 来源：Clippings/Fourier Opacity Map传统图形学性感时刻.md
- 更新：改用 clipping 作为来源，补充 Depth Pass / Shadow Mask 代码映射、Normalization、Ringing Suppression 与限制

## [2026-05-18] clipping-ingest | 基于 Clippings 重整 Claude Code 大代码库最佳实践 → queries/20260518-claude-code-large-codebases-best-practices.md
- 来源：Clippings/How Claude Code works in large codebases Best practices and where to start.md
- 更新：改用 clipping 作为来源，补充 Agentic Search、五层 Harness、LSP、Subagents、组织 owner 与 CarlaUE5 启发

## [2026-05-18] clipping-ingest | Kimi Agent Infra Database 服务 → queries/20260518-kimi-agent-infra-database-service.md
- 来源：Clippings/Agent Infra 实践复盘：Kimi 如何搭建 Agent 背后的 Database 服务.md
- 新建：Kimi K2.6 建站场景下的 Agent-native database infra 笔记

## [2026-05-18] clipping-ingest | Agent Infra Runtime 层 → queries/20260518-agent-infra-runtime-layer.md
- 来源：Clippings/当我们在谈论 Agent Infra 时我们在谈论什么.md
- 新建：Agent Infra 作为 inference 之上的 runtime 层，整理 Box、Branching、Messaging、Scheduler 等抽象

## [2026-05-18] clipping-ingest | AI Agent 喜欢的基础软件 → queries/20260518-ai-agent-friendly-infrastructure.md
- 来源：Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？.md
- 新建：稳定心智模型、自然语言到符号表示、日抛 workload、虚拟化和商业模式整理

## [2026-05-18] create | Agent-native Infrastructure 概念页 → concepts/agent-native-infrastructure.md
- 来源：三篇 Agent Infra clipping + Kimi/TiDB 案例
- 核心火花：Agent Infra 不是训练/推理 infra，而是支撑 Agent action 的 runtime 层；关键能力是可丢弃环境、虚拟独占、并行探索和低成本长尾服务

## [2026-05-18] clipping-ingest | Claude Code Prompt Caching → queries/20260518-claude-code-prompt-caching.md
- 来源：Clippings/Lessons from building Claude Code Prompt caching is everything.md
- 核心：prefix match、稳定工具集、cache-safe compaction、defer tool loading

## [2026-05-18] clipping-ingest | Onboarding Claude Code like a new developer → queries/20260518-onboarding-claude-code-like-new-developer.md
- 来源：Clippings/Onboarding Claude Code like a new developer Lessons from 17 years of development.md
- 核心：Skyline legacy codebase 案例，context layer 作为版本化项目资产

## [2026-05-18] clipping-ingest | Claude Opus 4.7 with Claude Code → queries/20260518-claude-opus-4-7-code-best-practices.md
- 来源：Clippings/Best practices for using Claude Opus 4.7 with Claude Code.md
- 核心：xhigh effort、adaptive thinking、减少交互轮次、明确 subagent/tool-use 触发条件

## [2026-05-18] clipping-ingest | Claude Code Session Management and 1M Context → queries/20260518-claude-code-session-management-1m-context.md
- 来源：Clippings/Using Claude Code session management and 1M context.md
- 核心：continue / rewind / clear / compact / subagents 的 context hygiene 决策

## [2026-05-18] clipping-ingest | Seeing like an agent → queries/20260518-claude-code-tool-design-seeing-like-agent.md
- 来源：Clippings/Seeing like an agent how we design tools in Claude Code.md
- 核心：AskUserQuestion、Task tool、Grep、progressive disclosure、工具随模型能力演化

## [2026-05-18] clipping-ingest | Claude Code Subagents → queries/20260518-claude-code-subagents.md
- 来源：Clippings/How and when to use subagents in Claude Code.md
- 核心：研究、并行、fresh review、verification、pipeline workflow 的 subagent 使用边界

## [2026-05-18] clipping-ingest | Claude Code Auto Mode → queries/20260518-claude-code-auto-mode.md
- 来源：Clippings/Auto mode for Claude Code.md
- 核心：少打断的权限模式，classifier 在 tool call 前阻断危险动作

## [2026-05-18] clipping-ingest | Claude Code Code Review → queries/20260518-claude-code-code-review.md
- 来源：Clippings/Code Review for Claude Code.md
- 核心：多 agent 深度 PR 审查，验证 bug、过滤误报、按严重程度输出

## [2026-05-18] create | Claude Code Harness 概念页 → concepts/claude-code-harness.md
- 来源：8 篇 Anthropic Claude Code blog + 大代码库最佳实践
- 核心：Claude Code 的效果由模型 + harness 决定，harness 包括 cache、context、tools、subagents、permissions、review、onboarding 和 model tuning

## [2026-05-18] article-ingest | Why I Don’t Vibe Code → queries/20260518-why-i-dont-vibe-code.md
- 来源：raw/articles/20260518-why-i-dont-vibe-code.md
- 核心：vibe coding 能降低 accidental complexity，但 friction、essential complexity、协作流程和责任链条不能被简单外包给 LLM

## [2026-05-18] clipping-ingest | Pi Coding Agent 最全面指南 → queries/20260518-pi-coding-agent-goal-open-model-harness.md
- 来源：Clippings/Pi Coding Agent 最全面指南（完美支持goal）.md
- 核心：Pi 不是更省心的 Claude Code，而是面向开放模型测试的可拆卸 agent harness；关键在 provider 配置、最小组件栈、goal 注入、plan-first 和 skill-amplified workflow

## [2026-05-18] paper-ingest | No Silver Bullet → queries/20260518-brooks-no-silver-bullet.md
- 来源：raw/papers/20260518-brooks-no-silver-bullet.pdf
- 新建：整理 Brooks 对 essence / accident 的区分、四个 essential difficulties、promising attacks，以及对 AI coding / agent harness 的迁移

## [2026-05-18] create | Essential vs Accidental Complexity 概念页 → concepts/essential-vs-accidental-complexity.md
- 来源：Brooks《No Silver Bullet》+ Why I Don’t Vibe Code
- 核心：LLM / coding agent 主要压缩 accidental complexity；需求、抽象、边界、变化、责任和系统设计仍是 essential complexity

## [2026-05-18] video-ingest | X article/video: Obsidian Web Clipper AI Interpreter → queries/20260518-obsidian-web-clipper-ai-interpreter-video.md
- 来源：https://x.com/alin_zone/status/2055860128356892744
- 媒体：raw/assets/video/x-2055860128356892744/x-2055860128356892744.mp4
- 说明：视频无音频流，无法 FunASR 转录；已保存关键帧和 X article JSON，并基于公开正文生成无音轨说明与结构化笔记

## [2026-05-18] video-ingest | Lex Fridman Podcast #491-#494 → queries/20260518-lex-fridman-491-494-builder-stack-synthesis.md
- 来源：YouTube playlist + Lex Fridman 官方 transcripts
- 创建笔记：queries/20260518-lex-fridman-491-peter-steinberger-openclaw.md
- 创建笔记：queries/20260518-lex-fridman-492-rick-beato-music-ai.md
- 创建笔记：queries/20260518-lex-fridman-493-jeff-kaplan-game-design.md
- 创建笔记：queries/20260518-lex-fridman-494-jensen-huang-nvidia-ai.md
- 创建综合页：queries/20260518-lex-fridman-491-494-builder-stack-synthesis.md
- 核心内容：AI factory、personal agent runtime、interactive worlds、creative authenticity 共同组成 AI 时代 builder stack

## [2026-05-18] video-ingest-update | Lex Fridman Podcast #491-#494 raw video download
- 补下载原始视频：raw/assets/video/lex-fridman-491-494/YFjfBk8HI5o/YFjfBk8HI5o.mp4
- 补下载原始视频：raw/assets/video/lex-fridman-491-494/1SJiTwbSI58/1SJiTwbSI58.mp4
- 补下载原始视频：raw/assets/video/lex-fridman-491-494/H9rF1CSSh-w/H9rF1CSSh-w.mp4
- 补下载原始视频：raw/assets/video/lex-fridman-491-494/vif8NQcjVf0/vif8NQcjVf0.mp4
- 同步更新四篇 episode note 和综合页的 sources
