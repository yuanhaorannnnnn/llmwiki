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
