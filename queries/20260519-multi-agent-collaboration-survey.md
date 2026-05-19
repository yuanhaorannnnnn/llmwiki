---
title: "多智能体协作工程调查：触发拓扑、调用链与四大系统的设计取舍"
created: 2026-05-19
updated: 2026-05-19
type: query
tags: [clipping, agent, multi-agent, architecture, codex, claude-code, openclaw, hermes, topology]
sources: [Clippings/多智能体协作调查：Agent 到底该怎么分工.md]
source_url: https://x.com/Russell3402/article/2056331558223786416
confidence: high
rating: 7
---

# 多智能体协作工程调查：Agent 到底该怎么分工

## 核心观点

多智能体从来不是"多开几个模型实例"。工程上真正决定成败的是：**触发机制（谁有权开 worker）、拓扑结构（worker 怎么组织）、上下文隔离（worker 知道什么）、权限边界（worker 能做什么）、merge/reduce（谁对结果负责）**。四大系统（Codex、Claude Code、OpenClaw、Hermes）在这五个维度上做出了截然不同的取舍，没有任何一个是"万能正确答案"。

一句话口诀：**先设计边界，再增加 agent 数量。先决定谁 reduce，再决定开几个 worker。**

## 关键要点

### 1. 四类触发机制

| 触发方式 | 机制 | 代表系统 | 适用场景 |
|---------|------|---------|---------|
| **显式触发** | 用户说 "use parallel subagents" | Codex | 用户需要精确控制并行时机 |
| **语义触发** | 模型根据 subagent description 自动匹配 | Claude Code 普通 subagent | 专家自动出现、减少用户干预 |
| **路由触发** | 按 channel/account/thread 入口绑定 agent | OpenClaw | 多渠道、多身份系统 |
| **队列触发** | dispatcher 按 assignee 从 board/queue 拉起 worker | Hermes Kanban | 跨天、跨重启、需人类介入的长期任务 |

### 2. 七种拓扑结构

```
星型 fan-out/fan-in    链式 pipeline        树型 hierarchical
   主                       A                    main
  /|\                      ↓                 orchestrator
 w1 w2 w3                  B                  /    |    \
    ↓                      ↓                w1    w2    w3
   主                      C
                           ↓
                           主

网状 team mesh          Gateway routing      Durable board
   w1 ←→ w2            入口A→agent A          board: task, assignee
    ↕   ↕              入口B→agent B          state: blocked/retry/handoff
   w3 ←→ w4            入口C→agent C
```

| 拓扑 | 适用 | 不适用 |
|------|------|--------|
| 星型 | 独立并行任务（安全+测试+性能 review） | worker 之间需要互相纠错 |
| 链式 | 强顺序任务（定位→修复→测试→review） | 可以独立并行的工作 |
| 树型 | 大任务分层委派 | 深度和并发控制不足时指数膨胀 |
| 网状 | 多假设验证，需互相挑战 | 写文件冲突频繁时 |
| Gateway | 多渠道/多身份/多权限 | 单入口单用户 |
| Durable board | 跨天、重试、等人类 | 需要本轮立即返回的短任务 |

### 3. 调用链：多 agent 系统的七层拆解

```
input event
  → router/dispatcher   ← 是否拆？拆给谁？
  → context builder     ← worker 知道什么？（委派信息 = 需求文档）
  → worker profile      ← 什么角色？只读 explorer / 可写 worker / reviewer
  → execution sandbox   ← 能跑 shell？能写文件？能联网？能 spawn child？
  → state store         ← 状态放哪里？本轮 / session / 数据库
  → merge/reduce        ← 谁判断冲突？谁取舍？谁写最终 patch？
  → final output / next task
```

**关键 insight**：对 subagent 来说，委派信息就是需求文档。只写 "fix the error" 相当于把不完整需求丢给新同事。

### 4. 四大系统对比

| 维度 | Codex | Claude Code | OpenClaw | Hermes |
|------|-------|-------------|----------|--------|
| **核心场景** | 单次 coding session 的显式并行 | 专家注册表 + description 自动路由 | 多渠道 Gateway + 后台 agent | 短任务 RPC + 长任务 durable queue |
| **默认拓扑** | 星型（显式 fan-out） | 三层：普通 subagent / Agent Teams / worktrees | Routing → Agent isolation → Background subagent / ACP | delegate_task (RPC) + Kanban (持久队列) |
| **触发方式** | 显式授权为主 | description 语义匹配 | 入口绑定路由 | 自动 delegation + Kanban dispatcher |
| **并发控制** | max_threads + max_depth | Agent Teams 实验性 | maxSpawnDepth=1 | 默认 3 并发 child |
| **隔离粒度** | 上下文隔离 + 角色 profile | 普通 subagent 独立上下文；worktree 文件隔离 | 入口身份+workspace+session+工具四层隔离 | leaf worker 严格受限：不能再 delegate/不能问用户/不能写持久内存 |
| **优势** | 可预测、用户可控 | 专家自动匹配、三层覆盖广 | 多入口长期稳定运行 | 短/长任务分离清晰 |
| **弱点** | 不会自动判断"该并行" | description 太宽会乱触发；team 实验性 | 不擅长单次 coding 深度 | 短任务上 Kanban 笨重；长任务用 delegate_task 丢状态 |

