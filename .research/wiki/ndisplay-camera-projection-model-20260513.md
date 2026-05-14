# 深度研究报告：nDisplay 相机投影模型与多屏拼接原理

> 研究范围：nDisplay 的 off-axis projection、多屏拼接优于手动拼接的根因、ICVFX inner/outer frustum 模型、FOV 计算
> 信息源：本地 clippings（4 个）、外部 web（Epic 官方文档 + 80.lv 深度解析 + UE 论坛 + NVIDIA 同步文档）
> 研究深度：Deep

## 1. 研究概述

### 1.1 核心问题

为什么 nDisplay 拼接多个屏幕/投影仪比手动在引擎里摆多个 Camera、手动拼画面效果好？拼接后的相机投影模型是什么？FOV 如何计算？

### 1.2 关键发现（TL;DR）

- **nDisplay 的根本优势不在"画"，在"同步"**：硬件级 genlock + framelock 保证所有渲染节点在同一 v-blank 时刻 swap buffer，手动摆 Camera 根本做不到这点——GPU 各自跑各自的时钟，画面边界必然撕裂
- **nDisplay 的投影模型是 off-axis（非对称）投影**：每个屏幕根据其 3D 位置、尺寸和 View Origin 自动生成非对称视锥体。手动方式必须自己计算每个屏幕的 projection matrix，一旦屏幕或相机位置变了全部重算
- **Inner/Outer Frustum 是对"摄像机看见的 LED 墙"和"其余 LED 墙"的物理分工**：Inner 跟追踪摄像机实时偏移（产生 parallax），Outer 静态用于灯光/反射
- **FOV 的三个层次**：(1) UE 相机 FOV = 水平 FOV，垂直由 AR 推导 → (2) Maintain Axis 规则决定多屏不同比例时的缩放策略 → (3) nDisplay 的 FOVMultiplier 做 overscan 补偿延迟

## 2. nDisplay vs 手动拼接：根本差异

### 2.1 手动摆 Camera 的四个致命缺陷

| 问题 | 手动方案 | nDisplay 方案 |
|------|---------|--------------|
| **帧同步** | 每台机器的 GPU 独立跑时钟，swap buffer 时刻不同——画面边界撕裂 | Quadro Sync II genlock（外部时钟）+ framelock（RJ45 菊花链），所有节点同一微秒 swap |
| **视锥体计算** | 每块屏幕手动算 asymmetric projection matrix，一旦屏幕/相机位置变全部重来 | 自动从屏幕 3D 位置+View Origin 生成 off-axis frustum |
| **集群管理** | 手动 SSH 到每台机器启动 UE，手动关 | Switchboard 一键启动/管理所有节点 |
| **边缘融合** | 自己写 shader 做 edge blend | 内置 post-process edge blending |

### 2.2 帧同步是物理层面的差距

手动方案里即使你在代码层面把 camera 参数算对了，**物理上无法保证多台机器的 GPU 在同一帧的同一像素位置显示的是同一个逻辑帧的数据**。每台机器的 GPU clock 有微小差异，swap buffer 时刻错开 1-2ms 就会在屏幕边界产生可见撕裂。

nDisplay 的做法是：
```
外部 sync generator (tri-level)
    → BNC → Master Quadro Sync II (genlock 输入)
              → RJ45 → Slave Quadro Sync II → ... (framelock 菊花链)
```

- **Genlock**：所有 GPU 的 raster scan 被锁定到同一个外部时钟，每个像素在同一时刻开始渲染
- **Framelock**：Master Quadro Sync II 在 v-blank 时刻发出脉冲，所有节点的 swap buffer 同步翻转

**关键限制**：硬件同步必须用 Quadro 级 GPU（RTX A 系列），消费级 RTX 2080/3080/4080 没有 Quadro Sync II 支持。软件同步（`swap_sync_policy=1`）存在但不保证帧完美锁定。

## 3. 拼接后的相机投影模型

### 3.1 核心概念：Off-axis / Asymmetric Frustum

当观众（或被追踪的相机）偏离屏幕中心时，标准的对称视锥体会产生透视扭曲。nDisplay **为每个屏幕生成一个非对称视锥体**，其参数由以下三者决定：
- 屏幕在 3D 空间中的位置 + 旋转 + 尺寸
- 观众的 View Origin（眼点位置）
- 屏幕的实际物理几何

直觉类比：你站在一扇窗户前。窗户在你的左边——你看到的左边玻璃上的画面应该是"从你眼睛向左看出去能看到的东西"，右边玻璃同理。nDisplay 自动为每块"玻璃"计算精确的非对称视锥。

### 3.2 四种投影策略（Projection Policies）

