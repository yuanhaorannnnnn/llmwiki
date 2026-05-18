---
title: "Anthropic 多 Agent 研究系统：从原型到生产的工程实战手册"
created: 2026-05-11
updated: 2026-05-11
type: query
tags: [article, multi-agent, prompt-engineering, evaluation, anthropic, agent-ops]
sources: [Clippings/How we built our multi-agent research system.md]
source_url: https://www.anthropic.com/engineering/multi-agent-research-system
confidence: high
---

# Anthropic 多 Agent 研究系统：从原型到生产的工程实战手册

![架构图](raw/articles/images/20260511-how-we-built-our-multi-agent-research-system/image.png)

## 核心观点

Anthropic 把 Claude Research 从原型做到生产级多 Agent 系统，核心发现是：**多 Agent 架构的价值不在"让 Agent 协作"，在于通过平行上下文窗口增加 token 预算**。token 用量解释了 BrowseComp 80% 的性能方差。工程上最反直觉的教训是——Agent 系统的原型到生产鸿沟比传统软件大得多，因为错误会非线性和级联放大。

## 关键要点

1. **Orchestrator-worker 架构：Opus 4 lead + Sonnet 4 subagents = +90.2% 的单 Agent 性能**
   不是让 Agent 互相聊天。模式：一个 lead agent 分析 query→制定策略→并行 spawn subagents（每个有独立的 context window/tools/prompt）→等全部返回→编译最终答案。subagents 充当"智能过滤器"，在自己的上下文里独立搜索、压缩信息，只把最关键的 token 传回 lead。适合广度优先查询（同时探索多个独立方向）。**不适合**：所有 agent 需要共享上下文、子任务间有大量依赖（如大部分 coding 任务）。

2. **Token 预算是最强杠杆：80% 性能方差来自 token 用量，多 Agent 吃 15× token**
   BrowseComp 评测中三因素解释 95% 方差：token 用量（80%）、工具调用次数、模型选择。多 Agent 通过独立上下文窗口增加并行推理容量。Sonnet 4 升级 > Sonnet 3.7 翻倍 token 预算。代价：单 Agent ≈ 4× chat token，多 Agent ≈ 15× chat token。只对任务价值够高的场景经济可行。

3. **Prompt agent 用启发式策略，不用僵硬规则——但必须加硬 guardrail**
   把优秀人类研究者的策略编码进 prompt：什么时候深度挖一个主题（depth）、什么时候广撒网（breadth）、怎么评估来源质量、怎么根据中间发现调整搜索方向。同时加硬约束防止灾难：最大 subagent 数、搜索轮次上限、超时 kill。早期系统犯过的错误：为简单查询 spawn 50 个 subagent，满网找不存在的来源，subagent 之间过度更新互相干扰。

4. **Agent 评测三板斧：20 个 case 起步 → 单 LLM judge 5 维度打分 → 人工抽查**
   - **起步**：初期改动效果大（prompt tweak 30%→80%），20 个代表性 case 就能看到变化。不要等凑够几百个。
   - **LLM judge**：一个 prompt 输出 5 维度 0.0-1.0 分（事实准确性、引用准确性、完整性、来源质量、工具效率）+ pass/fail。**单个 judge 比多个 judge 更一致**——多 judge 实验结果反而不稳定。
   - **人工**：自动化测不出 source bias。早期 Agent 总是选 SEO 内容农场而非学术 PDF——人工测试才发现，加了 source quality heuristics 解决。
   - **End-state 评测**（附录补充）：对有状态的 agent，不看中间步骤对不对，看最终状态对不对。复杂流程拆成离散 checkpoint 而非逐步验证。

5. **长上下文管理：总结→存外部存储→spawn 带干净上下文的 subagent**
   对话到几百轮时：让 agent 把已完成阶段总结成结构化摘要 → 存入外部存储 → spawn 新 subagent 带干净上下文 → 通过 handoff 传递引用 → 新 agent 从外部存储拉回 research plan 等关键信息。这直接防止 context overflow，同时保持对话连贯性。

6. **Subagent→文件系统→轻量引用模式，防"传话游戏"式信息损失**
   subagent 产生的结构化输出（代码、报告、可视化）直接写到外部存储。只把轻量引用（路径/handle）传回 lead agent。不要在大段 conversation history 里反复拷贝输出。subagent 的专用 prompt 生成的代码/报告往往比通过通用 coordinator 过滤后的质量更高。

7. **Agent 错误处理：支持 resume + 把工具失败告诉 agent 让它自适应**
   不能从头 restart——太贵，用户等不起。在出错点建立 resume。当工具调用失败时，把错误信息直接告诉 agent（"search 暂时不可用，试试 browse 或跳过这个子问题"），让模型自己决策。叠加确定性保障：retry logic + 定期 checkpoint。生产部署用 rainbow deployment——逐步切流量，新旧版本并行，不打断正在运行的 agent。

## 行动建议

1. 构建多 Agent 系统时，先用 orchestrator-worker 模式——不要一上来就 agent 间自由通信
2. 把 token 预算当第一性能杠杆：先加并行上下文窗口，再考虑换模型
3. Agent 评测：立刻建一个 20 条查询的小测试集，用单个 LLM judge prompt 做 5 维度打分
4. 写 agent prompt 时编码"优秀人类怎么做"的启发式策略，但加硬 guardrail（上限、超时）
5. 生产部署：工具调用层外包 retry+checkpoint；出错了把错误信息传给 agent 而非静默重试
6. 用 subagent→filesystem→reference 模式替代 subagent→coordinator→copy 模式

## 相关笔记
- [[deep-research-agents]] — Deep Research Agents
- [[20260518-claude-code-large-codebases-best-practices]] — Claude Code 在大代码库中的工作方式：企业级部署最佳实践
- [[20260514-264page-agent-survey]] — 264 页 Agent 综述：MetaGPT、Mila、斯坦福、耶鲁、谷歌联合撰写
- [[kimi-k2-5-tech-blog-visual-agentic-intelligence]] — Kimi K2.5 的 Agent Swarm：用 PARL 训练并行编排器的工程细节
- [[20260514-barrystop-agent-three-iron-rules]] — Barry Zhang (Anthropic) AI Engineer Summit：如何构建高效 Agent 的三条铁律
- [[20260512-perplexity-agent-skills-design]] — Perplexity Agent Skills 设计与维护方法论

## 来源

- 原文：https://www.anthropic.com/engineering/multi-agent-research-system
- 原始文本：[[Clippings/How we built our multi-agent research system.md]]
- 图片：[[raw/articles/images/20260511-how-we-built-our-multi-agent-research-system/image.png]] [[raw/articles/images/20260511-how-we-built-our-multi-agent-research-system/image-1.png]] [[raw/articles/images/20260511-how-we-built-our-multi-agent-research-system/image-2.png]]
