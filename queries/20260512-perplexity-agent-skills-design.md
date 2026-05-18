---
title: "Perplexity Agent Skills 设计与维护方法论"
created: 2026-05-12
updated: 2026-05-12
type: query
tags: [article, agent-skills, skill-design, perplexity, methodology]
sources: ["Clippings/Designing, Refining, and Maintaining Agent Skills at Perplexity.md"]
source_url: https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
confidence: medium
---

# Perplexity Agent Skills 设计与维护方法论

## 核心观点

Skill 不是普通软件——它是"给模型和其环境构建的上下文"。用写代码的思维写 Skill 会失败。PEP20 的 20 条 Zen of Python 里至少有一半在 Skill 世界里是错的。核心差异：代码的优化目标是正确性和可维护性，Skill 的优化目标是**在最小的 token 成本下让模型做对的事**。Perplexity 公开的这份内部指南是当前 agent skills 工程领域最系统的实践总结，覆盖 Skill 本质定义、何时需要/不需要 Skill、5 步构建流程和维护飞轮。

## 关键要点

1. **一个 Skill 是四件事：Directory + Format + Invocable + Progressive**
   - **Directory**：不只是 SKILL.md，用 hub-and-spoke 模式（scripts/、references/、assets/、config.json），把条件性内容从主干拆到分支
   - **Format**：`name: lower-kebab-case`，`description` 是路由触发器（"Load when..."而非"This Skill does..."），取决于 `depends:` 实现层级依赖
   - **Invocable**：Skill 不是总在 context 里——按需加载，Computer 的隔离沙箱+递归加载依赖+剥离 frontmatter 再注入
   - **Progressive**：三级 token 成本结构，每一级成本数量级不同

2. **三级渐进式加载 = 三级成本边界**
   ```
   L1: Skill index（name + description，~100 token/skill）
       → 每个 session、每个用户都付费，进入门槛极高
   L2: SKILL.md body（≤ 5000 token）
       → 加载后整个对话都付费直到 compaction 边界
       → 多 Skill 叠加（3-5 个）会放大成本，冗余内容连带降低其他 Skill
   L3: scripts / subskills / formatting
       → 条件性加载，agent 需要时才用，可容 20000+ token
   ```
   判断标准：L1 每个 token 都重要，L2 相对宽松，L3 最宽松。

3. **Skill description 是整个 Skill 最难写的一句话**
   - 它不是文档，是路由触发器。写"用户什么时候需要加载这个 Skill"，不写"这个 Skill 做什么"
   - 反例：`"This Skill monitors pull requests and checks CI status"`
   - 正例：`"Load when the user says 'babysit this PR', 'watch CI', or asks you to make sure their PR lands"`
   - 50 词以内，用真实用户查询的语言
   - 每加一个新 Skill 都可能让其他所有 Skill 变差（action at a distance）

4. **什么时候不需要 Skill**
   - 模型训练数据已有覆盖的通用知识（git 命令、常见工具用法）——写成文档好但写成 Skill 差
   - 和 system prompt 重复的内容——应该放全局 context 而非条件加载的 Skill
   - 变化快于你能维护的内容（如频繁变更的 MCP 端点工具列表）——注入后会产生漂移

5. **构建 Skill 的 5 步流程**
   - **Step 0: 先写 evals**——采样来源：真实用户查询、已知失败案例、邻域越界（相邻 Skill 被误路由）。负面样例的效力大于正面样例
   - **Step 1: 写 description**——只关心路由精度和召回率，不关心 Skill 内容
   - **Step 2: 写 body**——跳过模型已知的（别列 git 命令清单），写"Cherry-pick onto clean branch, resolve conflicts preserving intent"而非一步步命令。**Gotchas/负面样例是最高信号内容**，每次 agent 出错就加一条
   - **Step 3: 用 hierarchy**——条件性、分支性内容从 SKILL.md 拆到子文件夹
   - **Step 4: 迭代**——在一个分支上做多次迭代，提交单个 changeset + eval 结果，方便 reviewer
   - **Step 5: Ship**

6. **维护飞轮：Gotchas append-mostly**
   ```
   agent 在某个任务失败     → 加一条 gotcha
   agent 非目标场景加载 Skill → 收紧 description + 加负面 eval
   agent 应加载但没加载       → 加关键词 + 正面 eval
   system prompt 变更        → 检查重复/冲突
   ```
   从 80/20 做到 99.9% 的过程就是 gotcha 列表增长的过程。**不要加更长的指令**，加负面样例就够了。合并后改 description 必须有 eval 支撑。

## 行动建议

- **把所有 Skill 的 description 改成 "Load when..." 格式**——检查现有的 content-ingest、paper-to-concept 等是否写了路由触发条件而非功能描述
- **给每个 Skill 建 eval 集**——至少包含：正确加载场景、不应该加载的场景（邻域越界）、加载后是否正确读取了 accessory 文件
- **从 SKILL.md body 中删除模型已知的常识**——"用 yt-dlp 下载视频"这种 LLM 本来就会的内容不应占用 token 预算
- **建立 gotcha 段**——在 Skill 末尾加 `## Gotchas` 或 `## 常见错误`，每次 agent 在这个 Skill 上出错就追加一条
- **检查 action at a distance**——新增 content-ingest 后，要不要检查它是否影响了 paper-to-concept 的路由？两个 Skill 的 description 边界是否清晰？

## 相关笔记
- [[20260513-complete-guide-building-claude-skills]] — Anthropic 官方 Claude Skills 构建完整指南：从设计到分发
- [[20260518-claude-code-large-codebases-best-practices]] — Claude Code 在大代码库中的工作方式：企业级部署最佳实践
- [[20260514-barrystop-agent-three-iron-rules]] — Barry Zhang (Anthropic) AI Engineer Summit：如何构建高效 Agent 的三条铁律
- [[20260512-tdd-not-ai-native]] — TDD 反而不是 AI 时代的答案：从过程确定性到结果确定性
- [[20260518-obsidian-ceo-stephango-note-system]] — Obsidian CEO Steph Ango 的笔记系统：File over App 哲学与极简主义实践

## 来源

- 原文：https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
- 原始文本：[[Clippings/Designing, Refining, and Maintaining Agent Skills at Perplexity.md]]