| 策略 | 视锥体来源 | 拼接方式 | 适用场景 |
|------|-----------|---------|---------|
| **Simple** | 屏幕矩形 3D 位置 + View Origin → 自动 off-axis frustum | 所有屏幕共享同一个 View Origin，边自动对齐 | 平面墙、简单多屏 |
| **Camera** | 绑定 UE CineCameraActor | 通过 ICVFX Camera 组件追踪物理摄像机 | 虚拟制片 LED 墙 (ICVFX) |
| **Mesh** | 屏幕几何用 3D mesh 定义 + UV channel 0 做 warp map | 通过相邻 mesh 的 UV 对齐实现拼接 | 曲面 LED 墙、穹顶投影 |
| **Manual** | 手动提供 4×4 projection matrix 或 frustum angles | 用户全手动计算拼接 | 非标投影系统、motion platform |

**Simple Policy = 手动方案的自动化**：你只要告诉 nDisplay 屏幕在哪、多大，它自动算 asymmetric frustum。这就是 nDisplay 比手动摆 Camera 好的核心工程差异。

### 3.3 Inner Frustum vs Outer Frustum（虚拟制片专有）

```
┌──────────────────────────────────────┐
│             LED Wall                 │
│  ┌──────────────────────┐            │
│  │                      │            │
│  │    Inner Frustum     │  ← 跟踪摄像机看见的区域
│  │    (全质量渲染)       │     跟随 LiveLink 实时偏移
│  │                      │     产生 parallax 效果
│  └──────────────────────┘            │
│  Outer Frustum                      │
│  (降低质量渲染)  ← 用于灯光/反射     │
│  静态 DefaultViewPoint              │
│  不跟随摄像机移动                    │
└──────────────────────────────────────┘
```

- **Inner Frustum**：摄像机从当前位置通过镜头能看到的那部分 LED 墙。**实时跟踪摄像机移动**，产生正确的 parallax。全分辨率渲染。
- **Outer Frustum**：LED 墙上摄像机视野以外的部分。**用 DefaultViewPoint 做投影原点**，不跟摄像机移动（因为真实世界里墙面反射不跟摄像机）。可降分辨率和质量渲染，主要用途是给演员/道具提供动态灯光和反射。
- **FOVMultiplier**（Overscan Multiplier, 0.05-5.0）：增加 inner frustum 尺寸，给摄像机移动时的渲染延迟留缓冲。如果摄像机快速旋转（whip pan），overscan 防止边缘出现黑色未渲染区域。

## 4. FOV 计算

### 4.1 UE 基础 FOV 模型

UE 中 Camera 组件的单个 FOV 值是**水平 FOV (α)**。垂直 FOV (β) 由以下关系推导：

```
tan(β/2) = tan(α/2) / AR_cam
```

其中 `AR_cam = ViewportWidth / ViewportHeight`。

### 4.2 Maintain Axis 规则——多屏不同比例时的行为

当 nDisplay 的不同屏幕有不同分辨率/比例时，Maintain Axis 决定 FOV 如何调整：

| 模式 | 行为 | 公式 |
|------|------|------|
| **Maintain Y** | 垂直 FOV 不变，水平拉伸/收缩 | α_new = 2 · atan(AR_new · tan(β/2)) |
| **Maintain X** | 水平 FOV 不变，垂直拉伸/收缩 | β_new = 2 · atan(tan(α/2) / AR_new) |

默认：
- Gameplay Camera → Maintain Y（游戏画面默认保持垂直视野不变）
- SceneCaptureComponent2D → 硬编码等效 Maintain X（水平 FOV 保持）

### 4.3 投影矩阵中的 FOV 计算

`CalculateProjectionMatrixGivenViewRectangle()` 实现：

```cpp
// Maintain Y
XAxisMultiplier = SizeY / SizeX;
YAxisMultiplier = 1.0f;
HalfYFOV = atan(tan(HalfXFOV) / ViewInfo.AspectRatio);
MatrixHalfFOV = HalfYFOV;

// Maintain X
XAxisMultiplier = 1.0f;
YAxisMultiplier = SizeX / SizeY;
MatrixHalfFOV = HalfXFOV;
```

`FReversedZPerspectiveMatrix(MatrixHalfFOV, MatrixHalfFOV, XAxisMultiplier, YAxisMultiplier, NearClip, NearClip)` 构建最终投影矩阵。两个 multiplier 的作用是"补偿当前宽高比"，保证预期轴保持固定。

### 4.4 nDisplay 特有：Overscan & Custom Frustum

nDisplay 的 `DisplayClusterConfigurationICVFX_CameraCustomFrustum` 提供**每方向独立 overscan 控制**：

| 参数 | 作用 |
|------|------|
| `Left/Right/Top/Bottom` | 每边独立扩展（% 或 像素） |
| `FieldOfViewMultiplier` | 全局 overscan 乘数 |
| `AdaptResolution` | 选择 overscan 是增加渲染分辨率还是缩放 |

