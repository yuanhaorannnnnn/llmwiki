---
title: "为什么我不 Vibe Code：摩擦、责任与 Essential Complexity"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, agents, methodology, safety]
sources: ["raw/articles/20260518-why-i-dont-vibe-code.md"]
source_url: https://jacobharr.is/personal/i-dont-vibe-code
confidence: medium
rating: 6
---

# 为什么我不 Vibe Code：摩擦、责任与 Essential Complexity

## 核心观点

这篇文章不是反对所有 LLM coding，而是反对把 vibe coding 当作消除软件开发摩擦的终极答案。作者的核心判断是：LLM 能降低 accidental complexity，但软件真正困难的部分是 essential complexity，包括抽象设计、数据解释、团队协作、责任承担和对系统后果的判断。

它和 [[claude-code-harness]] 形成有效张力：Harness 让 agentic coding 更可控、更高效，但这篇文章提醒我们，真正危险的不是模型写不出代码，而是团队把“摩擦”误判为必须移除的低效环节。它背后的理论源头是 Brooks 的 [[essential-vs-accidental-complexity]] 区分。

## 关键要点

### 1. AI 主要压缩 accidental complexity，不会消灭 essential complexity

作者借 Fred Brooks 的 “No Silver Bullet” 区分两类复杂度：accidental complexity 是写代码、记 API、做重复实现的复杂；essential complexity 是如何为真实世界建立合适抽象、权衡约束、做可维护设计的复杂。

Vibe coding 对前者很有效：查 ImageMagick 参数、生成样板代码、快速改 UI 都可以交给模型。但如果问题本身是“这个系统该如何抽象”，模型的输出只能反映 prompt 和上下文，不能替代设计判断。

这与 [[20260512-tdd-not-ai-native]] 的结论同向：AI 可以在约束内探索路径，但边界、invariants 和价值判断必须由人定义。

### 2. 抽象必然遮蔽现实，LLM 更容易把遮蔽当成现实

作者从 “Seeing Like a State” 引出一个数据系统问题：程序员为了构建系统，必须把真实世界压缩成表单、字段、枚举、数据库约束。这不是错误，但每个抽象都会遮蔽一部分现实。

LLM 的问题在于它更难意识到自己的视角边界。它看到的是 tokenized text，而不是完整社会语境、数据收集过程、字段缺失原因、组织历史和专家知识。用它做数据分析或高风险系统判断时，最大的风险不是算错，而是过早相信简化后的表象。

这个视角可以补充 [[20260518-claude-code-tool-design-seeing-like-agent]]：工具设计要 seeing like an agent，但系统设计也要反过来识别 agent 看不见什么。

### 3. Friction 是架构坏味道和学习过程，不只是效率损耗

作者最有价值的洞见是 “friction is a gift”。当代码写得困难、理解代码库很慢、重构让人痛苦时，这些摩擦经常是在暴露架构方向、抽象边界或上下文理解的问题。

如果团队用 agent 一路把摩擦“写穿”，很可能得到能跑、测试过、但抽象奇怪的系统。几年后留下来的设计文档可能只是一份当时喂给模型的 Markdown prompt，而不是能解释权衡的 Architecture Decision Record。

对 [[claude-code-harness]] 来说，这意味着 harness 不应该只优化吞吐量，还应该保留 `/plan`、ADR、review、rewind、human checkpoint 这类让人重新思考的停顿点。

### 4. Vibe coding 成功案例常依赖专家操盘或低失败成本

作者观察到，很多成功的 vibe coding 故事来自两类场景：

- 操作者本来就是专家，知道怎样评估模型输出。
- 失败成本低，产品是否长期可维护不重要。

这解释了为什么 [[20260518-claude-code-code-review]] 这种 review layer 重要：当 AI 代码量上升，瓶颈不是生成，而是判断“the rest of the owl” 是否真的正确、安全、可维护。

### 5. 责任不能外包给模型

作者在数据新闻和 civic technology 背景下强调 accountability：错误代码可能带来更正、诉讼，甚至影响公共服务和弱势群体。LLM 没有 conscience，不能被问责，也不会因为错误而真正承担后果。

因此，AI coding 的组织问题不是“谁写了代码”，而是“谁对代码后果负责”。这和 [[20260518-claude-code-auto-mode]] 的 permission layer、[[20260518-claude-code-code-review]] 的 review gate 形成互补：权限和审查不是保守阻力，而是责任链条的一部分。

## 可迁移洞见

- 不要把所有 friction 都当作低效；先判断它是不是架构信号、知识缺口或责任边界。
- 对高风险代码，AI 输出必须进入人类可解释的设计记录、review 和 invariant 检查，而不是只留下 prompt。
- Agentic coding 的最佳场景不是“人不懂也能做”，而是“懂的人把重复实现和搜索交给工具”。
- 组织采用 AI coding 时，应显式保护产品、设计、QA、合规、用户研究等协作摩擦，因为这些摩擦常常是质量控制。

## 相关笔记

- [[claude-code-harness]]
- [[essential-vs-accidental-complexity]]
- [[20260512-tdd-not-ai-native]]
- [[20260518-claude-code-tool-design-seeing-like-agent]]
- [[20260518-claude-code-code-review]]
- [[20260518-claude-code-auto-mode]]
- [[agent-native-infrastructure]]

## 来源

- 原文：https://jacobharr.is/personal/i-dont-vibe-code
- 原始文本：[[../raw/articles/20260518-why-i-dont-vibe-code.md]]
