---
title: "Anthropic 官方 Claude Skills 构建完整指南：从设计到分发"
created: 2026-05-13
updated: 2026-05-13
type: query
tags: [article, claude, skill-design, agent-skills, methodology, guide]
sources: [raw/articles/20260513-complete-guide-building-claude-skills.md]
confidence: high
---

# Anthropic 官方 Claude Skills 构建完整指南：从设计到分发

## 核心观点

这份 33 页的 Anthropic 官方指南系统性地定义了 Skill 是什么（"教 Claude 一次，每次都受益的可复用指令集"）、如何设计（从识别可重复工作流开始）、如何测试迭代（eval-first 范式）、以及如何分发。和 Perplexity 的 Skills 方法论形成互补——Perplexity 偏"组织结构和维护飞轮"，这份指南偏"个人/小团队从零构建 Skill 的实操流程"。

## 关键要点

### 1. Skill 的本质定义

Skill 是一个**包含指令的文件夹**，教 Claude 处理特定任务或工作流。核心理念："不是每次都要重新解释你的偏好、流程和领域知识——教一次，每次都受益。"

适用场景：可重复的工作流——从前端设计 spec、研究方法论、团队风格文档生成、到复杂多步骤流程编排。

### 2. 构建 Skill 的四阶段流程

```
规划设计 → 测试迭代 → 分发共享 → 持续维护
```

#### Phase 1: 规划设计

- **从识别可重复工作流开始**——不是"我想写一个 Skill"，而是"我第三次让我做同一件事了，这该是个 Skill"
- **写 description 是最高杠杆的决策**——5 个关键原则：
  - 写用户会说的自然语言，不要写技术描述
  - 包含正例和反例："Load when..." + "Do NOT load when..."
  - 描述意图和场景，不要总结工作流
  - 保持简洁（50 词内）
  - 避免与其他 Skill 的 description 重叠
- **依赖声明**：用 `depends:` 字段定义 Skill 间的层级关系，避免重复内容

#### Phase 2: 测试迭代（eval-first）

- **在任何 Skill 内容写之前，先设计 eval 用例**——和 Perplexity 的"Step 0: Write the Evals"完全一致
- eval 类型：路由精度（是否在正确场景加载）、输出质量（加载后的行为正确性）、副作用检测（是否误触发其他 Skill）
- 用真实查询做 eval，不要只用人造测试——采样生产日志或历史会话
- 迭代循环：改 description → 跑路由 eval → 改 body → 跑质量 eval → 重复

#### Phase 3: 分发共享

- 打包为独立文件夹：`skill-name/SKILL.md` + scripts/ + references/ + assets/
- 版本管理：在 frontmatter 中声明 `version`
- 安装方式：放到 `~/.claude/skills/` 目录或 team-shared 位置
- 共享时的注意事项：脚本中的硬编码路径、外部依赖声明、隐私信息（API key）不要打包

#### Phase 4: 持续维护

- Skill 是 append-mostly 的——新增 gotchas 远比修改核心指令频繁
- 环境变化检查清单：新模型版本、系统 prompt 更新、新 Skill 引入是否冲突
- 定期审计冗余：Skill 中是否有内容可以被 prompt 或者系统能力自然覆盖

### 3. 常见模式和反模式

| 类型 | 说明 |
|------|------|
| ✅ Hub-and-spoke | SKILL.md 做路由+核心指令，重内容放 references/ 渐进加载 |
| ✅ Progressive disclosure | 三级 token 成本：index → body → scripts |
| ✅ Gotchas section | 积累"不要这样做"的经验——每次出错追加一条 |
| ❌ Write-only documentation | 把 Skill 当人类文档写——列 git 命令清单、重复系统已知知识 |
| ❌ One-shot generation | 用 LLM 生成 Skill 后不测试就发布——LLM 生成的 Skill 对 LLM 自己没帮助 |
| ❌ Drifting description | 合并后改 description 不加 eval → 路由漂移 + 误伤周围 Skill |

### 4. 故障排查

- **Skill 没被加载**：检查 description 是否匹配用户的自然表达方式；是否和其他 Skill 的触发词冲突
- **Skill 加载了但不按预期工作**：检查 body 是否被正确地剥离了 frontmatter；references/ 文件是否被正确引用
- **Skill 加载了但行为变差**：可能是 body 太长超出有效 context；缩减到 5000 token 内，拆分条件内容到 references/
- **新 Skill 导致其他 Skill 路由出问题**：action at a distance——description 的关键词和周围 Skill 重叠了

## 与已有知识的对照

| 来源 | 核心贡献 |
|------|---------|
| Perplexity Skills 方法论 | "Load when..."、三级渐进加载、gotchas 维护飞轮、org 级 Skill 治理 |
| **Anthropic 官方指南（本文）** | 四阶段流程、eval-first 范式、分发机制、故障排查清单 |
| discussion-digest skill | Anthropic 的 HTML 可视化实际上是 Hub-and-spoke 模式的实例 |
| content-ingest 路由 | description 路由触发器的实际工程验证 |

两个来源互相印证的关键共识：
- **description 是最难写的一行**——Perplexity 和 Anthropic 独立得出相同结论
- **eval 必须在 Skill 内容之前写**
- **LLM 生成的 Skill 对 LLM 自己无益**——Perplexity 的结论在 Anthropic 指南中被确认
- **action at a distance 是 Skill 系统的固有风险**

## 行动建议

- 给现有的 3 个 self skill（content-ingest、paper-to-concept、discussion-digest）补充 eval 用例——至少路由精度 eval
- 检查 discussion-digest 的 description 是否和 content-ingest 有触发词重叠
- 在 skill 维护流程中加入"每次出错→追加 gotcha"的 append-mostly 习惯

## 来源

- 原文：[[raw/articles/20260513-complete-guide-building-claude-skills.md]]
- PDF：[[raw/notes/待阅读/The-Complete-Guide-to-Building-Skill-for-Claude.pdf]]
