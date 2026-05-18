---
title: "如何做 AI Agent 喜欢的基础软件"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, architecture, platform]
sources: ["Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？.md"]
source_url: https://mp.weixin.qq.com/s?__biz=Mzg5NTc0MjgwMw==&mid=2247521814&idx=1&sn=49ceeed78a26438ade5d5b706623e88f&scene=21&poc_token=HOOMCmqjpnEmeKZEdCsRwviMhZYyLg_aQdW3I0AX
confidence: medium
rating: 7
---

# 如何做 AI Agent 喜欢的基础软件

## 核心观点

这篇文章从“基础软件的主要使用者正在从人类开发者转向 AI Agent”出发，重新定义 Agent-friendly infrastructure 的设计原则。它的核心不是给 Agent 发明一套全新接口，而是顺应模型已经内化的稳定心智模型：文件系统、shell、SQL、代码、进程、I/O。

真正的变化不在于底层能力全新，而在于使用者、规模和生命周期变了：Agent 会高速创建资源、并行试错、丢弃失败路径，并把过去不经济的长尾软件需求变成可服务对象。

## 关键要点

### 1. 暴露给 Agent 的不是 UI，而是心智模型

Agent 使用基础软件时，真正接触的不是视觉 UI，而是系统背后的抽象和约定。文件系统、Bash、Python、SQL 这类几十年稳定抽象，对 LLM 极其友好，因为它们在训练语料中反复出现，语义边界稳定，组合方式清晰。

文章不看好为了 Agent 发明全新框架的原因也在这里：如果人类程序员都懒得学，模型训练语料里也缺乏稳定模式，那么 Agent 更难可靠使用。Agent 更偏好“它已经懂的系统”，然后用远高于人类的速度写胶水代码。

### 2. 好接口：自然语言表达意图，符号逻辑固化执行

Agent-friendly interface 至少要满足三点：

- 可以被自然语言描述。
- 可以被符号逻辑固化。
- 能交付确定性结果。

自然语言适合表达意图，但不适合承载执行语义。成功系统通常会在自然语言和执行之间放一个稳定中间层，例如 SQL、脚本、代码、配置文件。Agent 可以容忍输入阶段的歧义，但系统必须定义“歧义何时被消除”。

这和 [[20260512-tdd-not-ai-native]] 的结论相通：AI 可以自由探索实现路径，但 contract、schema 和 invariant 必须清晰。

### 3. Agent 产出的工作负载是日抛型的

文章提出一个关键转变：Agent 时代的很多代码和服务不是长期精雕细琢的工程，而是“快速创建、验证、丢弃”的日抛型工作负载。

这并不意味着可靠性不重要。恰恰相反，长尾需求被释放后，租户数量会爆炸；每个服务访问频率低，但仍然需要在线。Supabase 式 idle pause 对长尾 Agent 服务并不天然合适，因为再小的在线服务也是在线服务。

### 4. 低成本的前提是虚拟化

如果每个 Agent 任务背后都是一个真实 infra 环境，或者一个真实 Postgres 进程，百万级规模下管理开销会先于业务价值爆炸。因此必须引入虚拟化：

- 虚拟数据库实例
- 虚拟分支
- 虚拟环境

关键是资源层高度共享，语义层保持隔离。Agent 需要感觉“这是我的独立环境，我可以随便试”，底层则不能真的为每个需求分配完整物理实例。

这个观点与 [[20260518-kimi-agent-infra-database-service]] 完全闭合：TiDB Cloud 的虚拟数据库界面正是这条原则的落地案例。

### 5. 单位时间能撬动多少算力，会成为新指标

传统聊天式 Agent 的单位时间算力基本被锁在单轮请求上。复杂任务更像团队协作，需要同时启动 100 或 1000 个 worker 并行探索。文章称这类模式为 wide research：把几百篇论文分发给大量 Agent 并行阅读，再由汇总 Agent 交叉验证和结构化输出。

这要求 infra 能快速开“工位”、分发任务、收敛结果、去重、纠错、回放失败，并让成本实时可见。这里和 [[kimi-k2-5-tech-blog-visual-agentic-intelligence]] 的 PARL / Critical Steps 思想有明显连接：并行不是 prompt 风格，而是系统能力。

### 6. 商业模式从 token 转向持续服务

文章最后的商业判断是：真正成功的 Agent 公司不应只是卖 token，而应把一次性的推理成本沉淀为可复用、可在线运行、边际成本可摊薄的服务。

Agent 把过去不经济的长尾需求释放出来，最终像一家目标用户群扩大 100 倍、1000 倍的云服务公司。底层仍然可能是数据库、文件系统、云服务这些传统能力，只是使用者从人变成了 Agent。

## 与已有知识的关联

- [[agent-native-infrastructure]] — 本文贡献心智模型、接口、日抛工作负载、虚拟化和商业模式视角。
- [[20260518-agent-infra-runtime-layer]] — runtime / Box / scheduler 是本文“日抛 + 并行 + 隔离”的系统实现方向。
- [[20260518-kimi-agent-infra-database-service]] — Kimi + TiDB 是低成本虚拟化数据库的案例。
- [[llm-wiki-stack]] — wiki 本身也沿用文件系统和 Markdown 这类稳定心智模型，而不是发明新数据库。

## 可迁移洞见

1. 给 Agent 用的软件，优先贴近古老、稳定、训练语料充足的抽象。
2. 自然语言可以是入口，但必须尽快冻结成代码、SQL、配置等确定性表示。
3. Agent-native infra 的默认工作负载是短生命周期、高数量、低频访问、仍需在线。
4. “看起来独占，实际上虚拟化”会成为 Agent Infra 的基础设计模式。

## 来源

- 原文：https://mp.weixin.qq.com/s?__biz=Mzg5NTc0MjgwMw==&mid=2247521814&idx=1&sn=49ceeed78a26438ade5d5b706623e88f&scene=21&poc_token=HOOMCmqjpnEmeKZEdCsRwviMhZYyLg_aQdW3I0AX
- 剪藏：[[../Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？.md]]

