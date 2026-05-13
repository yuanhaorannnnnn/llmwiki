---
title: "nDisplay 技术总览：实时内容的多屏无限制缩放"
created: 2026-05-12
updated: 2026-05-12
type: query
tags: [article, unreal-engine, ndisplay, multi-display, virtual-production, led-wall]
sources:
  - Clippings/nDisplay Overview for Unreal Engine  Unreal Engine 5.7 Documentation.md
  - Clippings/探究nDisplay技术：实时内容的无限制缩放.md
confidence: high
---

# nDisplay 技术总览：实时内容的多屏无限制缩放

## 核心观点

nDisplay 是 UE 将实时 3D 内容跨多台机器、多块屏幕、多种异形显示面同步渲染的集群系统。核心挑战不是"画出来"，而是**同步**——多台机器的每帧画面必须精确对齐边缘、同时显示、同一视角，否则肉眼可见撕裂。nDisplay 通过主节点+二级节点架构 + 共享配置资产 + VRPN/Live Link 同步输入解决了这个分布式渲染的画布拼接问题。

## 关键要点

1. **架构：主节点 + N 个二级节点**
   - 主节点：接受 VRPN/Live Link 输入（空间追踪、控制器），同步给所有二级节点。本身也参与渲染
   - 二级节点：每个运行一个 UE 实例，渲染一块或多块屏幕/投影仪
   - 所有节点由同一个配置资产（nDisplay Config Asset）描述：哪些机器、屏幕多大、在 3D 空间中的位置关系

2. **两种屏幕映射模式**
   - 一对一：每台电脑 + 一个 UE 实例 → 一台显示设备。最标准
   - 一对多：一台电脑 + 一个 UE 实例 → 多台显示设备。需要 GPU 厂商多屏技术（NVIDIA Mosaic / AMD Eyefinity）拼接成连续画幅，再用 nDisplay 输出映射工具分配视口

3. **同步机制——这是最难的部分**
   - 所有节点必须在同一帧时间点渲染各自的视口——否则画面撕裂
   - 需要硬件同步支持（NVIDIA Quadro Sync / Sync II 卡 + 支持的驱动设置）
   - 软件层面 nDisplay 插件负责帧同步 + 视角同步

4. **应用场景**
   - 虚拟制片（LED 幕墙）：nDisplay 控制多块 LED 面板上的实时背景。2019 年 Epic+Lux Machina+ARRI 联合测试是行业标杆案例
   - 现场演艺：Childish Gambino 演唱会——5 台机器渲染 5.4K×5.4K 投影到穹顶
   - 军事训练：沉浸式穹顶投影，受训者保持沉浸感的同时与战友保持物理联系
   - 建筑可视化、模拟器

5. **与 Multi-Process Rendering 的关系**
   - nDisplay 解决"怎么把画布拼接起来"（多机器同步）
   - MPR 解决"怎么让一台机器上的两张 GPU 高效协作"（单节点内部的多 GPU）
   - 两者可以叠加使用：nDisplay 集群 + 每个节点跑 MPR

## 来源

- 原文：[[Clippings/nDisplay Overview for Unreal Engine  Unreal Engine 5.7 Documentation.md]]
- 原文：[[Clippings/探究nDisplay技术：实时内容的无限制缩放.md]]
