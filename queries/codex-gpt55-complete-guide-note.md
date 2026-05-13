---
title: Codex + GPT-5.5 完整教程结构化笔记
created: 2026-04-28
updated: 2026-04-28
type: query
tags: [video, transcript, product, platform, agent, tool-use, methodology]
sources: [raw/transcripts/2048628829753835521_transcript.md, raw/assets/video/2048628829753835521/2048628829753835521.mp4]
confidence: medium
---

# Codex + GPT-5.5 完整教程结构化笔记

## 核心观点

视频把 OpenAI Codex 描述为一个“统一的 AI agent 工作台”：它不是单纯的聊天窗口，而是把项目目录、文件读写、浏览器/计算机使用、插件、skills、自动化和多任务 agent 编排放在同一个界面里。讲者的核心判断是，未来高效使用 agent 和 tool-use 的关键不是一次只等一个任务完成，而是把工作拆成多个可并行推进的 agent 会话，每个会话围绕一个明确产物运行。

教程前半部分建立基础用法：项目目录、权限、模型 effort、文件预览、skills/plugins、automations。后半部分用一个名为 Chorus 的 AI agent 学习类 app 作为实战案例，同时推进 iOS app、landing page、investor deck、launch video 和 X post 自动化，展示 Codex 如何从“生成单个文件”扩展成“协调多个工作流产物”的操作系统。

需要注意：本笔记基于 FunASR 转录稿整理，时间戳为 approximate；视频中关于产品能力、模型版本和第三方工具状态的说法来自原视频内容，未做外部事实核验。

## 关键要点

1. **项目目录是 Codex 工作流的中心**  
   Codex 会在指定项目文件夹中创建、编辑和组织文件。讲者建议按项目建目录，并把同一主题下的聊天、产物、输出文件集中在同一项目中，这样后续可以在新会话中引用已有文件继续工作。

2. **权限、模型和 effort 决定 agent 的工作方式**  
   视频反复强调权限设置会影响 agent 是否需要用户逐步批准操作；模型和 effort 则影响复杂任务质量。讲者偏好高权限与高 effort，让 agent 能长时间自主推进。

3. **文件预览让非代码产物也进入 agent 工作流**  
   Codex 不只生成代码，也能创建和编辑 spreadsheets、documents、PowerPoint decks、web apps、videos 等文件。侧边预览和 full-screen preview 让用户可以直接检查产物，并用自然语言继续要求修改。

4. **skills 是可复用工作流，plugins 是外部能力入口**  
   视频把 skill 类比为 reusable recipe，把 plugin 视为可安装能力单元。讲者展示了 Google Calendar、Gmail、Figma、Remotion、Tally、Supabase、Tfully 等工具如何被接入或包装成 agent 可调用能力。

5. **重复性工作应转成 automation**  
   讲者演示了把“每周日历总结并发邮件”“每月 YouTube 视频表现分析”“每天生成 X 草稿”等任务转成定时 automation。关键模式是：先让 agent 跑通一次，再把成功流程固化为定时任务。

6. **不知道下一步怎么做时，直接让 agent 选型和拆解**  
   在数据库、认证、部署、TestFlight、API skill 创建等环节，讲者多次直接询问 Codex “应该用什么方案”“我还需要做什么”。这体现了 agent 工作流中的一个实用策略：把技术不确定性转成 agent 的研究与行动任务。

7. **多任务不是同时思考多个问题，而是连续发出清晰任务**  
   视频对 multitasking 的定义更接近 serial tasking：用户在一个会话中投入精力写清楚 prompt，提交后切换到另一个会话。最佳实践是让多个 agent 分别承担 design、app、deck、video、deployment、automation 等独立产物。

8. **复杂产物需要跨模型和跨工具协作**  
   讲者认为 Codex 的界面和通用 agent 体验强，但在设计任务上又引入 Claude Code 辅助 landing page、deck 和 motion graphics。实际工作中可以让 Codex 做 orchestration，让更擅长视觉设计的模型处理 design-heavy tasks。

9. **实战案例覆盖了一个产品发布闭环**  
   Chorus app 案例包含：先写 plan，再做 mobile design，创建 Swift app，接 Supabase 数据库和 authentication，做 waitlist landing page，生成 investor deck，制作 Remotion launch video，部署到 Vercel，提交 TestFlight，最后配置 X post automation。

10. **skill 创建的核心触发点是“我反复做这件事”**  
    讲者用 YouTube transcript API 和 Tfully API 举例：当某个流程需要反复执行，且外部服务有 API，就可以让 Codex 研究 API、生成 skill、测试调用，并在之后用 `$skill` 或 slash/mention 形式触发。

## 行动建议

1. 使用 Codex 做真实项目时，先创建清晰项目目录，并让每个产物落在该目录下，避免聊天和文件分散。
2. 把任务拆成“可单独验收的产物”：例如 plan、prototype、mobile app、web app、deck、video、automation，每个产物用独立会话推进。
3. 给 agent 的 prompt 要包含目标、上下文、产物格式、完成标准和当前限制；复杂任务先要求生成 plan，再要求执行。
4. 对重复流程先手动跑通一次，再让 Codex 总结步骤并封装成 skill 或 automation。
5. 当工作依赖第三方工具时，优先确认是否已有 plugin；没有 plugin 时，再考虑用 API key 创建自定义 skill。
6. 对设计类产物要安排人工审查和多轮修改；可以把截图、局部标注和具体坐标/时间点作为修改依据。
7. 长任务运行时采用并行会话：等待一个 agent 构建时，切换到另一个会话推进研究、素材、设计或部署。
8. 对高权限 agent 操作保持边界意识：只在明确项目目录中运行，敏感 API key、账号、发布操作需要单独复核。
9. 对视频里提到的产品能力、模型版本和插件能力，在实际采用前重新确认当前版本文档；这些信息高度时效性。

## 可复用工作流

```text
┌────────────────────┐
│  Project Folder    │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│  Plan / Checklist  │
└─────────┬──────────┘
          ▼
┌─────────────────────────────────────────────┐
│  Parallel Agent Chats                       │
├──────────┬──────────┬──────────┬───────────┤
│  App     │  Web     │  Deck    │  Video    │
└────┬─────┴────┬─────┴────┬─────┴─────┬─────┘
     ▼          ▼          ▼           ▼
┌────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐
│ Build  │ │ Deploy   │ │ Export │ │ Render   │
└────┬───┘ └────┬─────┘ └────┬───┘ └────┬─────┘
     └──────────┴────────────┴──────────┘
                    ▼
          ┌──────────────────┐
          │  Automation       │
          └──────────────────┘
```

## 来源路径

- 视频：[[raw/assets/video/2048628829753835521/2048628829753835521.mp4]]
- 缩略图：[[raw/assets/video/2048628829753835521/2048628829753835521.jpg]]
- 元数据：`raw/assets/video/2048628829753835521/2048628829753835521.info.json`
- 音频：[[raw/assets/audio/2048628829753835521.wav]]
- 转录稿：[[raw/transcripts/2048628829753835521_transcript.md]]
- FunASR 输出：`raw/transcripts/2048628829753835521.funasr.json`
- 原始链接：`https://x.com/i/status/2048698399961289011`
- ASR 后端：FunASR `iic/SenseVoiceSmall`
- 时间戳模式：`approximate`
