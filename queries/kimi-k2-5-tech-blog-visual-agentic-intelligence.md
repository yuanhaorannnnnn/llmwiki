---
title: "Kimi K2.5 的 Agent Swarm：用 PARL 训练并行编排器的工程细节"
created: 2026-05-11
updated: 2026-05-11
type: query
tags: [article, agent-swarm, multi-agent, rl, kimi]
sources: [Clippings/Kimi K2.5 Tech Blog Visual Agentic Intelligence.md]
source_url: https://www.kimi.com/blog/kimi-k2-5
confidence: medium
---

# Kimi K2.5 的 Agent Swarm：用 PARL 训练并行编排器的工程细节

## 核心观点

Kimi K2.5 的 Agent Swarm 不是手动编排的多 Agent 系统，而是一个**用强化学习训练的并行编排器**——模型自己学会什么时候 spawn subagent、怎么分配任务、什么时候合并结果。训练方法叫 PARL（Parallel-Agent Reinforcement Learning），核心挑战是防止模型退化成串行执行（serial collapse），解决手段是分阶段 reward shaping + 用 Critical Steps 做 latency 约束。工程上最值得借鉴的是它把"并行性"当成一个需要刻意训练的 RL 目标，而不是靠 prompt engineering 硬推。

## 关键要点

1. **PARL 架构：可训练的 orchestrator + 冻结的 subagents**
   orchestrator agent 负责拆任务（"找 100 个细分领域的 top YouTuber" → 拆成 100 个子任务），动态 spawn 子 agent 去并行执行。subagents 是冻结的（不参与训练），只做具体搜索/推理工作。orchestrator 通过 RL 学习什么时候拆、拆多少、怎么合。
   
   为什么冻结 subagents：如果 subagents 也训练，训练过程中每个 subagent 的行为在变，orchestrator 收到的反馈就变成 non-stationary——RL 学习的基础不稳。

2. **防止 serial collapse 的 reward 设计：三部分，λ 逐步退火到零**
   ```
   r_PARL = λ₁ · r_parallel + λ₂ · r_finish + r_perf
   ```
   - `r_parallel`：激励 spawn subagent——但会导致 spurious parallelism（为得分猛 spawn 但不干活的 subagent）
   - `r_finish`：激励 subagent 真正完成任务——防止假并行
   - `r_perf`：最终任务质量
   - λ₁ 和 λ₂ **在训练过程中逐步退火到零**——前期鼓励探索并行策略，后期让任务质量主导优化

   这个 staged reward 设计是防止早期 RL 掉进 serial collapse 局部最优的关键。

3. **Critical Steps 指标：用关键路径思维评估并行效率**
   ```
   CriticalSteps = Σ (S_main(t) + max_i S_sub,i(t))
   ```
   不是计总步数（那会奖励串行），而是计每一时间步的"最长腿"——main agent 的编排开销 + 最慢的那个 subagent 的步数。spawn 更多 subagent 只在缩短关键路径时得分。这个指标直接对应 wall-clock latency。

4. **制造计算瓶颈来强迫并行**
   直接在环境中加约束：不是"建议你并行"而是"不并行就跑不完"。具体做法：不按总步数评估，只按 Critical Steps 评估。串行执行意味着 Critical Steps = 所有步数之和，必输。

5. **Agent Swarm 的实际性能：4.5× wall-clock 加速**
   在 wide search 场景中，同样准确率目标下，Agent Swarm 把 Critical Steps 压到单 Agent 的 1/3 到 1/4.5，wall-clock 时间对应缩短。100 个 subagent 并行搜索 100 个细分领域 YouTube 创作者，结果汇入一个 spreadsheet。

6. **K2.5 其他可迁移经验**
   - **视觉编码**：vision-text 联合预训练到足够大后，视觉能力和文本能力不再是 trade-off，而是一起涨——不用再纠结"加视觉能力会不会吃掉文本能力"
   - **编码评测配置**：SWE-Bench 系列用 minimal tool set（bash, createfile, insert, view, strreplace, submit）加 tailored system prompts，非 thinking 模式下得分最高

## 行动建议

1. 设计 multi-agent RL 训练时，在 reward 里显式加入并行性激励 + 完成率激励，但用退火策略让任务质量最终接管
2. 评估并行 agent 系统不要用总步数——用 Critical Steps（最长腿求和），这会直接对应 wall-clock
3. 如果模型拒绝并行，在环境里加计算瓶颈强制它——不要靠 prompt 求它并行
4. 构建 agentic coding benchmark 时，用 minimal tool set（6 个工具以内）而非全量工具集——非思考模式下 minimal tools 得分反而更高

## 来源

- 原文：https://www.kimi.com/blog/kimi-k2-5
- 剪藏：[[Clippings/Kimi K2.5 Tech Blog Visual Agentic Intelligence.md]]
