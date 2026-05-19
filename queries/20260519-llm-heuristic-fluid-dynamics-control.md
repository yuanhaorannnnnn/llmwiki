---
title: "LLM 替代深度强化学习做流体力学控制：Codex 发现可解释启发式策略"
created: 2026-05-19
updated: 2026-05-19
type: query
tags: [clipping, llm, agent, scientific-computing, fluid-dynamics, reinforcement-learning, codex, heuristic]
sources: [Clippings/DonsetPG's blog.md]
source_url: https://donsetpg.github.io/#/blog/heuristic-learning-for-fluid-dynamics-a-case-study
confidence: high
rating: 7
---

# LLM 替代 DRL 做流体力学控制

## 核心观点

用 Codex（LLM agent）替代深度强化学习（PPO/SAC）来做流体力学控制优化，结果是**反直觉的**：Codex 在 Rayleigh-Bénard 对流和湍流通道等难题上**显著优于**最好的 DRL agent；在所有 Beacon 基准上至少打平，~50-60% 的情况下超越。更重要的是，Codex 产出的策略是**纯 Python 函数**——不是黑箱神经网络权重，而是带物理含义的可读代码。花费仅 $6-14 一次。

**这不是"LLM 替代数值模拟"——这是"LLM 替代控制策略搜索"。**

## 关键要点

### 1. 方法：LLM 作为启发式搜索器

传统路径：DRL agent (PPO/SAC) 与环境交互成千上万轮 → 产出一个神经网络策略（不可解释的黑箱）

LLM 路径：Codex 观察环境（public observation） → 写出控制策略（Python 函数） → 仿真器评估 → Codex 根据结果迭代改进策略

**关键区别**：
- DRL 产出一个神经网络的权重
- Codex 产出一个带注释的 Python 函数，其中包含明确的物理特征工程

### 2. 实验结果对比

| 环境 | Codex vs DRL |
|------|-------------|
| Cylinder (基础) | 胜 PPO，略逊 SAC |
| Rayleigh-Bénard 对流 | **显著优于**所有 DRL agent |
| 湍流通道 (Turbulent Channel) | **显著优于**所有 DRL agent |
| Beacon 基准套件 | ≥ 最好 DRL agent，50-60% 超越 |

**迁移学习**：Codex 从 5-jet 策略迁移到 10-jet，几乎立即适应——DRL agent 做同样的迁移需要多得多的样本且效果更差。

**长时域稳定性**：Codex 的策略在训练时域外（400 步 vs 100 步训练）保持稳定——PPO 策略在同样条件下崩溃。

### 3. 两个具体策略分析

**Shkadov 落膜问题（延迟形状反馈）**
```python
feature = (
    q.mean()                          # 均值
    - 0.585 * (q[-1] - q[0])          # 斜率
    + 0.922 * (q[mid] - 0.5*(q[0]+q[-1]))  # 曲率 ← 主要贡献
    - 0.228 * q[-1]                   # 末端偏差
)
delayed = signal_history[j][t - 11]   # 11 步延迟 = 平流时钟
```
曲率项做了大部分工作——"增长的薄膜波是形状问题，曲率是最便宜的可用形状信号"。延迟 11 步是一个粗糙的平流时钟：控制器等待上游变形到达喷射器可以起作用的点。

**TCFSmall3D 湍流通道（空间局部反馈）**
```python
signal = -0.264 * v + 0.211 * u     # u, v 为两通道壁场
action = smooth(action)             # 壁面网格平滑
action[wall] -= action[wall].mean() # 移除每壁均值
```
关键发现：如果不保留空间信息（如果把 2048×2 壁场压缩成一个标量），策略崩溃。物理通过代码渗透——控制器之所以工作，是因为它保持了几何结构。

### 4. 成本

| 阶段 | 输入 tokens | 缓存命中 | 输出 | 费用 |
|------|-----------|---------|------|------|
| 10-actuator 适应 | 8.3M | 8.0M | 20.8k | $6.05 |
| 完整实验 + 图表 | 9.8M | 9.4M | 28.2k | $7.42 |
| 5-actuator 启发式搜索 | 21.3M | 21.0M | 74.2k | $13.95 |

> 96%+ 的输入 token 来自缓存命中——长线程累积的上下文几乎全部被缓存。

### 5. 方法论意义

这个工作指向一个更一般的模式：**LLM 作为科学计算中的启发式搜索器**。任何需要"在仿真环境中迭代试错、且成功的标准是可量化的"的优化问题，都可以用这套框架：
1. 暴露 public observation（仿真器的观测接口）
2. 定义 reward（目标函数）
3. 让 LLM 写控制策略（Python 函数）
4. 仿真器评估 → LLM 根据结果改进
5. 产出可解释的策略代码 + 物理解释

对比传统 DRL：不需要设计 reward shaping、不需要调 PPO/SAC 超参、不需要担心训练不稳定、产物是人可读的代码而非权重矩阵。

## 与已有知识的关联

- [[20260519-codex-goals-guide]] — Goal 的 "verification surface" 在这里是仿真器评估结果
- [[20260519-codex-maxxing-jason-liu]] — Jason 的 "ambition without verification is just a wish"——仿真器就是那个 verification oracle
- [[neural-radiance-field]] — 同为 AI + 传统物理仿真的交叉应用

## 来源

- [[Clippings/DonsetPG's blog.md]]
- https://donsetpg.github.io/#/blog/heuristic-learning-for-fluid-dynamics-a-case-study
