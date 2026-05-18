---
title: "Agent-native Infrastructure"
created: 2026-05-18
updated: 2026-05-18
type: concept
tags: [concept, agents, architecture, platform]
sources:
  - "Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？.md"
  - "Clippings/当我们在谈论 Agent Infra 时我们在谈论什么.md"
  - "Clippings/Agent Infra 实践复盘：Kimi 如何搭建 Agent 背后的 Database 服务.md"
confidence: medium
rating: 7
---

# Agent-native Infrastructure

## 定义

Agent-native Infrastructure 是面向 AI Agent 而不是人类开发者设计的基础设施层。它位于模型 inference 之上，负责让 Agent 稳定执行动作、隔离副作用、并行探索、管理上下文和状态，并把一次性推理结果沉淀为可持续运行的服务。^[Clippings/当我们在谈论 Agent Infra 时我们在谈论什么.md]

它不是新的训练框架，也不是单纯的 tool calling。更准确地说，它是 Agent 的 runtime：给每个 action 一个可复现、可丢弃、可调度、可回放的执行环境，并让大量短生命周期、低访问频率但仍需在线的 Agent workload 以极低成本存在。^[Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？.md]

## 当前知识状态

三篇 clipping 形成了一条完整链路：

- `如何做 AI Agent 喜欢的基础软件` 给出设计原则：稳定心智模型、自然语言入口、符号化中间表示、日抛 workload、虚拟化和低成本。
- `当我们在谈论 Agent Infra 时我们在谈论什么` 给出 runtime 抽象：`Skill + Env = Box`，以及 Agent 版 Kubernetes 所需的 Context Manager、Branching、Messaging、Scheduler、Box Runtime。
- `Kimi 如何搭建 Agent 背后的 Database 服务` 给出落地案例：TiDB Cloud 通过虚拟数据库界面，为海量 Kimi Agent 站点提供看似独立、底层共享的 database service。

这三者合在一起的“火花”是：Agent Infra 的核心不是让模型更聪明，而是让 Agent 的试错更便宜、环境更可控、状态更可隔离、服务更可持续。

## 核心原则

### 1. 使用模型已经懂的心智模型

Agent 更喜欢文件系统、shell、SQL、Python、进程、I/O 这类古老稳定的抽象。它们在训练语料中出现充分，语义边界清楚，组合方式成熟。为 Agent 设计基础软件时，优先顺应这些稳定抽象，而不是发明全新范式。^[Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？.md]

### 2. 自然语言负责表达意图，符号系统负责执行

自然语言适合让 Agent 表达或理解用户意图，但执行前必须收敛到确定性中间表示，例如代码、SQL、配置或脚本。一个 Agent-friendly 系统必须回答：歧义在什么时刻被消除，结果如何验证。^[Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？.md]

### 3. Action 必须拥有可丢弃环境

长程任务中的副作用会污染环境。Coding Agent 的 worktree、多 Agent 的 sandbox、浏览器自动化的会话状态，本质都需要一个可复现、可丢弃的执行环境。`Box` 抽象把 Skill 和 Env 绑定起来，让 action 在语义上可调用，在系统上可隔离。^[Clippings/当我们在谈论 Agent Infra 时我们在谈论什么.md]

### 4. 虚拟独占，物理共享

Agent 需要感觉自己拥有独立数据库、独立文件系统、独立 sandbox，可以自由建表、删表、试错和回滚。但平台不能真的为每个长尾任务分配完整实例。可规模化的方案是资源层共享、语义层隔离，即“看起来独占，实际上虚拟化”。^[Clippings/Agent Infra 实践复盘：Kimi 如何搭建 Agent 背后的 Database 服务.md]

### 5. 并行探索是基础设施能力

复杂任务不是单轮对话，而是并行探索。Agent Infra 需要支持快速创建大量 worker / Box / sandbox，分发任务、收敛结果、去重、纠错、回放失败，并提供实时成本可见性。这个方向接近 Agent 版 Kubernetes + Hadoop。^[Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？.md]

## 参考架构

```text
┌────────────────────┐
│ User Intent         │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Agent / Planner     │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Box Runtime         │
│ Skill + Env         │
└────┬──────────┬────┘
     │          │
     ▼          ▼
┌──────────┐  ┌──────────────┐
│ Branches │  │ Message Hub  │
└────┬─────┘  └──────┬───────┘
     │               │
     ▼               ▼
┌────────────────────────────┐
│ Scheduler + Lifecycle      │
└────────────┬───────────────┘
             ▼
┌────────────────────────────┐
│ Virtual Storage / Database │
└────────────┬───────────────┘
             ▼
┌────────────────────────────┐
│ Shared Physical Resources  │
└────────────────────────────┘
```

## 与现有知识的关系

- [[20260518-agent-infra-runtime-layer]] — runtime / Box / scheduler 的理论描述。
- [[20260518-ai-agent-friendly-infrastructure]] — 心智模型、接口设计、虚拟化和商业模式。
- [[20260518-kimi-agent-infra-database-service]] — Kimi + TiDB Cloud 的 database service 案例。
- [[deep-research-agents]] — 关注 long-horizon research agent 的控制结构；本页关注执行环境和运行时。
- [[kimi-k2-5-tech-blog-visual-agentic-intelligence]] — PARL / Agent Swarm 说明并行探索需要被训练和度量，本页补充其 infra 前提。
- [[20260518-claude-code-large-codebases-best-practices]] — Claude Code harness 是 coding agent 的轻量 runtime 配置层。

## 开放问题 / 争议

- `Box` 和现有 Docker / Firecracker / browser sandbox / cloud workspace 的边界是什么？
- Agent-native database 是否会走 TiDB 式虚拟数据库，还是 Neon/Supabase 式 serverless Postgres 会补齐隔离和成本问题？
- Agent Infra 的收费单位应该是 token、Box runtime、持久服务、状态量，还是任务成功价值？
- 如果 Agent 可以无限并行试错，治理、权限和成本上限应该如何表达为可验证 contract？

## 来源

- [[../Clippings/创业者思考：如何做 AI Agent 喜欢的基础软件？]]
- [[../Clippings/当我们在谈论 Agent Infra 时我们在谈论什么]]
- [[../Clippings/Agent Infra 实践复盘：Kimi 如何搭建 Agent 背后的 Database 服务]]

