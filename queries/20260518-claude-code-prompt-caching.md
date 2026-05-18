---
title: "Claude Code 构建经验：Prompt Caching 是一切"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, architecture, optimization]
sources: ["Clippings/Lessons from building Claude Code Prompt caching is everything.md"]
source_url: https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything
confidence: high
rating: 7
---

# Claude Code 构建经验：Prompt Caching 是一切

## 核心观点

长时间运行的 agent 产品能成立，很大程度依赖 prompt caching。Claude Code 的整个 harness 都围绕缓存命中率设计：缓存命中降低延迟和成本，也直接影响订阅制产品能给用户多慷慨的 rate limit。

这篇文章最重要的工程约束是：prompt caching 是 prefix match。任何改变 cached prefix 的行为，包括系统提示顺序、工具列表、模型、工具 schema、时间戳，都可能让整段上下文重新计费。

## 关键要点

### 1. 静态内容前置，动态内容后置

Claude Code 的缓存友好顺序是：

```text
Static system prompt + tools
  → CLAUDE.md
  → session context
  → conversation messages
```

稳定内容越靠前，跨 session、跨项目、跨 turn 复用越多。破坏缓存的典型错误包括：在 static system prompt 里放精确时间戳、非确定性打乱 tool order、会话中更新 tool parameters。

### 2. 用 message 更新状态，不要改 prompt

如果时间、文件变化、环境提醒这类信息变了，优先把更新放进下一条 message 或 tool result。Claude Code 使用 `<system-reminder>` 这类方式把新信息注入消息，而不是改 system prompt。

这和 [[20260518-claude-code-large-codebases-best-practices]] 的 harness 思想一致：系统层稳定，动态信息在消息层流动。

### 3. 不要中途换模型或工具集

Prompt cache 按模型隔离。一个 100k token 的 Opus 会话中切到 Haiku，可能比继续让 Opus 回答更贵，因为 Haiku 要重建缓存。

工具集也一样。中途增删工具会让工具定义这段 cached prefix 失效。Plan Mode 的正确设计不是替换成只读工具集，而是保留完整工具集，用 `EnterPlanMode` / `ExitPlanMode` 作为状态转换工具。

### 4. Defer tool loading，而不是删除工具

Claude Code 有大量 MCP tools 时，不把完整 schema 全塞进每次请求，也不在会话中删工具。做法是固定发送轻量 stub，通过 tool search 在需要时加载完整 schema。

这条和 [[20260518-claude-code-tool-design-seeing-like-agent]] 的 progressive disclosure 是同一个原则：给 agent 发现能力，而不是把全部细节预加载。

### 5. Compaction 必须 cache-safe fork

天真的 compaction 会用一个新的 summarization prompt + no tools 调用模型，这和父会话 prefix 完全不同，会导致整段历史无缓存计费。Claude Code 的做法是用和父会话完全相同的 system prompt、user context、system context、tool definitions，把 compaction prompt 作为末尾新 user message 追加。

因此 compaction 需要预留 buffer，保证同时容纳 compact prompt 和 summary 输出。

## 可迁移洞见

- Agent 产品的成本优化不是事后加缓存，而是从 harness 结构开始围绕缓存设计。
- 工具、模型、system prompt 都是 cached prefix 的一部分，不能按传统 UI 状态随意切换。
- Side computation 如 compaction、summarization、skill execution，也应尽量共享父会话 prefix。

## 相关笔记

- [[claude-code-harness]]
- [[20260518-claude-code-session-management-1m-context]]
- [[20260518-claude-code-tool-design-seeing-like-agent]]
- [[20260518-claude-code-large-codebases-best-practices]]

## 来源

- 原文：https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything
- 剪藏：[[../Clippings/Lessons from building Claude Code Prompt caching is everything.md]]

