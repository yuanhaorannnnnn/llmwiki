---
title: "Codex Goals：用持久化目标合约替代反复提示的 Agent 工作模式"
created: 2026-05-19
updated: 2026-05-19
type: query
tags: [clipping, codex, agent, workflow, goals, evidence, architecture]
sources: [Clippings/Using Goals in Codex.md]
source_url: https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
confidence: high
rating: 6
---

# Codex Goals：用持久化目标合约替代反复提示

## 核心观点

Codex 的 Goals 不是在 prompt 里多写几句话——它是**线程级持久化状态**，把"做这个 → 等 → 再做下一个"的离散 prompt 模式改成了"一直工作到证据说完成"的持续循环。核心区别在于：一个 Goal 定义了**完成条件**——什么才算做完、怎么验证、什么不能动——而不只是定义下一步做什么。

这个设计解决了 Agent 使用中的一个根本摩擦：每次 Codex 停下来，你都得重新描述上下文和目标。Goal 让目标持久化在线程里，Codex 可以自己检查证据、决定下一步、继续工作——直到目标达成或诚实地被阻塞。

## 关键要点

### 1. Prompt vs Goal：根本差异

```
Prompt:   ask → work → result → wait（等用户说下一句）
Goal:     work → check → continue or complete（自行循环）
```

| 场景 | Prompt | Goal |
|------|--------|------|
| 单次编辑、解释、review | ✅ 正确工具 | ❌ 过度设计 |
| 性能调优（多轮试探） | ❌ 每轮都要重新描述 | ✅ 目标持久，自动循环 |
| 复现 flaky test | ❌ 路径不确定，多轮 | ✅ 调查+修复+验证循环 |
| 依赖迁移/重构 | ❌ 跨文件修改需要多轮 | ✅ 跨轮次追踪进度 |
| 论文复现 | ❌ 每步都要人工推进 | ✅ claim-by-claim 证据审计 |

### 2. Goal 生命周期管理

```bash
/goal          # 查看当前 Goal
/goal pause    # 暂停活跃 Goal（保留状态）
/goal resume   # 恢复暂停的 Goal
/goal clear    # 清除当前 Goal

# 设置 Goal
/goal Reduce p95 latency below 120 ms without regressing correctness tests
```

生命周期状态：`active → paused → resumed → completed | budget-limited | cleared`

### 3. 强 Goal 六要素

弱 Goal = `Improve performance`（没有完成标准）

强 Goal 定义六个东西：

| # | 要素 | 含义 | 例子 |
|---|------|------|------|
| 1 | **Outcome** | 做完时什么必须为真 | p95 latency < 120ms |
| 2 | **Verification surface** | 用什么证据证明 | checkout benchmark |
| 3 | **Constraints** | 什么不能退化 | correctness suite 保持绿色 |
| 4 | **Boundaries** | 可用哪些资源 | 仅 checkout service + benchmark fixtures |
| 5 | **Iteration policy** | 每轮后如何选下一步 | 记录变化、benchmark 结果、下一步最佳实验 |
| 6 | **Blocked stop** | 卡住时报告什么 | 尝试路径、收集的证据、阻塞点、需要什么 |

**模板：**
```
/goal <期望终态> verified by <具体证据> while preserving <约束>.
Use <允许的输入/工具/边界>.
Between iterations, <如何选择下一步>.
If blocked, <报告内容和解除阻塞需要什么>.
```

### 4. 架构设计要点

- **线程作用域**（非全局内存、非项目级指令）：Goal 属于当前 thread，随 thread 的上下文一起存在
- **事件驱动续接**（非简单循环）：只在 turn 完成 + 无待处理工作 + 无用户输入排队 + thread 空闲时检查续接条件
- **保守 dispatcher**：plan-only 工作不触发续接；中断会暂停 goal；无工具调用的续接轮次会抑制下一轮自动续接
- **预算明确**：达预算上限 → 停止实质性工作 → 总结进度和阻塞点 → 不等同于完成
- **证据审计强制**：Goal 不能因为模型"觉得可能完成了"就标记完成——必须对比 objective 与具体证据
- **权限边界**：模型可以启动 Goal、可以在证据支持时标记完成；暂停/恢复/清除/预算限制由用户或系统控制

### 5. 强 Goal 示例

**性能调优（弱→强）：**
```
弱：/goal Improve performance
强：/goal Reduce p95 checkout latency below 120 ms, verified by the checkout benchmark, while keeping the correctness suite green. Use only the checkout service, benchmark fixtures, and related tests. Between iterations, record what changed, what the benchmark showed, and the next best experiment to try. If the benchmark cannot run or no valid paths remain, stop with the attempted paths, the evidence gathered, the blocker, and the next input needed.
```

**论文复现（研究型 Goal）：**
```
/goal Produce the strongest evidence-backed reproduction of Buehler et al., "Deep Hedging," using the available paper materials and local resources. Attempt every headline result, verify the outputs, and end with a report that separates reproduced mechanics, approximate trained results, blocked exact replay, and remaining uncertainty.
```

**文档生成：**
```
弱：/goal Write docs for this feature
强：/goal Produce a docs page for Goals that explains the lifecycle, command surface, and two examples. Verify that the page builds locally and that all referenced commands match the current CLI behavior.
```

### 6. 不应使用 Goal 的场景

- 单行编辑、简单解释、简短 code review
- 完成标准模糊（"make this better"、"refactor this code"）
- 想隐藏不确定性（数据可能不可用、benchmark 可能 flaky——必须在 Goal 里声明）
- Goal 最强当任务满足三条件：**持久化目标 + 基于证据的完成线 + 需要多轮调查的路径**

### 7. 研究型 Goal 的 claim-by-claim 审计

用于论文复现的标准流程：
1. 将论文的 headline claims 和 supporting claims 分开
2. 将每个 claim 映射到可用证据
3. 重建可本地测试的部分
4. 对无法精确复现的 claims 标注 blocked
5. 生成审计报告，层级标记：已确认 → 近似重构 → 被阻塞 → 仍不确定

**关键：** Goal 不是让 Codex "做出漂亮的复现结果"，而是"最小化不确定性，同时不过度宣称证据支持了什么东西"。

## 与已有知识的关联

- [[20260518-claude-code-large-codebases-best-practices]] — Subagents 的"探索与编辑分离"模式与 Goal 的 continuation loop 互补
- [[20260514-barrystop-agent-three-iron-rules]] — Barry 的"预算敏感的 Agent"与 Goal 的 budget accounting 同构
- [[20260512-perplexity-agent-skills-design]] — Skills 的渐进式披露 vs Goal 的持久化目标，两者解决不同层次的问题
- [[20260515-boris-cherny-opus-4-7-tips]] — "给 Claude 一个验证自己输出的方式" ≈ Goal 的 verification surface

## 行动建议

- 如果你用 Codex：对于跨多轮的调优/调查/迁移任务，用 `/goal` 替代反复 "keep going" 提示
- 写 Goal 时先问：什么证据能证明完成？什么不能变？卡住了怎么办？三个问题回答完再写 `/goal`
- 不确定怎么写 Goal 时，先让 Codex 帮你拟草案：`Help me turn this into a strong /goal: I want Codex to...`
- Claude Code 没有同等的 Goal 机制——但可以通过在 CLAUDE.md 或 session 开始时明确声明 Objective + Verification + Constraints 来模拟

## 来源

- [[Clippings/Using Goals in Codex.md]]
- https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
