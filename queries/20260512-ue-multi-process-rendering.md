---
title: "UE5 Multi-Process Rendering：多进程替代多 GPU 的渲染架构"
created: 2026-05-12
updated: 2026-05-12
type: query
tags: [article, unreal-engine, rendering, multi-gpu, ndisplay, virtual-production]
sources:
  - Clippings/Multi-Process Rendering Introduction.md
  - Clippings/Getting Started with Multi-Process Rendering in Unreal Engine  Unreal Engine 5.7 Documentation.md
  - Clippings/Converting from mGPU to Multi-Process Rendering in Unreal Engine.  Unreal Engine 5.7 Documentation.md
confidence: high
---

# UE5 Multi-Process Rendering：多进程替代多 GPU 的渲染架构

## 核心观点

UE 5.2 引入的 Multi-Process Rendering (MPR) 是 nDisplay 多 GPU 策略的根本性转向：不再让多张 GPU 通过 NVLink/SLI 共享内存（mGPU 模式），而是**每张 GPU 跑一个独立的 UE 进程**，进程间只传输最终渲染纹理。这不仅性能更好，而且解除了对 NVLink 的硬件依赖——ADA Lovelace 架构的 GPU 不再支持 NVLink，MPR 是强制迁移路径。

## 关键要点

1. **mGPU vs MPR：架构差异**
   - mGPU（4.27 引入）：两张 GPU 共享全部 GPU 内存，通过 NVLink + SLI 高带宽互联。CPU 上只有一个 UE 进程。问题：NVLink 带宽瓶颈 + SLI 已被 NVIDIA 放弃
   - MPR（5.2 引入）：每张 GPU 启动独立 UE 进程（onscreen node + offscreen node）。GPU 间仅通过 CPU/主板传输最终渲染纹理，不共享内存
   - 性能结论：大多数场景中 MPR 优于 mGPU。EPIC 推荐默认使用 MPR

2. **工作原理：双进程分工**
   - onscreen node（主 GPU）：正常渲染，负责输出到 LED 墙/显示器
   - offscreen node（副 GPU）：渲染内视锥（inner frustum），将结果作为纹理回传给 onscreen node
   - onscreen node 合成两者的画面 → 最终输出
   - 两个进程各自拥有独立的 GPU 内存空间

3. **硬件前置条件**
   - 至少两张 GPU
   - **必须禁用 SLI**——如果使用 NVIDIA Mosaic，不能设为 Premium Mosaic（会自动启用 SLI）
   - 建议禁用 Intel Hyper-Threading / AMD SMT
   - ADA Lovelace GPU 只能用 MPR（无 NVLink 支持）

4. **从 mGPU 迁移到 MPR 的关键变更**
   - mGPU 配置中启用 SLI + NVLink → MPR 中必须关闭
   - mGPU 的 nDisplay 集群中每个渲染节点只启动 1 个 UE 实例 → MPR 启动 2 个
   - mGPU 依赖 GPU 间内存共享 → MPR 依赖 GPU 间纹理传输（CPU/主板带宽）

## 与 SLI/NVLink 的历史关系

MPR 的出现标志着多 GPU 渲染从"硬件层面统一"到"软件层面协作"的范式迁移。SLI（2004-2022）的核心假设是"让多张 GPU 假装成一张"——但现代 GPU 的计算能力已超过 SLI 桥的通信带宽所能支撑的数据共享量。MPR 的做法恰恰相反：承认 GPU 是独立的，只在边界处交换数据。

## 相关笔记
- [[20260512-gpu-communication-tech]] — GPU 通信技术全景：GPU Direct、NVLink、RDMA 与 SLI
- [[20260512-ue-ndisplay-overview]] — nDisplay 技术总览：实时内容的多屏无限制缩放
- [[20260512-wayland-protocol-architecture]] — Wayland 协议与架构详解：为什么 X11 必须被替代
- [[20260514-ue-digital-twin-development-guide]] — UE 数字孪生开发流程与前沿展望 v4.0

## 来源

- 原文：[[Clippings/Multi-Process Rendering Introduction.md]]
- 原文：[[Clippings/Getting Started with Multi-Process Rendering in Unreal Engine  Unreal Engine 5.7 Documentation.md]]
- 原文：[[Clippings/Converting from mGPU to Multi-Process Rendering in Unreal Engine.  Unreal Engine 5.7 Documentation.md]]
