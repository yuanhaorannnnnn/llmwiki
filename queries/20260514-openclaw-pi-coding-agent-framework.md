---
title: "OpenClaw 背后框架 Pi：好的 Coding Agent 应该让用户决定需要什么"
created: 2026-05-14
updated: 2026-05-18
type: query
tags: [article, wechat, coding-agent, framework, developer-tools]
sources: [raw/articles/wechat_2_BKJq0HIe7TpsUUaT6mzSKA.md]
source_url: https://mp.weixin.qq.com/s/BKJq0HIe7TpsUUaT6mzSKA
confidence: medium
---

# OpenClaw 背后框架 Pi：好的 Coding Agent 应该让用户决定需要什么

## 核心观点

OpenClaw 的核心框架 Pi 的设计哲学：**让用户定义"需要什么"，而不是让 Agent 猜测你需要什么。** 与当前主流 Agent 框架（自动拆解任务、自动决策路径）相反，Pi 强调保留用户在关键决策点的主动性——Agent 负责执行，用户负责定义范围和验收标准。

## 关键要点

- Pi 框架与 Anthropic Barry 的 "Keep it simple" 完全一致：Agent = Environment + Tools + System Prompt 的循环即可，不需要复杂的任务规划引擎
- 核心差异化：用户的判断力不可替代——Agent 不该替用户决定"需要什么"

## 与已有知识的关联

- `queries/20260514-barrystop-agent-three-iron-rules.md` — Barry 的第二条铁律（Keep it simple）在此得到独立验证
- `queries/20260512-tdd-not-ai-native.md` — "人定义边界约束，AI 在护栏内探索"与此同构

## 相关笔记
- [[20260518-pi-coding-agent-goal-open-model-harness]] — Pi Coding Agent 最全面指南：面向开放模型的可拆卸 Agent Harness
- [[claude-code-practical-tips-note]] — Claude Code 实用技巧——官方核心开发者现场演示
- [[20260515-raycast-v2-technical-deep-dive]] — Raycast v2 跨平台重写技术深潜：自建 Hybrid 栈的决策与细节
- [[20260515-boris-cherny-opus-4-7-tips]] — Boris Cherny Opus 4.7 实操六条：从 Auto Mode 到自验证循环

## 来源

- 原文：[[raw/articles/wechat_2_BKJq0HIe7TpsUUaT6mzSKA.md]]
