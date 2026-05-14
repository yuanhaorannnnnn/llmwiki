---
title: 3D Gaussian Splatting 技术栈
created: 2026-04-30
updated: 2026-05-13
type: concept
tags: [model, architecture, rendering, multi-modal, video, mesh-extraction]
sources:
  - raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2023-SuGaR Surface-Aligned Gaussian Splatting.pdf
  - raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2024-2D Gaussian Splatting for Geometrically Accurate Radiance Fields.pdf
  - raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2024-Gaussian Opacity Fields Efficient and Compact Surface Reconstruction in Unbounded Scenes.pdf
  - raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2025-3DGS-TO-PC.pdf
#   - raw/papers/paper/E-神经渲染/2025-3DGUT Enabling Distorted Cameras and Secondary Rays in Gaussian Splatting.pdf
#   - raw/papers/paper/E-神经渲染/2025-OMNIRE OMNI URBAN SCENE RECONSTRUCTION.pdf
#   - raw/papers/paper/E-神经渲染/REAL-TIME PHOTOREALISTIC DYNAMIC SCENE REPRESENTATION AND RENDERING WITH 4D GAUSSIAN.pdf
#   - raw/papers/paper/E-神经渲染/TargetWorks/3DGS路线/2025-FreeTimeGS Free Gaussian Primitives at Anytime and Anywhere.pdf
confidence: high
---

# 3D Gaussian Splatting 技术栈

> 3D Gaussian Splatting（3DGS）是 2023 年提出的神经渲染方法，用数百万个 3D 高斯粒子（位置、协方差、颜色、不透明度）表示场景，通过光栅化 tile-based rasterizer 实时渲染。截至 2024-2025 年，3DGS 已发展出一个完整的技术栈，覆盖渲染后端、相机模型、场景规模、动态场景、深度先验和网格提取六个维度。

## 定义

3DGS 用**显式基元**（3D 高斯椭球）替代了 NeRF 的隐式 MLP 或网格表示。每个粒子有：
- 均值 µ = (x, y, z) — 空间位置
- 协方差 Σ（3×3）— 描述椭球的形状和方向
- 颜色 — 球谐系数（SH）编码，支持视角相关颜色
- 不透明度 σ — 控制粒子透明度

渲染时，粒子按深度排序后投影到 2D，用 alpha blending 合成像素颜色。这是**光栅化**路径，不是光线追踪。

**为什么快？**
- 显式表示 → 不需要 MLP 前向传播
- 光栅化 → GPU 硬件加速，tile-based 并行
- 可微渲染 → 可以直接从照片优化粒子参数

## 技术脉络

```
基础 3DGS (2023)
    ├── 渲染后端升级
    │     ├── 3D Gaussian Ray Tracing — 光线追踪替代光栅化，解决反射/鱼眼/随机采样
    │     └── 3DGUT — 不换渲染器，改用无迹变换支持畸变相机
    ├── 场景规模扩展
    │     └── OmniRe — 场景图 + 多表示类型（静态/刚体/SMPL/可变形）
    ├── 动态场景
    │     ├── 4D Gaussian Splatting — 4D 高斯时空统一，运动自然涌现
    │     ├── FreeTimeGS — 短寿命高斯接力，线性运动逼近复杂轨迹
    │     └── Split4D — 4D 分割，粒子流动自追踪 → 见 [[4d-scene-decomposition]]
```

## 核心论文对比

| 维度 | 论文 | 核心问题 | 方法 | 速度 | 关键权衡 |
|---|---|---|---|---|---|
| 渲染后端 | 3DGRT (NVIDIA, 2024) | 光栅化不支持反射、鱼眼、随机采样 | 光线追踪 + 拉伸二十面体包围代理 + k-buffer 步进 | 前向 78-190 FPS（慢 2 倍） | 全能力但速度损失 |
| 相机模型 | 3DGUT (NVIDIA, 2025) | 鱼眼/卷帘快门相机畸变 | 无迹变换(UT)替换 EWA 投影公式 | 光栅化速度（347 FPS） | 保留速度，获得部分能力 |
| 场景规模 | OmniRe (NVIDIA, 2025) | 城市场景多物体单独操控 | 场景图：静态高斯 + 刚体 SE(3) + SMPL + 共享变形网络 | 实时 | 表示复杂度 vs 操控粒度 |
| 动态场景 | 4DGS (ICLR 2024) | 时空耦合，运动显式建模困难 | 4D 高斯 (x,y,z,t) + 4D 旋转 + 条件分布渲染 | 实时 | 统一表示 vs 突变事件 |
| 动态场景 | FreeTimeGS (ZJU, 2025) | 大运动/非刚性/出现消失 | 短寿命高斯（出生时间 µt + 寿命 s + 速度 v） | 实时 | 分段线性 vs 全局一致性 |

