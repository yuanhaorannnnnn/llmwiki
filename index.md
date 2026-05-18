# Wiki Index

> 内容目录。每页按类型列出，附一行摘要。
> 查询时先读此文件定位相关页面。
> Last updated: 2026-05-18

---

## Ingest Sources
- 文章: `raw/articles/`
- 论文: `raw/papers/`
- 视频/访谈: `raw/transcripts/`
- 剪藏: `Clippings/`
- 图片/音频/视频: `raw/assets/`

---

## Entities
<!-- 按字母序排列 -->

## Concepts
- [[deep-research-agents]]
- [[neural-implicit-fields]]
- [[neural-radiance-field]] — NeRF 技术栈概念页：逆渲染本质、体渲染物理模型、Plenoxel 去神经网络化框架、位置编码/层次采样/视角相关颜色三大工程技巧，与 3DGS 的显式vs隐式/体渲染vs光栅化对比。
- [[depth-estimation]]
- [[4d-scene-decomposition]]
- [[3d-gaussian-splatting]] — 综合 6 篇 2024-2025 年论文的 3D Gaussian Splatting 技术栈概念页，涵盖渲染后端（光栅化 vs 光线追踪）、相机模型（无迹变换）、场景图、动态场景（4D 高斯/短寿命高斯）、深度先验（Prompting 范式）五个维度。
- [[sim-ready-asset-generation]] — 从视觉输入生成可直接导入物理引擎的 3D 资产的方法论概念页，核心区分"视觉正确"与"物理正确"，以 PhysX-Anything 为案例解析 Global→Local 多轮生成、193x 体素压缩和 sim-to-real 评估范式。
- [[redundancy-based-reliability-estimation]] — 无 ground truth 时利用多源冗余观测估计各源可靠性的概率方法论概念页，以高斯 Copula + 单因子近似为核心工具，可迁移至多 LLM 一致性评估、多 IMU 故障检测等场景。

## Comparisons
- [[kimi-k2-5-vs-claude-opus-4-6-coding-experience]] — 基于视频转录稿整理 Kimi K2.5 与 Claude Opus 4.6 在 Coding Agent 场景中的体验差异、关键要点和行动建议。

