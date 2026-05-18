---
title: "Claude Opus 4.7 与 Claude Code 使用最佳实践"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, model, methodology]
sources: ["Clippings/Best practices for using Claude Opus 4.7 with Claude Code.md"]
source_url: https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code
confidence: high
rating: 6
---

# Claude Opus 4.7 与 Claude Code 使用最佳实践

## 核心观点

Opus 4.7 在 Claude Code 中更适合被当作“可委托的工程师”，而不是需要逐行指导的 pair programmer。它在 ambiguous task、long-running agentic work、bug finding、code review、跨 session context carry 上更强，但也因为 tokenizer 和 adaptive thinking 行为变化，需要重新调整 effort、prompt 和交互节奏。

## 关键要点

### 1. 第一轮给完整任务，比多轮逐步补充更好

Opus 4.7 在 interactive session 中每次用户 turn 后会投入更多 reasoning。好处是长会话更连贯，坏处是多轮零碎补充会增加 token overhead。

推荐在第一轮给清楚：

- intent
- constraints
- acceptance criteria
- relevant file locations
- expected verification

这与 [[20260518-claude-code-prompt-caching]] 的缓存逻辑一致：更少用户 turn，通常更高效。

### 2. `xhigh` 是默认推荐 effort

Opus 4.7 的 Claude Code 默认 effort 是 `xhigh`，介于 `high` 与 `max` 之间。官方建议：

- `medium/low`：低成本、低延迟、范围明确的任务。
- `high`：并发 session 或成本敏感场景。
- `xhigh`：大多数 coding / agentic work。
- `max`：极难任务或 eval 上限测试，容易 overthinking。

### 3. Adaptive thinking 取代固定 thinking budget

Opus 4.7 不支持 fixed thinking budget 的 Extended Thinking，而是 adaptive thinking：模型决定每一步是否需要更多思考。可以用 prompt 调整：

- 更多思考：“Think carefully and step-by-step...”
- 更少思考：“Prioritize responding quickly...”

### 4. 行为变化：更少工具、更少 subagents、更少默认冗长

Opus 4.7 默认回答更随任务复杂度校准，不像 4.6 那么默认 verbose。它也更倾向先 reasoning，再决定是否调用工具；默认 spawn subagents 更谨慎。

如果工作需要大量文件读取、搜索或并行 subagents，需要明确写出触发条件。

## 可迁移洞见

- 模型升级后，旧 harness 不应原封不动迁移；effort、subagent policy、tool-use instructions 都要复核。
- 高能力模型更适合“明确目标后授权执行”，而不是碎片化遥控。
- Auto Mode 和通知适合与 Opus 4.7 的长任务能力组合。

## 相关笔记

- [[claude-code-harness]]
- [[20260515-boris-cherny-opus-4-7-tips]]
- [[20260518-claude-code-auto-mode]]
- [[20260518-claude-code-subagents]]
- [[20260518-claude-code-large-codebases-best-practices]]

## 来源

- 原文：https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code
- 剪藏：[[../Clippings/Best practices for using Claude Opus 4.7 with Claude Code.md]]

