---
title: "Claude Code Harness"
created: 2026-05-18
updated: 2026-05-18
type: concept
tags: [concept, agents, architecture, methodology]
sources:
  - "Clippings/How Claude Code works in large codebases Best practices and where to start.md"
  - "Clippings/Lessons from building Claude Code Prompt caching is everything.md"
  - "Clippings/Using Claude Code session management and 1M context.md"
  - "Clippings/Seeing like an agent how we design tools in Claude Code.md"
  - "Clippings/How and when to use subagents in Claude Code.md"
  - "Clippings/Onboarding Claude Code like a new developer Lessons from 17 years of development.md"
  - "Clippings/Best practices for using Claude Opus 4.7 with Claude Code.md"
  - "Clippings/Auto mode for Claude Code.md"
  - "Clippings/Code Review for Claude Code.md"
confidence: high
rating: 7
---

# Claude Code Harness

## 定义

Claude Code Harness 是围绕 Claude 模型构建的工程运行体系：它通过 context、prompt caching、tool design、skills、subagents、session management、permissions、MCP、LSP、code review 等层，把模型能力转化为可在真实代码库中长期运行的 agentic coding system。

这个概念的核心是：Claude Code 的效果不是模型单独决定的，而是模型 + harness 共同决定。Harness 决定 Claude 看见什么、如何行动、什么时候分叉、如何保持上下文干净、怎样审查结果，以及如何在组织里被稳定采用。

## 当前知识状态

Anthropic 这批 blog 形成了一个完整操作系统：

- 大代码库导航：[[20260518-claude-code-large-codebases-best-practices]]
- Prompt caching：[[20260518-claude-code-prompt-caching]]
- Session/context：[[20260518-claude-code-session-management-1m-context]]
- Tool design：[[20260518-claude-code-tool-design-seeing-like-agent]]
- Subagents：[[20260518-claude-code-subagents]]
- Onboarding/context layer：[[20260518-onboarding-claude-code-like-new-developer]]
- Model tuning：[[20260518-claude-opus-4-7-code-best-practices]]
- Permissions：[[20260518-claude-code-auto-mode]]
- Review：[[20260518-claude-code-code-review]]

## 核心原则

### 1. Stable prefix is product architecture

Prompt caching 是 prefix match，因此 system prompt、tools、`CLAUDE.md`、session context 的顺序和稳定性是产品架构问题，不是 API 小优化。Plan Mode、tool search、compaction 都要围绕缓存约束设计。

### 2. Context is maintained, not wished into existence

Claude 不能自动继承一个组织 17 年的隐性知识。`CLAUDE.md`、skills、MCP、project docs、context repo 都是 onboarding Claude 的材料。Context layer 应像代码一样 versioned、grown、maintained。

### 3. Search beats stale retrieval when code is live

大代码库里 RAG 索引容易过期。Claude Code 更依赖 agentic search：读文件、grep、LSP、沿引用追踪。前提是代码库要可导航，且 harness 给出起始方向。

### 4. Tool design must see like an agent

好工具不是人觉得优雅，而是模型能稳定理解和调用。结构化交互用 tool schema，条件知识用 progressive disclosure，成熟专家流程用 skills / subagents。模型升级后，旧工具可能变成约束。

### 5. Context hygiene needs branching primitives

`/clear`、`/rewind`、`/compact`、subagents 是上下文分支和裁剪工具。大任务不是无限延长一个 session，而是持续判断哪些内容应该留在 parent context，哪些应该进入 child context 或 summary。

### 6. Autonomy needs permission and review layers

Auto Mode 减少执行打断，但需要 classifier 守住危险操作。Code Review 用多 agent 深读 PR，把 AI 代码产量放大后的 review bottleneck 转化为组织级 quality gate。

## 参考结构

```text
┌────────────────────┐
│ Model / Effort      │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Stable Prompt Prefix│
│ System + Tools      │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Context Layer       │
│ CLAUDE.md + Skills  │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Tool + Search Layer │
│ Grep + LSP + MCP    │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Branching Layer     │
│ Rewind/Compact/Subs │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Safety + Review     │
│ Auto Mode + PR Rev  │
└────────────────────┘
```

## 与现有知识的关系

- [[agent-native-infrastructure]] — Claude Code Harness 是 coding agent 场景下的 agent-native runtime 轻量实现。
- [[20260512-perplexity-agent-skills-design]] — skill progressive disclosure 与 route description 的外部方法论。
- [[deep-research-agents]] — long-horizon agent 需要 control/context structure；Claude Code Harness 是工程实现版本。
- [[20260512-tdd-not-ai-native]] — Claude Code Code Review 和 verification layer 是 AI coding 时代测试之外的质量控制。

## 开放问题 / 争议

- 个人用户是否应该把 `CLAUDE.md`、skills、hooks、subagents 抽成独立 “AI context repo”？
- Code Review 的 $15-25/PR 成本在个人项目里是否值得，还是只适合高价值 repo？
- Auto Mode 的 classifier 能否表达项目级风险偏好，还是仍需外层 sandbox？
- Claude Code Harness 与更通用的 [[agent-native-infrastructure]] 会在多大程度上合流？

## 来源

- [[../Clippings/How Claude Code works in large codebases Best practices and where to start]]
- [[../Clippings/Lessons from building Claude Code Prompt caching is everything]]
- [[../Clippings/Using Claude Code session management and 1M context]]
- [[../Clippings/Seeing like an agent how we design tools in Claude Code]]
- [[../Clippings/How and when to use subagents in Claude Code]]
- [[../Clippings/Onboarding Claude Code like a new developer Lessons from 17 years of development]]
- [[../Clippings/Best practices for using Claude Opus 4.7 with Claude Code]]
- [[../Clippings/Auto mode for Claude Code]]
- [[../Clippings/Code Review for Claude Code]]