## 关键概念详解

### 1. 渲染后端：光栅化 vs 光线追踪

**3DGS 原生光栅化**：从相机发射像素射线，找到覆盖该像素的所有 2D 高斯椭圆，按深度排序后 alpha blend。快，但**单射线路径**——无法处理反射、折射、景深。

**3DGRT 光线追踪**：
- **包围体代理**：给每个高斯粒子包一个拉伸二十面体壳，利用 GPU RT core 做硬件加速射线-三角面求交
- **adaptive clamping**：根据粒子不透明度动态调整壳大小，减少 3 倍计算量
- **k-buffer 步进**：一次射线抓取最近 k=16 个粒子，排序后计算颜色，再发新射线继续

**3DGUT 折中方案**：不换渲染器，只换投影公式。
- EWA splatting：一阶泰勒展开近似投影函数 → 对鱼眼失效
- **无迹变换(UT)**：用 7 个 sigma points 代表高斯粒子，分别投影后重构 2D 高斯 → 任意投影函数都适用

**选型建议**：
- 只需要鱼眼/卷帘快门 → 3DGUT（速度无损）
- 需要反射/折射/实例化 → 3DGRT（付速度代价）

### 2. 场景图： heterogeneous representation

OmniRe 的核心设计哲学：**场景里的每个东西用最适合的方式表示**。

| 节点类型 | 表示 | 适用对象 | 操控方式 |
|---|---|---|---|
| 静态节点 | 3D 高斯 | 建筑、道路、树木 | 不可动 |
| 刚体节点 | 局部高斯 + SE(3) | 车辆 | 改变换矩阵 |
| SMPL 节点 | SMPL 网格 + 高斯绑定 | 行人 | 改关节角度 |
| 可变形节点 | 共享变形网络 + 实例嵌入 | 骑自行车的人、婴儿车 | 神经网络变形 |

**力量来源**：解耦。每个物体独立建模、独立优化、独立操控。SMPL 提供几何先验和关节级控制，高斯提供外观细节。

### 3. 动态场景：三种思路

**4DGS（时空统一）**：
- 把 (x,y,z,t) 当成一个 4D 空间，粒子是 4D 高斯椭球
- 4D 旋转让椭球在时空中倾斜 → 自然涌现运动
- 渲染时从 4D 高斯"切"出 3D 切片
- **假设**：所有动态都可以用平滑椭球覆盖

**FreeTimeGS（短寿命接力）**：
- 每个高斯有 µt（出生时间）、s（寿命）、v（速度）
- 运动函数：µx(t) = µx + v · (t - µt)，t ∈ [µt, µt+s]
- **假设**：复杂运动 = 多个短程线性运动的叠加

**对比**：4DGS 假设"一个高斯贯穿全视频"；FreeTimeGS 假设"多个高斯接力覆盖"。前者对平滑运动优雅，后者对突变/大运动更稳定。

### 4. 深度先验：Prompting 范式

Prompt Depth Anything 的核心不是深度估计，而是** prompting 范式在传感器融合中的应用**。

- **基础模型**：Depth Anything v2（ViT-Large + DPT 解码器）——提供高分辨率形状理解
- **提示**：iPhone LiDAR（192×256，噪声大）——提供绝对尺度锚点
- **融合**：零初始化卷积层，训练初期输出为 0（等价于原始模型），LiDAR 信息渐进渗透

**关键洞察**：尺度信息不需要密集，只需要存在。稀疏 LiDAR 锚点足以"锚定"整个深度图的绝对尺度。

