---
title: "Seeing like an agent：Claude Code 工具设计方法"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, tool-use, methodology]
sources: ["Clippings/Seeing like an agent how we design tools in Claude Code.md"]
source_url: https://claude.com/blog/seeing-like-an-agent
confidence: high
rating: 7
---

# Seeing like an agent：Claude Code 工具设计方法

## 核心观点

设计 agent tools 的关键不是“人觉得这个工具好不好”，而是模型是否能理解、愿意调用、能稳定产出正确结构。Anthropic 把这称为 seeing like an agent：读模型输出、实验、观察它如何使用工具，并随着模型能力变化重新评估工具是否还在帮忙。

## 关键要点

### 1. Tool 设计要贴合模型能力

给 agent 一个通用 bash/code execution，还是给五十个专用工具，取决于模型自身能力和任务环境。工具太少，模型手算困难；工具太多，模型每一步都多一个选择负担。

### 2. AskUserQuestion 的三次迭代

为了降低 Claude 向用户提问的摩擦，团队尝试过：

- 在 `ExitPlanTool` 里加 questions 参数：计划和问题混在一起，语义冲突。
- 让 Claude 输出特定 Markdown 格式：模型不够稳定，会多写句子、漏选项、破坏格式。
- 独立 `AskUserQuestion` tool：Claude 可随时调用，UI modal 阻塞 agent loop，结构化 options 稳定。

结论：需要结构化 UI / block loop 的交互，应该是 tool，而不是自然语言格式约定。

### 3. 从 TodoWrite 到 Task tool

早期 Claude 需要 todo list 保持目标；后续模型能力提升后，todo reminders 反而让 Claude 过度拘泥旧计划。团队将 TodoWrite 替换为 Task tool，支持 dependencies、跨 subagent 更新、修改和删除。

这说明工具会随模型能力变化从“辅助”变成“束缚”。需要定期审查。

### 4. 从 RAG 到 Grep：让 Claude 自己找上下文

Claude Code 早期内部版本用 RAG 预索引代码库，但 RAG 要求 setup、对环境脆弱，而且模型是被动拿 context。改用 Grep 后，Claude 能像工程师一样主动搜索、读文件、构建上下文。

这和 [[20260518-claude-code-large-codebases-best-practices]] 的 Agentic Search 论点一致。

### 5. Progressive disclosure 优先于新增工具

Claude Code 约有 20 个工具，新增工具门槛很高。对于 Claude Code 自身文档问答，团队没有把所有 docs 放入 system prompt，也没有加大量工具，而是做 Claude Code Guide subagent：主 agent 只得到答案，doc search 留在子上下文。

## 可迁移洞见

- 工具不是越多越好；每个工具都是模型 action space 的新分支。
- 如果输出格式必须稳定，别只靠 markdown prompt，做成 tool schema。
- 随模型升级，过去必要的工具可能变成限制。
- Search capability 是 agent 自主构建 context 的核心能力。

## 相关笔记

- [[claude-code-harness]]
- [[20260518-claude-code-prompt-caching]]
- [[20260518-claude-code-subagents]]
- [[20260512-perplexity-agent-skills-design]]
- [[20260518-claude-code-large-codebases-best-practices]]

## 来源

- 原文：https://claude.com/blog/seeing-like-an-agent
- 剪藏：[[../Clippings/Seeing like an agent how we design tools in Claude Code.md]]

