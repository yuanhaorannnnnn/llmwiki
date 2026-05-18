---
title: "Boris Cherny Opus 4.7 实操六条：从 Auto Mode 到自验证循环"
created: 2026-05-15
updated: 2026-05-15
type: query
tags: [article, claude-code, opus, agent-workflow, tips]
sources: [Clippings/x-thread-boris-cherny-opus-4-7.md]
source_url: https://x.com/bcherny/status/1912766697495101546
confidence: high
---

# Boris Cherny Opus 4.7 实操六条：从 Auto Mode 到自验证循环

## 核心观点

Claude Code 团队成员 Boris Cherny 在深度使用 Opus 4.7 几周后的实操总结。六条建议构成一个完整的 agent 工作流升级路径：**降低摩擦（Auto Mode + Focus Mode + fewer-permission-prompts）→ 提高质量（Effort 调参 + self-verification）→ 持久化（Recaps）**。核心洞察：Opus 4.7 的改进在老工作流中是"nice improvement"，但一旦调整为利用长运行时间和更强 agentic 能力，就是"significant leap"。

## 六条实操

### 1. Auto Mode — 自动审批安全命令
- `Shift-Tab` 进入，权限提示交给模型分类器判断安全性
- 安全命令自动批准，无需人工盯屏
- 核心价值：**可以同时跑多个 Claude 并行任务**——一个跑起来了就切到下一个

### 2. /fewer-permission-prompts
- 扫描历史会话中的 Bash/MCP 命令，识别安全但反复触发权限提示的命令
- 自动生成推荐 allowlist → 添加到 `settings.json`
- 本质：**让系统学习你的安全偏好，减少重复确认**

### 3. Recaps — 会话摘要
- 为配合 Opus 4.7 发布的新功能
- 记录 agent 做了什么 + 下一步是什么
- 用于长时间运行 session 的断点恢复——离开几小时回来能立刻接上
- 对比：我们的 `/save` + `/restore` 是手写版，Recaps 是自动版

### 4. Focus Mode — 只看最终结果
- CLI 中隐藏中间过程，只展示最终产出
- 适用条件：**你已经信任模型会跑正确的命令和编辑**
- 信号：模型质量和可靠性到了可以"不用看过程"的程度

### 5. Effort 调参 — 替代 thinking budgets
- Opus 4.7 用 adaptive thinking 取代固定 thinking budget
- 调整 effort（不是 token 数）：低 effort = 更快响应 + 更省 token；高 effort = 最强智能
- 直觉：不是"你给我想 2000 token"，而是"你多努力想想"

### 6. 给 Claude 一个验证自己输出的方式
- "一直都能让 Claude 产出 2-3x 提升的方法，4.7 时代更重要"
- 不同任务验证方式不同：
  - 后端代码 → 写单元测试 + 跑 CI
  - 前端 → 用 Playwright 截图对比
  - 数据 → 写 assertion check
- **本质就是 TDD 那篇的核心论点——verify state, not behavior**

## 行动建议

- 如果你用 Claude Code Max/Teams/Enterprise，开 Auto Mode 并行跑任务
- 跑一次 `/fewer-permission-prompts` 减少日常摩擦
- 对复杂任务用高 effort，简单任务用低 effort——不是所有场景都需要最强模型
- **建立"Claude 自验证"的习惯**——每次给任务时多花 10 秒想一个问题："Claude 怎么自己验证自己的输出？"

## 与已有知识的关联

- `queries/20260512-tdd-not-ai-native.md` — 第 6 条"自验证"与该文核心论点完全一致
- `queries/20260514-barrystop-agent-three-iron-rules.md` — Barry 的"预算敏感的 Agent"与 Effort 调参同构
- 我们的 `/save` + `/restore` = Recaps 的手写版；我们的 MCP + Bash 自动化 = Auto Mode 的前身

## 相关笔记
- [[claude-code-practical-tips-note]] — Claude Code 实用技巧——官方核心开发者现场演示
- [[20260518-claude-code-large-codebases-best-practices]] — Claude Code 在大代码库中的工作方式：企业级部署最佳实践
- [[20260514-barrystop-agent-three-iron-rules]] — Barry Zhang (Anthropic) AI Engineer Summit：如何构建高效 Agent 的三条铁律
- [[20260512-tdd-not-ai-native]] — TDD 反而不是 AI 时代的答案：从过程确定性到结果确定性

## 来源

- X Thread：https://x.com/bcherny/status/1912766697495101546