## 可迁移洞见

### "换组件 vs 换系统"

3DGUT 的启发：当系统的某一小步成为瓶颈时，先检查那一步能不能用一个"更通用但计算量不大"的近似替换，而不是直接升级整个管线。

### "短寿命 + 接力"

FreeTimeGS 的启发：复杂系统不要用一个复杂模型覆盖全部，而是拆成很多小片段，每段用简单模型。片段之间的接缝由优化自动处理。

### "多表示类型 + 统一渲染"

OmniRe 的启发：不是"选一个方法然后扩展"，而是"每个东西用最适合的方式表示，再统一组合"。

### 6. 网格提取：从高斯粒子到几何表面

3DGS 输出数百万离散高斯椭球——没有显式 mesh，不能导入传统 3D 工具。四篇论文沿不同路径解决同一问题。

| 维度 | 论文 | 核心方法 | 关键权衡 |
|------|------|---------|---------|
| 正则化+重建 | SuGaR (INRIA, 2023) | 表面对齐正则项 → Poisson 重建 | 第一个方法，但正则项是软约束 |
| 表征降维 | 2DGS (ShanghaiTech+Tübingen, 2024) | 3D椭球→2D圆盘(surfel) + depth distortion loss | 几何从表征层面保证，非后处理 |
| 不透明度场 | GOF (Tübingen, 2024) | 高斯不透明度场 → level-set → Marching Tetrahedra | 最完整/平滑，无边界场景适用 |
| 点云采样 | 3DGS-to-PC (2025) | 概率密度采样 + 马氏距离过滤 | 灵活可定制，输出点云非 mesh |

**SuGaR → 2DGS → GOF 演进逻辑**：SuGaR 加正则"逼"高斯贴表面 → 2DGS 从根上把椭球换圆盘让表面对齐天然成立 → GOF 不改变表征求改提取方案，在不透明度场找等值面。

**2DGS 的关键洞察**：表面是 2D 的，3D 椭球天然不适合表示表面。把高斯从 3D 降维为 2D 圆盘 = 从表征层面解决了表面提取问题，而非后处理修补。

## 来源

| 维度 | 论文 | PDF 路径 |
|------|------|---------|
| 网格提取 | SuGaR (2023) | `raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2023-SuGaR.pdf` |
| 网格提取 | 2DGS (2024) | `raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2024-2D Gaussian Splatting.pdf` |
| 网格提取 | GOF (2024) | `raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2024-Gaussian Opacity Fields.pdf` |
| 网格提取 | 3DGS-to-PC (2025) | `raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2025-3DGS-TO-PC.pdf` |

| 论文 | PDF 路径 | Denote 笔记 |
|---|---|---|
| 3D Gaussian Ray Tracing | `raw/papers/paper/E-神经渲染/3D Gaussian Ray Tracing Fast Tracing of Particle Scenes.pdf` | `~/Documents/notes/20260430T102938--paper-3d-gaussian-ray-tracing__paper.md` |
| 3DGUT | `raw/papers/paper/E-神经渲染/2025-3DGUT Enabling Distorted Cameras and Secondary Rays in Gaussian Splatting.pdf` | `~/Documents/notes/20260430T103537--paper-3dgut__paper.md` |
| OmniRe | `raw/papers/paper/E-神经渲染/2025-OMNIRE OMNI URBAN SCENE RECONSTRUCTION.pdf` | `~/Documents/notes/20260430T104915--paper-omnire__paper.md` |
| 4D Gaussian Splatting | `raw/papers/paper/E-神经渲染/REAL-TIME PHOTOREALISTIC DYNAMIC SCENE REPRESENTATION AND RENDERING WITH 4D GAUSSIAN.pdf` | `~/Documents/notes/20260430T110316--paper-4d-gaussian-splatting__paper.md` |
| FreeTimeGS | `raw/papers/paper/E-神经渲染/TargetWorks/3DGS路线/2025-FreeTimeGS Free Gaussian Primitives at Anytime and Anywhere.pdf` | `~/Documents/notes/20260430T110838--paper-freetimegs__paper.md` |