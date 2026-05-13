---
title: Sim-ready Asset Generation
created: 2026-04-30
updated: 2026-04-30
type: concept
tags: [model, embodied-intelligence, simulation, 3d-generation, robotics]
sources:
  - raw/papers/paper/E-物理仿真/2025-PhysX-Anything-Generative-Sim-Ready-3D-Assets-with-Physical-Properties-from-a-Single-Image.pdf
confidence: high
---

# Sim-ready Asset Generation

> 传统 3D 生成模型解决"像不像"的问题。Sim-ready asset generation 解决"能不能用"的问题——从单张图片/视频自动生成可直接导入物理引擎的 3D 资产，包含完整几何、材质、关节约束和物理属性，无需任何手工修改。

## 定义

**Sim-ready（模拟就绪）** 指生成的 3D 资产满足以下条件：
- 几何完整 —— mesh 或体素表示，无破面、无空洞
- 物理属性自洽 —— 密度、摩擦系数、弹性模量等参数合理
- 关节约束正确 —— 铰链、滑轨、齿轮等运动副的类型、位置和范围准确
- 标准格式输出 —— URDF、XML、MuJoCo MJCF 等模拟器原生格式

简言之：**拖进 MuJoCo/PhysX，重力开始作用，铰链开始转动**。

**为什么不是传统 3D 生成？**
- 传统 3D 生成（如 DreamFusion、Point-E）只优化视觉保真度——渲染图跟原图像不像
- Sim-ready 生成额外优化**物理一致性**——模拟器里的行为跟真实物体一不一致
- 这是 sim-to-real gap 的最前端：如果模拟器里的资产本身就是错的，后面策略学习再强也白搭

## 技术脉络

```
3D 生成（视觉导向）
    ├── mesh / point cloud / NeRF / 3DGS —— "长得像"
    └── PhysX-Anything —— "长得像 + 物理对 + 能直接用"

Sim-ready 生成（物理导向）
    ├── 前期：手工建模 + 物理标注（CAD → URDF，半天一个物体）
    └── PhysX-Anything：VLM 多轮对话 + 体素压缩 + Flow Transformer → 全自动
```

## 核心方法：PhysX-Anything

### 1. Global → Local 多轮生成 Pipeline

**第一轮（Global）**：VLM 看完整图，输出结构化物理描述
- 物体名称、类别、长宽高
- 材料类型、密度
- 部件列表（每个部件的名称、连接关系、关节类型）

**第 N 轮（Local）**：逐部件生成几何
- 对第 i 个部件："l_i 号部件长什么样？"
- VLM 输出 `32×32×32` 体素网格中被占据的坐标

关键设计：生成部件时，VLM 上下文**只保留 Global 信息**，不保留之前部件的几何细节。避免上下文遗忘——先输出的简单部件不会被后面复杂部件挤掉。

### 2. 193x 体素压缩

原始 mesh 描述一个部件需要~17 万 token（顶点+面索引）。VLM 上下文窗口撑不住。

PhysX-Anything 的做法：
1. `32×32×32 = 32768` 个体素格子，只列出被占据的格子编号
2. 连续编号用区间压缩：`199-216` 表示 199 到 216 全被占
3. 结果：平均 919 token/部件，**193 倍压缩**

**关键洞察**：不需要改 VLM 的 tokenizer、不需要训练特殊的 3D tokenizer。把 3D 问题变成字符串压缩问题，利用 VLM 本来就擅长的"理解数字序列"能力。

### 3. Coarse-to-fine 细化

- VLM 输出：粗体素 `32³`（低分辨率，但结构正确）
- Flow Transformer：将粗体素细化为高分辨率几何
- 格式解码器：同时输出 mesh + URDF + XML + 3D Gaussian + 部件级 mesh

### 4. 效果

| 指标 | 之前最佳 (PhysXGen) | PhysX-Anything | 提升 |
|------|---------------------|----------------|------|
| 绝对尺寸误差 | 43.44 | **0.30** | 99% ↓ |
| 物理属性评分 | baseline | **显著领先** | — |
| 用户研究 (14人×1568分) | baseline | **几何+物理双维度领先** | — |

MuJoCo 实测：拧水龙头、开关门、折叠眼镜腿、按打火机——铰链转到位就停，抽屉拉到头有硬限位，打火机按下去有回弹。

## 关键概念详解

### Sim-ready vs. Visual-realistic

| 维度 | Visual-realistic | Sim-ready |
|------|-----------------|-----------|
| 评估标准 | PSNR, FID, CLIP score | 模拟器行为一致性 |
| 错误类型 | 纹理模糊、几何简化 | 关节类型错、密度离谱、重心偏 |
| 修复难度 | 局部微调可解 | 需全局物理自洽，局部优化基本无解 |
| 下游任务 | 渲染、展示 | 机器人策略学习、sim-to-real |

**核心洞见**：物理正确性是比视觉正确性更硬的生成质量标准。视觉好可以微调出来；物理好——密度、尺寸、关节约束全部自洽——基本上没法局部优化。能做到 sim-ready，意味着模型内部一定有一个**隐式的物理世界模型**，而不只是一台高级渲染器。

### 从"生成质量"到"可验证质量"

PhysX-Anything 提醒我们一件事：**评估生成模型不应该跟参考答案比像不像，而应该扔进真实物理过程里看对不对**。

这意味着：
- 评估 3D 生成 → 看模拟器里的行为一致性
- 评估视频生成 → 看物理参数（摩擦、碰撞响应、流体黏度）是否合理
- 评估任何生成 → 找一个"不允许作弊的物理引擎"来检验输出

## 可迁移洞见

### "先整体结构、再局部细节"的多轮生成策略

这个 pipeline 设计可以平移到其他生成任务：
- **视频生成**：先场景布局（哪些物体、在哪、怎么动），再逐物体轨迹
- **代码生成**：先架构设计（模块划分、接口定义），再逐模块实现
- **文档生成**：先大纲结构，再逐节展开

核心原则：把"全局约束"和"局部生成"解耦，避免上下文竞争。

### "把 X 问题变成字符串压缩问题"

193x 压缩的启示：当领域特定表示（mesh 顶点）遇到通用模型（VLM）的输入限制时，不要硬改模型，而是找一个**模型已擅长处理的中间表示**（数字序列 + 区间压缩）。

类似思路：
- 时间序列 → 用数字序列 + 趋势分段描述
- 图结构 → 用邻接表 + 节点属性文本描述
- 音频 → 用频谱包络 + 关键帧参数描述

## 来源

| 论文 | PDF 路径 | Denote 笔记 |
|------|----------|-------------|
| PhysX-Anything | `raw/papers/paper/E-物理仿真/2025-PhysX-Anything-Generative-Sim-Ready-3D-Assets-with-Physical-Properties-from-a-Single-Image.pdf` | `~/Documents/notes/20260428T155315--paper-physx-anything__paper.md` |
