---
title: "Claude Code Subagents：何时使用、如何使用"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, methodology]
sources: ["Clippings/How and when to use subagents in Claude Code.md"]
source_url: https://claude.com/blog/subagents-in-claude-code
confidence: high
rating: 7
---

# Claude Code Subagents：何时使用、如何使用

## 核心观点

Subagent 是带独立 context window 的 Claude 实例，用来隔离探索噪声、并行处理独立任务、获得新鲜视角或把 pipeline 阶段拆开。它不是“更多 agent 更好”，而是当 context isolation、parallelism 或 fresh perspective 真正有价值时才值得用。

## 关键要点

### 1. 什么是 subagent

Subagent 独立读取文件、探索代码或修改文件，结束后只把结果返回主会话。它不继承主会话历史和已加载 skills，多个 subagents 可以并行运行，并可有不同权限。

内置类型包括 general-purpose、plan agents、explore agents。

### 2. 适合使用的场景

- Research-heavy tasks：需要读几十个文件才能理解系统，但主会话只需要摘要。
- Multiple independent tasks：多个文件或模块互不依赖，可以并行处理。
- Fresh perspective：review / security / verification 不应继承主会话假设。
- Verification before committing：防止实现过拟合测试或漏边界。
- Pipeline workflows：design → implement → test 这类明确阶段。

经验信号：要探索 10+ 文件，或有 3+ 独立子任务，就值得考虑 subagents。

### 3. 调用方式层级

- Conversational invocation：直接要求 Claude 使用 subagent，说明 scope、parallelization、expected output。
- Custom subagents：放在 `.claude/agents/` 或 `~/.claude/agents/`，定义 name、description、tools、model。
- `CLAUDE.md` policy：规定什么时候必须用 read-only subagent，例如 code review。
- Skills：把复杂可复用流程封装成按需加载的 workflow。
- Hooks：成熟后用事件自动触发，例如 Stop hook 检查测试。

### 4. 不适合使用的场景

Subagents 有启动、token 和协调成本。小任务、强顺序任务、主会话已经有完整上下文时，直接做通常更简单。

## 可迁移洞见

- Subagent 是 context hygiene 工具，不只是并行工具。
- 对 review 类任务，fresh context 往往比更多上下文更有价值。
- 对重复模式，应从手动提示逐步升级为 custom subagent / skill / hook。
- “只返回 summary，不返回 raw file contents” 是保持 parent context 干净的关键输出约束。

## 相关笔记

- [[claude-code-harness]]
- [[20260518-claude-code-session-management-1m-context]]
- [[20260518-claude-code-code-review]]
- [[deep-research-agents]]
- [[kimi-k2-5-tech-blog-visual-agentic-intelligence]]

## 来源

- 原文：https://claude.com/blog/subagents-in-claude-code
- 剪藏：[[../Clippings/How and when to use subagents in Claude Code.md]]

