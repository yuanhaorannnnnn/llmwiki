---
title: "Claude Code Code Review：多 Agent 深度 PR 审查"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, evaluation, safety]
sources: ["Clippings/Code Review for Claude Code.md"]
source_url: https://claude.com/blog/code-review
confidence: high
rating: 6
---

# Claude Code Code Review：多 Agent 深度 PR 审查

## 核心观点

Claude Code Code Review 是 Anthropic 内部几乎每个 PR 都运行的多 agent review 系统。它不是为了快速 rubber stamp，而是为了做深度审查：并行找 bug、验证 bug、过滤 false positives、按严重程度排序，再把高信号结果写回 PR。

## 关键要点

### 1. Review bottleneck 被 AI 代码产量放大

Anthropic 工程师 code output 一年增长 200%，review 成为瓶颈。人类 reviewer 容易 skim，深读覆盖不够。Code Review 的目标是补上这个缺口，但最终 approve 仍然是人类决定。

内部数据：使用前 16% PR 有 substantive review comments，使用后 54% 有。

### 2. 多 Agent 深读而非单 Agent 快速扫

PR 创建后，系统 dispatch 一组 agents：

- 并行找 bugs。
- 验证 bugs，减少误报。
- 按 severity 排序。
- 输出一个 overview comment 和具体 inline comments。

Review 深度随 PR 大小和复杂度扩展。平均 review 约 20 分钟。

### 3. 成本换深度

Code Review 比 Claude Code GitHub Action 更贵，平均约 $15-25，按 PR 大小和复杂度扩展。管理员可设置月度组织 caps、仓库级启用、analytics dashboard。

### 4. 实测价值

内部大 PR（1000+ 行）84% 有 findings，平均 7.5 个问题；小 PR（50 行以下）31% 有 findings，平均 0.5 个问题。少于 1% findings 被标记 incorrect。

典型价值是发现人类快速扫 diff 会漏掉的关键 bug，甚至能发现 PR 邻近代码里的 latent issue。

## 与已有知识的关联

- [[20260518-claude-code-subagents]] — Code Review 是 review 场景下的多 subagent 产品化。
- [[20260518-claude-code-large-codebases-best-practices]] — 大代码库 adoption 需要把 review process 纳入治理。
- [[20260512-tdd-not-ai-native]] — AI 时代 verification 不应只靠测试绿，应有更强结果审查和 invariants。
- [[claude-code-harness]] — Code Review 是 harness 的组织级 quality gate。

## 来源

- 原文：https://claude.com/blog/code-review
- 剪藏：[[../Clippings/Code Review for Claude Code.md]]

