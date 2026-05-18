---
title: "Claude Code Session Management 与 1M Context"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, memory, methodology]
sources: ["Clippings/Using Claude Code session management and 1M context.md"]
source_url: https://claude.com/blog/using-claude-code-session-management-and-1m-context
confidence: high
rating: 7
---

# Claude Code Session Management 与 1M Context

## 核心观点

1M context 不等于可以无限延长一个 session。Context window 越大，越需要主动管理 context rot：文件读取、工具输出、探索分支、失败尝试都会留在上下文里，逐渐稀释当前任务信号。

Claude Code 的 session 管理本质是一组分支选择：continue、rewind、clear、compact、subagents。每个 turn 都是分叉点。

## 关键要点

### 1. 新任务通常新 session

官方 rule of thumb：开始新任务时，也应开始新 session。相关任务可以沿用上下文，例如实现后直接写文档；但真正不同的任务应 `/clear`，避免 context rot。

### 2. Rewind 优于继续纠正

如果 Claude 读了五个文件后走错方向，直接说“这不对，再试 X”会把错误路径留在上下文里。更好的方式是 `/rewind` 到有用文件读取之后，丢掉错误尝试，再带着新约束重 prompt。

这类似让“未来试错失败的 Claude”给“过去刚读完文件的 Claude”写 handoff message。

### 3. Compact 与 Clear 的差异

`/compact` 让模型总结当前 session 并继续。它省力但有损，且 autocompact 发生时模型可能正处于 context rot 最严重的时刻。

`/clear` 是你自己提炼 carry-over 信息后开新 session。它更费力，但上下文完全由你控制。

### 4. Subagents 保持 parent context 干净

当下一步会产生大量中间输出，而最终只需要结论时，用 subagent。Anthropic 的心智测试是：我之后还需要这些 tool output，还是只需要 conclusion？

典型场景：

- 让 subagent 验证实现。
- 让 subagent 读另一个 codebase 并总结模式。
- 让 subagent 基于 git changes 写 docs。

## 决策表

| 情况 | 选择 |
| --- | --- |
| 同一任务且上下文仍相关 | Continue |
| Claude 走错路 | Rewind |
| 中途上下文膨胀但任务没变 | `/compact <hint>` |
| 开始真正新任务 | `/clear` |
| 下一步中间输出很多，只要结论 | Subagent |

## 相关笔记

- [[claude-code-harness]]
- [[20260518-claude-code-prompt-caching]]
- [[20260518-claude-code-subagents]]
- [[deep-research-agents]]

## 来源

- 原文：https://claude.com/blog/using-claude-code-session-management-and-1m-context
- 剪藏：[[../Clippings/Using Claude Code session management and 1M context.md]]

