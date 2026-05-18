---
title: "Claude Code Auto Mode：少打断但保留安全护栏"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, safety, tool-use]
sources: ["Clippings/Auto mode for Claude Code.md"]
source_url: https://claude.com/blog/auto-mode
confidence: high
rating: 5
---

# Claude Code Auto Mode：少打断但保留安全护栏

## 核心观点

Auto Mode 是 Claude Code 的中间权限模式：比默认每次写文件/跑命令都请求批准少打断，比 `--dangerously-skip-permissions` 风险低。它让 Claude 代表用户做权限决策，但每个 tool call 执行前由 classifier 检查潜在破坏性动作。

## 关键要点

### 1. 目标是支持长任务无人值守

默认权限安全但频繁打断，无法启动长任务后离开。完全跳过权限只适合隔离环境。Auto Mode 试图在两者之间取平衡。

### 2. Classifier 在 tool call 前把关

Classifier 会检查：

- 大规模删除文件
- 敏感数据外传
- 恶意代码执行
- 其他潜在破坏动作

安全动作自动执行，风险动作被 block，Claude 被引导换方法。如果连续被 block，会触发用户权限提示。

### 3. 它降低风险，但不消除风险

官方仍建议在 isolated environments 中使用。Classifier 可能在用户意图不清或环境风险不可见时放过危险动作，也可能误 block 良性动作。它还会带来少量 token、cost、latency 开销。

## 与已有知识的关联

- [[20260518-claude-opus-4-7-code-best-practices]] — Opus 4.7 长任务能力增强后，Auto Mode 更有价值。
- [[20260518-claude-code-subagents]] — Auto Mode 解决权限打断，Subagents 解决上下文隔离和并行。
- [[claude-code-harness]] — Auto Mode 是 permission layer 的一部分。

## 来源

- 原文：https://claude.com/blog/auto-mode
- 剪藏：[[../Clippings/Auto mode for Claude Code.md]]