**Codex 的关键取舍**：把复杂度当质量要求处理，而不是自动翻译成更多 worker。`深入分析一下` = 质量要求，不是并行授权。"显式授权少了一点自动，但把系统行为变得可预测。"

**Claude Code Agent Teams**：启用后不再是星型 fan-out，而是 team mesh——teammate 有独立上下文，可互相通信，共享任务列表。但成本更高：更多消息、更多中间判断、可能改同一文件、可能互相冲突。

**Hermes 的短/长分离**：`delegate_task` 处理几十秒到几分钟的并行（fork/join）；`Kanban` 处理跨天、重试、等人类输入。混淆两者是常见失败模式。

### 5. 七个反模式

| #   | 反模式                        | 正确做法                                                          |
| --- | -------------------------- | ------------------------------------------------------------- |
| 1   | **把复杂度当触发器**               | 任务复杂 ≠ 应该并行。强依赖任务走 pipeline 不是 fan-out                        |
| 2   | **不给 delegation contract** | worker 需要：路径、错误现场、验收标准、禁止事项、输出格式                              |
| 3   | **多 worker 写同一片代码**        | 先按目录/模块分 ownership；分不出来就不并行写                                  |
| 4   | **没有 reducer**             | 必须有人做取舍、合并、去重、排序、验收                                           |
| 5   | **短任务上队列，长任务用 RPC**        | 短→fork/join，长→durable queue。混用 = 又笨重又丢状态                      |
| 6   | **权限过宽**                   | review agent 不该写文件；leaf worker 不该 spawn child；家庭入口不该有公司 shell |
| 7   | **没有观测和审计**                | 需要知道谁触发谁、传了什么 context、用了什么工具、失败在哪里                            |

### 6. Delegation Contract 模板

```text
Role:       你是 read-only explorer / scoped worker / security reviewer
Goal:       要回答或完成什么，边界是什么
Context:    项目路径、相关文件、错误信息、用户目标、已有判断
Allowed:    能读什么、能不能跑命令、能不能写文件、能不能联网
Ownership:  如果能写，只能写哪些目录或文件
Forbidden:  不要改什么、不要问用户、不要 spawn child
Output:     findings / patch / test result / confidence / open questions
Stop:       什么算完成，什么算阻塞
```

### 7. 选择顺序（8 问）

1. **单 agent 能不能做？** → 能就别拆
2. **主上下文会不会被污染？** → 长日志/大搜索丢给 explorer
3. **子任务能不能独立？** → 独立→并行；依赖→pipeline
4. **结果必须本轮返回？** → 是→fork/join；否→background；跨天→durable board
5. **worker 需不需要互相挑战？** → 不需要→星型；需要→team mesh
6. **会不会并行写文件？** → 先写 ownership，再决定能否并行
7. **需不需要入口隔离？** → 多渠道→Gateway routing
8. **失败后如何恢复？** → retry？block？handoff？审计？

## 与已有知识的关联

- [[20260519-codex-goals-guide]] — Goal 的 Outcome/Verification/Constraints/Boundaries 与 Delegation Contract 模板同构
- [[20260518-claude-code-large-codebases-best-practices]] — Claude Code 三层（Subagents / Agent Teams / worktrees+batch）的完整对应
- [[20260514-barrystop-agent-three-iron-rules]] — Barry 的"预算敏感的 Agent"对应并发控制（max_depth/max_threads）
- [[20260511-how-we-built-our-multi-agent-research-system]] — Anthropic 多 Agent 研究系统的实际工程实现

## 行动建议

- 写 subagent description 时，把它当成**路由规则**而非愿望："Use after auth code changes" > "review code quality"
- 委派 worker 前，先用 Delegation Contract 模板填一遍——省的 token 远多于写的 token
- 任务不确定是否该并行时，先只用读 explorer 并行探索，确认边界后再决定是否让 worker 写代码
- 如果多个 worker 会写同一文件 → 停下来，先把文件 ownership 写清楚

## 来源

- [[Clippings/多智能体协作调查：Agent 到底该怎么分工.md]]
- https://x.com/Russell3402/article/2056331558223786416