## Queries
- [[20260518-fourier-opacity-map]] — Fourier Opacity Map：用傅里叶级数解除顺序无关透明渲染——从 Alpha 混合 → Beer-Lambert → 狄拉克 δ → 傅里叶级数解析解，两 Pass GPU 实现与振铃抑制优化。
- [[20260518-claude-code-large-codebases-best-practices]] — Anthropic Applied AI 团队：Claude Code 在大代码库中的工作方式、Agentic Search vs RAG、五层 Harness 扩展体系（CLAUDE.md→Hooks→Skills→Plugins→MCP+LSP+Subagents）、三种企业配置模式、组织层面的采用策略。
- [[20260518-obsidian-ceo-stephango-note-system]] — Obsidian CEO Steph Ango 的个人笔记系统：File over App 哲学、极简文件夹策略、properties 替代文件夹分类、强制首次链接规则、模板驱动+可组合、Evergreen Notes、日周月年节奏系统，以及与 wiki 现有体系的对照。
- [[20260515-raycast-v2-technical-deep-dive]] — Raycast v2 跨平台重写技术深潜：自建 Hybrid 栈（原生外壳 + WebView + Node + Rust）的架构决策、Electron/Tauri 拒绝理由、WebKit/WebView2 原生感具体技巧、内存与性能数据。
- [[20260512-nvidia-drive-sim-neural-reconstruction]] — NVIDIA DRIVE Sim 神经重建引擎：从真实传感器数据到 3D 数字孪生的分钟级重建管线，支持闭环模拟和合成数据生成。
- [[20260512-jensen-huang-cmu-2026-commencement]] — Jensen Huang CMU 2026 毕业演讲：60 年计算范式终结（人写软件→机器学习）、失败即学习机制、AI 时代"明智推进"而非"畏缩退让"。
- [[20260512-html-effectiveness-demo-site]] — Thariq 的 AI 生成 HTML 演示合集离线镜像（21 个交互式页面），覆盖代码对比/可视化 diff/幻灯片/动画原型/流程图等 20 个用例。
- [[20260512-huzuohuyou-472-hk-political-department]] — 忽左忽右 472：港英政治部 Special Branch 的前世今生——从伦敦→上海→香港的殖民情报术复制、冷战谍都、九七解散轨迹。
- [[20260512-ue-multi-process-rendering]] — UE5 Multi-Process Rendering：双进程独立 GPU 替代 mGPU 共享显存，ADA Lovelace 不支持 NVLink 后的强制迁移路径。
- [[20260512-ue-ndisplay-overview]] — nDisplay 集群渲染技术总览：主节点+二级节点架构、帧同步机制、虚拟制片/LED 幕墙/穹顶投影实战用例。
- [[20260512-gpu-communication-tech]] — GPU 通信技术全景：GPUDirect 系列（P2P/RDMA/Storage）、NVLink→NVSwitch 演进、SLI 五模式与历史终结。
- [[20260512-hn-handoff-skill-discussion]] — HN 讨论可视化：/handoff skill 的诞生、AI 词汇滤镜效应（gate/handoff/invariant/seam）、LLM 是否"做事"的哲学辩论。
- [[20260512-airsim-physics-engine-discussion]] — AirSim 外部物理引擎集成讨论可视化（HTML）：8 人 106 天决策过程，JSBSim vs Gazebo，PR #3626 最终方案。
- [[20260512-alpha-compositing-guide]] — Alpha 融合技术详解：公式发展史（Smith→Wallace→Porter-Duff）、premultiplied alpha、over/in/atop/xor 模式、mask 二值化白边黑边陷阱。
- [[20260512-wayland-protocol-architecture]] — Wayland 协议与架构详解：为什么 X11 必须被替代、客户端渲染不可逆趋势、Every frame is perfect 设计哲学。
- [[20260512-openai-founders-podcast-core-memory]] — Sam Altman & Greg Brockman 首次合体播客：十年合作互补机制、安全哲学的分歧与迭代部署诞生、ChatGPT 真实影响故事、AI 公共叙事失败。
- [[20260512-the-next-great-moat]] — AI 时代真正的护城河不是产品/技术而是"组织形态本身"：form决定哪些人才只能在你的公司成为他们自己，情感承诺必须结构兑现。
- [[20260512-perplexity-agent-skills-design]] — Perplexity 内部 Agent Skills 设计与维护方法论：Skill 四本质（Directory/Format/Invocable/Progressive）、三级渐进加载、description 路由触发器、gotchas 维护飞轮。
- [[20260512-tdd-not-ai-native]] — TDD 在 AI 时代失效的根因分析（Goodhart's Law + 目标函数差异），替代方案：从过程确定性到结果确定性，用 property-based testing 和 E2E invariants 代替 mock-based unit test。
- [[20260511-how-we-built-our-multi-agent-research-system]] — Anthropic 多 Agent 研究系统的工程实战经验：orchestrator-worker 架构、prompt 启发式策略、评测三板斧、长上下文管理和 token 经济学。
- [[kimi-k2-5-tech-blog-visual-agentic-intelligence]] — Kimi K2.5 Agent Swarm 的 PARL 训练方法论：staged reward shaping 防 serial collapse、Critical Steps 指标、4.5× wall-clock 加速。
- [[anthropic-prompting-101-note]] — 基于 Anthropic Prompting 101 视频转录稿整理 prompt engineering 的核心观点、关键要点和行动建议。
- [[codex-gpt55-complete-guide-note]] — 基于 Codex + GPT-5.5 完整教程视频整理 Codex 项目组织、skills/plugins、自动化和多 agent 并行工作流。
- [[junhao-x-video-propaganda-note]] — 基于 X 视频画面字幕与 FunASR 对照整理的宣传叙事笔记，包含核心观点、关键要点和行动建议。
- [[claude-code-practical-tips-note]] — 基于 Anthropic Claude Code 核心开发者 Boris 工作坊演讲整理的实用技巧笔记，包含入门路径、prompt 策略、CLAUDE.md 配置、工具集成和高级工作流。
- [[tang-xuanzong-kaiyuan-collapse-note]] — 基于忽左忽右播客郭建龙访谈整理的唐玄宗与开天盛世崩溃分析笔记，涉及行政效率悖论、财政危机、节度使制度形成和安史之乱的制度分析。
