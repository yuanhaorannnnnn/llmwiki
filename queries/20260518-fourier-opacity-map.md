---
title: "Fourier Opacity Map：用傅里叶级数解决顺序无关透明渲染"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, wechat, rendering, graphics, transparency, oit, fourier, unreal-engine, shader]
sources: [raw/articles/20260518-wechat-BGjT__9N4du8lwI7gKOBKg.md]
source_url: https://mp.weixin.qq.com/s/BGjT__9N4du8lwI7gKOBKg
confidence: high
rating: 6
---

# Fourier Opacity Map：用傅里叶级数解决顺序无关透明渲染

## 核心观点

传统半透明渲染依赖片元排序——顺序错了，效果全错。Fourier Opacity Map 用一条巧妙的数学链路彻底解除排序依赖：**Alpha 混合（线性）→ Beer-Lambert 定律（物理吸收）→ 狄拉克函数（离散→连续）→ 傅里叶级数（积分解析解）**。最终效果是：无论片元以什么顺序提交，GPU 都能并行计算出正确的透光率。这是一次将传统图形学问题转化为数学解析解的经典示范。

## 关键要点

### 1. 从 Alpha 混合到物理吸收：四步数学转换

**Step 1 — Alpha → 吸收系数**
传统的 `alpha * color + (1-alpha) * background` 转为物理吸收模型：
```
α' = -2 * log(max(1 - α, 0.00001))
```
此变换源于透射率 `T = e^(-τ)` 与 `(1-α)` 的等价关系。

**Step 2 — 离散片元 → 连续密度函数**
用狄拉克 δ 函数将离散片元建模为连续密度分布：
```
d(z) = Σ α'_i · δ(z - z_i)
```
这一步将"按深度排序逐个求和"变成了"对深度变量的连续积分"。

**Step 3 — 积分 → 傅里叶级数解析解**
将密度函数展开为傅里叶级数，积分 `∫ d(z) dz` 变成对 sin/cos 项积分——每个 sin/cos 项的积分有闭合解析式。傅里叶系数 **与片元提交顺序无关**，只与片元深度和 α 值有关。

**Step 4 — 重构累积光学深度**
在着色点深度 `z` 处，只需要查表傅里叶系数 + 计算基函数值，就能得到该深度的累积光学深度 `τ(z)`，进而计算出准确的透光率。

### 2. 两 Pass GPU 实现

**Pass 1 — 生成 Fourier Opacity Map（MRT 输出）**
```hlsl
// 对每个片元，累加傅里叶系数的贡献（加法混合）
float IntegratedDensity = -2 * log(max(1.0 - Density, .00001f));
// OutColor0: [a_0, a_1·cos, a_2·cos, a_3·cos]
// OutColor1: [0,    b_1·sin, b_2·sin, b_3·sin]
// 使用 3 项傅里叶级数（k=1,2,3）
```
加法混合自动累加所有片元贡献到 MRT 纹理 → 得到完整傅里叶系数。

**Pass 2 — 从 Fourier Opacity Map 重构阴影**
```hlsl
// 读取累积的傅里叶系数
// 在着色点深度计算基函数值
// τ(z) = (a_0·z)/2 + Σ(a_k·sin(kωz)/(kω) + b_k·(1-cos(kωz))/(kω))
// 直接得到该深度的累积光学深度
```

### 3. 两个关键工程优化

**归一化（Normalization）**
- 问题：傅里叶级数截断 + 吉布斯现象 → 亮部更亮、暗部更暗
- 解决：`C_final = (Σ C_i·α'_i / Σ α'_i) · (1 - e^(-Σ α'_i))`
- 本质：将颜色贡献做加权平均，再乘以总透光率缩放因子

**振铃抑制（Ringing Suppression）**
```hlsl
#define RingingSuppressionScale(k) \
  (exp(-RingingSuppressionFactor * Square(k / NumTermsForRingingSuppression)))
```
- 高斯衰减函数对高频傅里叶系数加权
- 低频项（k=1）权重接近 1，保持主要形状
- 高频项（k=3+）权重指数衰减，平滑不连续点附近的过冲/欠冲
- 效果：消除阴影边界的伪影

### 4. 算法限制

- 使用 **3 项傅里叶级数**（原作），对大多数场景足够，但极复杂透明层叠可能欠拟合
- 两 MRT 的显存带宽开销（两个 float4 纹理）
- 对极高频率的几何细节，RingingSuppression 可能过度平滑

## 与已有知识的关联

- [[20260512-alpha-compositing-guide]] — 本文是该笔记中"顺序依赖透明混合"问题的数学解
- [[3d-gaussian-splatting]] — 3DGS 使用体渲染沿光线累积颜色，本质也是 Beer-Lambert 定律的积分形式
- [[neural-radiance-field]] — NeRF 体渲染沿光线采样累积，与本文的连续密度函数积分同构
## 相关笔记
- [[20260512-alpha-compositing-guide]] — Alpha 融合（Alpha Compositing）技术详解：从公式到实践陷阱
- [[3d-gaussian-splatting]] — 3D Gaussian Splatting 技术栈
- [[neural-radiance-field]] — Neural Radiance Field (NeRF) 技术栈

## 来源

- [[raw/articles/20260518-wechat-BGjT__9N4du8lwI7gKOBKg.md]]
- 知乎原文：https://zhuanlan.zhihu.com/p/1967330216536933895
