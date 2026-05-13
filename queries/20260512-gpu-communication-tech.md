---
title: "GPU 通信技术全景：GPU Direct、NVLink、RDMA 与 SLI"
created: 2026-05-12
updated: 2026-05-12
type: query
tags: [article, gpu, nvidia, nvlink, gpudirect, rdma, sli, multi-gpu]
sources:
  - Clippings/聊透 GPU 通信技术——GPU Direct、NVLink、RDMA.md
  - Clippings/SLI.md
confidence: high
---

# GPU 通信技术全景：GPU Direct、NVLink、RDMA 与 SLI

## 核心观点

GPU 通信技术本质上是解决同一个问题在不同物理尺度上的不同方案：**如何让数据绕过 CPU 直接到达 GPU**。物理距离决定了技术选择——机箱内用 NVLink/NVSwitch，跨机用 RDMA + InfiniBand/RoCE，跨存储用 GPUDirect Storage。SLI 是这个谱系中的历史产物：它是 2004 年开始的"让多 GPU 假装成一张"的思路，已被 NVLink（2016-2024）和 Multi-Process Rendering（2022-）分别在硬件和软件层面取代。

## 通信技术分层

```
单 GPU 内       → CUDA 内存模型
同机箱 GPU 间   → NVLink / NVSwitch（900 GB/s）、PCIe（64 GB/s x16）
                    历史：SLI（2004-2022，桥接器，1-2 GB/s）
GPU ↔ 存储      → GPUDirect Storage（绕过 CPU，直通 NVMe SSD）
GPU ↔ 网卡      → GPUDirect RDMA（GPU → NIC → 远端 GPU，绕过双方 CPU）
GPU ↔ 远端 GPU  → RDMA over InfiniBand/RoCE（跨节点，微秒级延迟）
```

## 关键技术详解

### 1. GPUDirect 系列——绕过 CPU 的通信范式

| 技术 | 解决的问题 | 数据路径 |
|------|-----------|---------|
| GPUDirect P2P | 同机箱多 GPU 直接访问对方显存 | GPU A ↔ GPU B（不经过 CPU 内存） |
| GPUDirect RDMA | 远端 GPU 直接访问本地 GPU 显存 | 远端 GPU → 本地 NIC → 本地 GPU（绕过本地 CPU） |
| GPUDirect Storage | 存储设备直接向 GPU 传输数据 | NVMe SSD → GPU（绕过 CPU 内存） |
| GPUDirect Video | 视频采集卡直接向 GPU 输送帧数据 | 采集卡 → GPU（绕过 CPU） |

### 2. NVLink & NVSwitch——SLI 的终极替代者

- **SLI (2004-2022)**：外部桥接器连接多张 GPU，共享工作负载。五模式：AFR（交替帧渲染）、SFR（分帧渲染）、AFR of SFR（混合）、Boost Hybrid（异构 GPU）、SLIAA（抗锯齿增强）、兼容模式（单 GPU）
- **NVLink (2016)**：取代 SLI 的 GPU 互联，带宽从 SLI 的 ~1-2 GB/s 提升到 900 GB/s（NVSwitch on H100）
- **NVSwitch**：连接多张 GPU 的交换芯片，使任意两张 GPU 之间的通信带宽不受拓扑限制
- **关键转折**：ADA Lovelace（RTX 40 系列）不再支持 NVLink——NVIDIA 在多 GPU 策略上从硬件共享转向软件协作

### 3. RDMA 与网络——跨节点 GPU 通信

- RDMA（Remote Direct Memory Access）：网卡直接读写 GPU 显存，绕过远端 CPU 和内核
- 传输层选择：InfiniBand（极低延迟，HPC/AI 训练首选）vs RoCE v2（RDMA over Converged Ethernet，兼容现有以太网）
- GPUDirect RDMA = GPUDirect P2P 的网络版：远端 GPU → 本地 NIC → 本地 GPU 显存（双方 CPU 均不参与）

## SLI 的历史定位

SLI 的致命缺陷不是技术本身，而是**根本假设变了**。SLI 假设"用多 GPU 渲染同一个画面，负载拆分后合并"，这在单帧渲染时代有效。但现代 GPU 的工作负载——训练、光线追踪、多视角渲染——天然不共享同一帧的内存空间。NVLink 在带宽上解决了 SLI 的瓶颈，但 ADA 架构放弃 NVLink 说明 NVIDIA 认为：GPU 间共享内存不再是最优解。

取而代之的是：
- AI 训练：每张 GPU 独立计算，通过 NVLink/NVSwitch 同步梯度（数据并行），而非共享显存
- UE 渲染：Multi-Process Rendering——每个 GPU 独立进程，只传输最终纹理（不共享内存）

## 来源

- 原文：[[Clippings/聊透 GPU 通信技术——GPU Direct、NVLink、RDMA.md]]
- 原文：[[Clippings/SLI.md]]
