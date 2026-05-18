---
title: "3DGS 转 Mesh 四篇论文合成：从高斯粒子到几何表面的演进"
created: 2026-05-13
updated: 2026-05-13
type: query
tags: [paper, 3dgs, mesh-extraction, surface-reconstruction, geometry]
sources:
  - raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2023-SuGaR Surface-Aligned Gaussian Splatting.pdf
  - raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2024-2D Gaussian Splatting for Geometrically Accurate Radiance Fields.pdf
  - raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2024-Gaussian Opacity Fields Efficient and Compact Surface Reconstruction in Unbounded Scenes.pdf
  - raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2025-3DGS-TO-PC.pdf
confidence: high
---

# 3DGS 转 Mesh 四篇论文合成：从高斯粒子到几何表面的演进

## 核心问题

3DGS 渲染质量好、速度快，但它的输出是**数百万个离散的 3D 高斯椭球**——没有显式表面，没有 mesh，不能导入传统 3D 软件。四篇论文从不同角度解决同一个问题：**如何从 3DGS 的高斯粒子中恢复出干净的几何表面**。

## 论文对比

| 维度 | SuGaR (2023) | 2DGS (2024) | GOF (2024) | 3DGS-to-PC (2025) |
|------|-------------|-------------|------------|-------------------|
| **机构** | INRIA | 上海科技+Tübingen | Tübingen+CTU | — |
| **输出** | Mesh | Mesh + 法线 | Mesh (tetrahedral) | **Point Cloud** |
| **核心思想** | 加正则项让高斯贴表面 → Poisson重建 | 高斯降维：3D椭球→2D圆盘（surfels） | 直接在高斯不透明度场中提取 level-set | 从高斯概率采样 + 马氏距离过滤 |
| **关键创新** | 第一个 3DGS→mesh 方法 | 2D surfels 天然对齐表面 + depth distortion loss | 直接识别等值面，跳过 TSDF 融合 | 灵活可定制的高斯→点云框架 |
| **渲染质量** | 保持 3DGS 水平 | 保持实时 + 高质量 | 保持高保真 | 不渲染（只输出点云） |
| **几何质量** | 中（依赖正则项效果） | 高（2D disk = 天然表面） | 最高（complete/smooth/detailed） | 高精度密集点云 |

## 演进脉络

```
3DGS (2023) — 数百万离散高斯椭球，只有渲染没有表面
    │
    ▼
SuGaR (2023) — 第一个尝试：加正则项让高斯贴表面 → Poisson重建
    问题：依赖正则化，高斯不一定完美对齐表面
    │
    ▼
2DGS (2024) — 根本性创新：把高斯从 3D 椭球降维成 2D 圆盘（surfel）
    → 2D disk 有明确的法线方向 → 表面自然涌现
    → 引入 depth distortion loss + normal consistency loss
    优势：不需要后处理正则，几何从表征层面保证
    │
    ├──→ 3DGS-to-PC (2025) — 旁支：不改表征，直接从高斯概率密度采样点云
    │                                    + 马氏距离过滤离群点
    │
    ▼
GOF (2024) — 更高维的解法：建立高斯不透明度场
    → 直接识别 level-set（等值面）作为表面
    → 用四面体网格（tetrahedral mesh）+ Marching Tetrahedra 提取
    → 相比传统 TSDF 融合深度图的方法：更完整、更平滑、更细节
```

## 关键技术点

### SuGaR：正则化 + Poisson 重建

- 在 3DGS 训练过程中加入**表面对齐正则项**，鼓励高斯椭球的最短轴与表面法线对齐
- 优化后，从对齐的高斯中采样点 → Poisson Surface Reconstruction → 提取 mesh
- 局限：正则项是软约束，不是硬保证

### 2DGS：表征层面的突破

- **核心洞察**：3D 高斯椭球天然不适合表示表面——表面是 2D 的
- 将高斯从 3D 降维为 2D 圆盘（surfel = surface element），每个 disk 有位置、法线、半径、颜色
- **Depth Distortion Loss**：约束 disk 沿射线方向集中，防止多个 disk 叠加在同一条射线上
- **Normal Consistency Loss**：邻近 disk 的法线方向一致性
- 渲染用 2D Gaussian Splatting（ray-splat intersection 的闭式解），速度接近原生 3DGS

### GOF：不透明度场 + 四面体网格

- 不依赖正则项，不改变高斯表征——直接对 3DGS 的输出构建**高斯不透明度场**
- 在不透明度场中找 level-set → 用 Marching Tetrahedra 提取三角 mesh
- 相比基于渲染深度图的 TSDF 融合方案：消除噪声、填补空洞、平滑表面
- 适用于无边界场景（unbounded scenes）

### 3DGS-to-PC：概率采样框架

- 将每个高斯视为一个 3D 概率密度函数（μ, Σ）→ 从中按概率采样点
- 用**马氏距离**（Mahalanobis distance）阈值过滤极端离群点
- 输出密集、高精度点云（而非 mesh）
- 灵活可定制：可控制密度/精度/噪声容忍度

## 与 wiki 现有知识的关联

- `concepts/3d-gaussian-splatting.md` — 本方向是 3DGS 技术栈的"几何提取"子方向
- `concepts/neural-radiance-field.md` — NeRF 也有 mesh 提取问题（如 NeRF2Mesh），3DGS 的 mesh 提取更直接
- `concepts/graphics-to-world-model.md` — GOF 的不透明度场 level-set 本质上是在做"从渲染表征到物理几何"的 Real2Sim 第一步

## 相关笔记
- [[3d-gaussian-splatting]] — 3D Gaussian Splatting 技术栈
- [[sim-ready-asset-generation]] — Sim-ready Asset Generation

## 来源

| 论文 | PDF 路径 |
|------|---------|
| SuGaR (2023) | `raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2023-SuGaR.pdf` |
| 2DGS (2024) | `raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2024-2D Gaussian Splatting.pdf` |
| GOF (2024) | `raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2024-Gaussian Opacity Fields.pdf` |
| 3DGS-to-PC (2025) | `raw/papers/paper/E-神经渲染/3DGS-ReconsMesh/2025-3DGS-TO-PC.pdf` |