**使用场景**：
- Whip pan 只往一个方向 → 只扩展该方向的 overscan
- 双机位拍摄 → inner frustum 扩展覆盖两个机位
- 大型置景遮挡 → 减少被遮挡侧的 overscan 省 GPU

## 5. 帧同步机制深度解析

### 5.1 两层同步

```
┌─ External Sync Generator ──┐
│  (tri-level, HDTV clock)   │
└──────────┬─────────────────┘
           │ BNC
           ▼
┌─────────────────────────┐
│  Master Quadro Sync II  │  ← genlock 输入：锁定 raster scan
│  (slot 1 of master node)│
└──────────┬──────────────┘
           │ RJ45 daisy-chain
           ▼
┌─────────────────────────┐
│  Slave Quadro Sync II   │  ← framelock：锁定 swap buffer flip
│  (slot 1 of slave node) │
└──────────┬──────────────┘
           │ RJ45
           ▼
         ...  (继续菊花链)
```

### 5.2 SW vs HW Sync

| 指标 | swap_sync_policy=1 (SW) | swap_sync_policy=2 (HW) |
|------|------------------------|------------------------|
| 依赖 | 网络时间协议 | Quadro Sync II 硬件 |
| GPU 要求 | 任何 GPU | Quadro 级（RTX A 系列） |
| 帧误差 | 毫秒级（取决于网络抖动） | 微秒级（硬件锁定） |
| 生产级 | 否 | 是 |

### 5.3 验证 sync 成功

- **Switchboard 节点报告**：`PresentMode: Hardware Composed: Independent Flip`（不是 `Composed: Flip`）
- **Quadro Sync II 卡 LED**：绿色 = 有效 sync 信号；红色 = 无信号
- **帧漂移检查**：物理上 sync 锁定时，节点间帧差为 0。2-10 帧差异说明 sync 完全失效

## 6. 关键技术概念总结

| 概念 | 一句话 |
|------|--------|
| Off-axis Projection | 从眼点出发，每块屏幕的非对称视锥体 |
| View Origin | 观众的 3D 位置——所有视锥体从这个点出发 |
| Projection Policy | nDisplay 生成视锥体的策略（Simple/Camera/Mesh/Manual） |
| ICVFX Camera | 绑定追踪摄像机，驱动 inner frustum 的 nDisplay 组件 |
| Inner Frustum | 摄像机看见的 LED 墙部分——全质量 + 实时跟踪 |
| Outer Frustum | LED 墙其余部分——降低质量 + 静态 + 灯光/反射 |
| Overscan | inner frustum 边缘额外渲染的像素缓冲区 |
| Genlock | 外部时钟锁定所有 GPU 的 raster scan |
| Framelock | RJ45 菊花链锁定所有 GPU 的 swap buffer flip |
| Swap Sync Policy | nDisplay 同步模式：SW (policy=1) 或 HW (policy=2) |

## 7. 信息来源

### 本地
- `Clippings/nDisplay Overview for Unreal Engine.md` — nDisplay 架构、主节点/二级节点
- `Clippings/探究nDisplay技术：实时内容的无限制缩放.md` — 应用场景、Scalable Display Manager
- `queries/20260512-ue-ndisplay-overview.md` — 之前合成的 nDisplay 总览
- `raw/notes/待阅读/unreal-engine-ndisplay-whitepaper-*.pdf` — 白皮书（图像密集，未完全提取）

### 外部 Web
- [Projection Policies in nDisplay (UE 5.6)](https://dev.epicgames.com/documentation/unreal-engine/projection-policies-in-ndisplay-in-unreal-engine) 🌐
- [In-Camera VFX Overview (UE 5.6)](https://dev.epicgames.com/documentation/unreal-engine/in-camera-vfx-overview-in-unreal-engine) 🌐
- [80.lv: UE5 Camera vs SceneCapture Deep Dive](https://80.lv/articles/deep-dive-ue5-camera-vs-scenecapture-maintain-axis-frustum-math-projection-pipeline) 🌐
- [nDisplay Synchronization with NVIDIA](https://dev.epicgames.com/documentation/ko-kr/unreal-engine/ndisplay-synchronization-with-nvidia) 🌐
- [ICVFX Camera Custom Frustum API](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/DisplayClusterConfigurationICVFX_CameraCustomFrustum) 🌐
- [GitHub/UPBGE: Off-axis projection for VP](https://github.com/UPBGE/upbge/discussions/1406) 🌐
- [Epic Forums: nDisplay sync troubleshooting](https://forums.unrealengine.com/t/problem-with-synchronization-two-unreal-instances-using-ndisplay-plugin/245875) 🌐
