---
title: "ADAS 测试体系及其在量产项目中的实践"
created: 2026-05-13
updated: 2026-05-13
type: query
tags: [presentation, adas, autonomous-driving, testing, v-model, simulation, mass-production]
sources: [raw/articles/20260513-adas-testing-system-mass-production.md]
confidence: medium
---

# ADAS 测试体系及其在量产项目中的实践

## 核心观点

这份 34 页 PPT 是一线 ADAS 量产实践的测试体系总结。核心逻辑是 **V 模型开发流程在 ADAS 领域的实例化**：从系统需求出发 → 逐层分解到软件/硬件单元 → 单元测试 → 集成测试 → 系统验证。覆盖 ADAS 典型架构（感知-融合-定位-决策-规控的完整功能族），仿真开发实践（从 MIL/SIL 到 HIL/VIL），以及实车道路测试的体系化方法论。

## 关键要点

### 1. ADAS 测试体系总览：V 模型 + 测试金字塔

```
系统需求 ──→ 系统测试（实车道路 + 场地）
    │
    ▼
架构设计 ──→ 集成测试（HIL 硬件在环 + VIL 车辆在环）
    │
    ▼
软件需求 ──→ 软件测试（SIL 软件在环）
    │
    ▼
详细设计 ──→ 单元测试（MIL 模型在环）
```

- V 模型左边是"逐层分解"，右边是"逐层验证"
- 越底层测试越自动化、越可重复；越顶层越接近真实场景、成本越高

### 2. 典型 ADAS 系统架构分层

| 层级 | 内容 |
|------|------|
| **功能族** | 泊车辅助 / 行车辅助 / 领航功能 |
| **感知融合** | Freespace 检测、视觉感知（OB&Line）、车位 BEV 感知、多传感器融合 |
| **定位** | 高精定位算法、姿态估计、动态标定 |
| **决策规划** | 决策模型、规控算法 |
| **基础软件** | 操作系统、中间件、通讯组件、协议栈、健康管理、OTA |
| **硬件** | Radar、LiDAR、USS、IMU、HDMap、总线、Switch、相机、CPU/GPU |

### 3. 仿真系统开发与测试实践

四个等级的仿真测试环：

| 级别 | 缩写 | 说明 | 成本/保真度 |
|------|------|------|-----------|
| 模型在环 | **MIL** | 纯算法模型，无真实硬件 | 最低成本，快速迭代 |
| 软件在环 | **SIL** | 实际代码运行在 PC 上 | 验证软件逻辑 |
| 硬件在环 | **HIL** | 真实 ECU + 仿真环境 | 验证硬软件集成 |
| 车辆在环 | **VIL** | 实车 + 仿真传感器输入 | 最接近真实，用于最终验证 |

测试场景来源：真实路采数据回灌 → 场景提取 → 参数化变体生成 → 仿真场景库。

### 4. 实车道路测试

- 场地测试（封闭道路）：标准工况、边界工况、失效模式
- 公开道路测试：ODD（运行设计域）内多样化路况积累里程
- 数据闭环：实车测试中暴露的问题 → 回灌到仿真场景库 → MIL/SIL/HIL 复现 → 修复 → 回归测试
- 关键 KPI：每千公里干预次数、场景覆盖率、回归测试通过率

## 与 wiki 现有知识的关联

- `concepts/graphics-to-world-model.md` — 仿真作为测试环境的理论框架在此得到了工程实例化（MIL→SIL→HIL→VIL）
- `concepts/sim-ready-asset-generation.md` — ADAS 仿真场景需要大量 sim-ready 资产（车辆、行人、道路），PhysX-Anything 类技术可降低场景构建成本
- `concepts/redundancy-based-reliability-estimation.md` — ADAS 多传感器融合的可靠性评估可借鉴冗余估计方法论

## 来源

- PDF：[[raw/notes/归档/竞品资料/ADAS测试体系及其在量产项目中的实践.pdf]]
- 原始文本：[[raw/articles/20260513-adas-testing-system-mass-production.md]]
