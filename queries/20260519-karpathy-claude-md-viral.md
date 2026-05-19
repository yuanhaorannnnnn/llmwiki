---
title: "Karpathy 的 CLAUDE.md：82,000 Star 的 21 条规则让编码准确率从 65% 到 94%"
created: 2026-05-19
updated: 2026-05-19
type: query
tags: [clipping, claude-code, prompt-engineering, claude-md, karpathy, productivity]
sources: [Clippings/Karpathy's CLAUDE.md hit 1 on GitHub with 82,000 stars. Most devs still haven't read it.Karpathy 的 CLAUDE.md 在 GitHub 上排名第一，获得了 82,000 个 star。但大多数开发者仍然没有读过它。.md]
source_url: https://x.com/0xDepressionn/status/2055999112470839383
confidence: high
rating: 6
---

# Karpathy 的 CLAUDE.md：21 条规则让编码准确率从 65% 到 94%

## 核心观点

Karpathy 识别了让 Claude Code 失败的 4 种行为模式，一个开发者将其扩展为 21 条规则写入 CLAUDE.md，在 GitHub 上获得 82,000 star。这份文件把 Claude Code 从一个"每次从零开始的健忘助手"变成了"记住决策、守住范围、确认后才破坏、从不建议破坏架构的框架"的可靠工具。**2 小时的一劳永逸设置，每个开发者每周节省 $975。**

## 关键要点

### Karpathy 的四条核心规则（65% → 94%）

```text
1. Ask, don't assume. 不确定就问，不要静默假设意图、架构或需求。
2. Simplest solution first. 总是实现最简单的可行方案。不添加未要求的抽象或灵活性。
3. Don't touch unrelated code. 如果文件或函数不直接属于当前任务，不要修改它——即使你觉得可以改进。
4. Flag uncertainty explicitly. 对方法或技术细节不够自信时，在做之前说出来。没有确定性的自信比承认缺口更有害。
```

### 三大板块 21 条规则

**板块一：Defaults（每次 30 分钟重复上下文的消除）**

| 规则 | 作用 |
|------|------|
| Kill the filler | 禁用 "Great question!"、"Of course!" 等填充词 |
| Match length to task | 简单问题直接答，复杂任务详细答，不填充不重复 |
| Show options before acting | 重大任务前给出 2-3 种方法，等选择 |
| Admit uncertainty | 不确定的事先说 "不确定"，不用似是而非的信息补缺口 |
| Who I am and what I know | 角色/擅长/短板 → Claude 调整回答深度 |
| Current project context | 项目/目标/受众/技术栈约束/避免事项 |
| Lock your voice | 写作风格、句式长度、常用/禁用词汇 |

**板块二：Behavior（防止未经授权的修改）**

| 规则 | 作用 |
|------|------|
| Stay in scope | 只改当前任务直接相关的文件/函数/行，不做额外重构/重命名/重格式化 |
| Ask before big changes | 重构段落、删内容、改语气 → 先描述变更等确认 |
| Confirm before destructive | 删文件、覆盖代码、删数据库记录 → 列出影响等确认 |
| Hard stops for production | 部署/迁移/schema 变更/不可逆命令 → 必须当前消息确认 |
| Always show what changed | 每个编码任务后列出：改了哪些文件、改了什么、有意不动的文件 |
| Never act without confirmation | 不得代你发送/发布/分享/排期任何东西 |
| Think before you write code | 架构决策/复杂调试/非平凡功能 → 先推理，标注不确定处，再实现 |

**板块三：Memory + Stack（健忘症的终结）**

| 规则 | 作用 |
|------|------|
| MEMORY.md decision log | 重大决策后记录：决定了什么、为什么、拒绝了什么 |
| Session end summary | "收尾"/"wrapping up" → 自动写 session summary 到 MEMORY.md |
| ERRORS.md failure log | 2 次以上尝试才成功的方案：什么不行、什么替代、注意事项 |
| Permanent facts list | 永远为真的项目约束，每次 session 自动应用 |
| Lock your tech stack | 技术栈锁定：语言/框架/包管理/数据库/测试/样式，不主动建议替代 |
| Extended Thinking | 架构/性能/数据库/长期决策 → 用扩展思考模式 |

### 成本计算（每个开发者每周）

| 浪费来源 | 时长 | $/周 |
|---------|------|------|
| 重复解释上下文 | 30 min/天 | $375 |
| 撤销未经授权的改动 | 1 hr/周 | $225 |
| 恢复遗忘的决策 | 2 hr/周 | $375 |
| **总计** | | **$975/周** |
| 团队 5 人 | | **$4,875/周** |
| **团队 5 人年化** | | **$253,500** |

### 设置步骤

1. 先在项目根目录创建 `CLAUDE.md`，从 Karpathy 的 4 条规则开始（2 分钟）
2. 用这段提示让 Claude 帮你写完整版：
   ```
   Based on what I've told you about myself, my project, and how I want to work:
   write me a complete CLAUDE.md file. Include: who I am, my tech context,
   my communication preferences, and default behaviors for every session.
   Be specific. Plain text. Under 500 words.
   ```
3. 每周发现缺失时追加一条，不一次性全加

## 与已有知识的关联

- [[20260518-claude-code-large-codebases-best-practices]] — Anthropic 的 "CLAUDE.md 必须精简层次化" 与本文的 21 条规则互为补充：Anthropic 说"不要太长"，本文说"至少要有这些"
- [[20260515-boris-cherny-opus-4-7-tips]] — Boris 的 Auto Mode + Focus Mode + 自验证循环 —— 本文的 CLAUDE.md 规则是 Boris 说 "Harness > Model" 的数据证明
- [[20260518-obsidian-ceo-stephango-note-system]] — Steph Ango 的 "一致性压倒决策" 与 MEMORY.md 决策日志 同构
- [[20260514-barrystop-agent-three-iron-rules]] — Barry 的 Agent 铁律与 Karpathy 的 4 条有大量重叠（"简洁优先" ≈ Simplest solution first）

## 行动建议

- 立即检查你的 `~/.claude/CLAUDE.md` 和项目 `CLAUDE.md`，与上文 21 条对照——缺了哪些？
- 从 Karpathy 的 4 条开始：如果只加 4 行，确保 "Ask don't assume" + "Simplest first" + "Don't touch unrelated" + "Flag uncertainty" 在文件里
- 你的 wiki 已有 MEMORY.md（`.agent-state/conversations/`）+ ERRORS.md（`mistakes.md`）+ Session end summary（dev-wrapup）——检查规则里有没有"每个 session 开始时自动读取它们"
- "Show options before acting" 这条是否适合你的工作流？你更偏向 Auto Mode 的自主执行，可能需要有选择地启用
