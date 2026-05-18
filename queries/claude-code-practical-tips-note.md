---
title: Claude Code 实用技巧——官方核心开发者现场演示
created: 2026-04-28
updated: 2026-04-28
type: query
tags: [agent, tool-use, product, platform, video]
sources: [raw/transcripts/2047876749925683200_transcript.md]
confidence: high
---

# Claude Code 实用技巧——官方核心开发者现场演示

> 来源：Anthropic Claude Code 核心开发者 Boris 在 2026 年 4 月的工作坊演讲。全程 28 分钟，面向已安装或刚接触 Claude Code 的工程师，纯实操导向。

## 核心观点

- **Claude Code 是"全 agent"编程工具，不是代码补全工具。** 它面向构建功能、编写整个文件、修复整个 bug，而非逐行补全。它通过少数几个工具（编辑文件、运行 bash 命令、搜索文件）串联工作，自行决定调用顺序。
- **上手第一件事永远是 Codebase Q&A，不是写代码。** Anthropic 内部入职培训过去要 2-3 周，现在 2-3 天，核心就是用 Claude Code 向代码库提问。这教会新人如何 prompt，也建立对 Claude Code 能力边界的直觉。
- **先规划再编码是得到好结果的最简单方法。** 不需要 plan mode 或特殊工具，只需说"before you write code, make a plan, ask for approval"。这避免一次生成 3000 行却完全不是你想要的。
- **给 Claude Code 一个"检查自己工作"的方式，让它自动迭代，效果提升显著。** 无论是 unit tests、integration tests、Puppeteer 截图还是 iOS simulator 截图，只要有反馈闭环，迭代两三次后结果接近完美。
- **`CLAUDE.md` 是投入产出比最高的配置。** 把常用命令、架构决策、核心文件、编码风格写进去，全队共享。越短越好——太长只会浪费 context。

## 关键要点

### 1. 初始设置
- `terminal setup`：启用 Shift+Enter 换行
- `/theme`：设置浅色/深色/色盲主题
- `/install-github-app`：在 GitHub issue/PR 中 @claude
- 自定义 allowed tools：减少频繁的权限确认弹窗
- macOS 用户可用系统听写（双击 dictation 键），直接语音输入 prompt

### 2. Codebase Q&A（入门首选）
- "这个类/函数是怎么被实例化/使用的？"——Claude Code 不止做文本搜索，会找实际用法示例，给出 Wiki 级别深度
- "为什么这个函数有 15 个参数，命名这么奇怪？"——自动查 git history、commits、关联 issue，汇总解释
- 用 web fetch 拉 GitHub issues，获取问题上下文
- 每周一 standup："what did I ship this week?"——自动读 git log，列出本周交付
- **无需索引、无需上传代码、无远程数据库、不训练模型**

### 3. 代码编辑

| 场景 | 推荐做法 |
|---|---|
| 复杂功能 | 先 brainstorm → make a plan → 等确认再写 |
| 提交代码 | "commit, push, make a PR"——自动读 history 匹配 commit 格式 |
| web UI | 给 mock + Puppeteer 截图，让它迭代 2-3 次 |
| 写单元测试 | 开 shift+tab auto-accept 模式，减少确认 |

### 4. 自定义工具
- **Bash 工具**：告诉 Claude 关于你团队的 CLI，它可以通过 `--help` 自己学会用法
- **MCP 工具**：添加 MCP server 后 Claude 自动使用；可 check-in `.mcp.json` 到代码库，团队成员启动 Claude Code 时提示安装
- Anthropic 内部示例：app repo 中有共享的 Puppeteer MCP server，所有工程师无需各自安装就能用

### 5. CLAUDE.md 上下文层次

```
企业策略（Enterprise policies）
  ├── 全局配置（~/.claude/）
  │   └── 用户级 CLAUDE.md + 自定义 slash commands
  └── 项目配置（git repo 内）
      ├── CLAUDE.md（项目根，check-in 共享）
      ├── CLAUDE.local.md（不 check-in，个人用）
      └── 子目录 CLAUDE.md（按需自动加载）
```

- 企业策略可统一管理权限：允许/阻止特定命令、禁止 fetch 特定 URL
- `/memory` 查看当前所有 memory 文件；`#` 记住某件事并选择存到哪个 memory

### 6. 快捷键（容易遗漏）
- `Shift+Tab`：切换 auto-accept edits 模式（bash 命令仍需确认）
- `#`：记住某事，自动写入 CLAUDE.md
- `!`：直接执行 bash 命令，命令和输出都会进入 context
- `Esc`：随时安全中断 Claude（不会破坏 session）
- `Esc` 两次：跳回历史对话
- `Ctrl+R`：查看 Claude 看到的完整输出
- `claude --resume` / `--continue`：恢复上次 session

### 7. Claude Code SDK（`-p` 模式）
- 即 CLI SDK：`claude -p "prompt"` → JSON 输出
- 支持指定 allowed tools、输出格式（JSON / streaming JSON）
- 可以 pipe 进 pipe 出：`git status | claude -p "..." | jq`
- 用法场景：CI 管道、incident response、日志分析、从 Sentry CLI 拉数据

### 8. Power User 并行工作流
- 多个 terminal tab 跑不同 repo 的 Claude Code
- 同一 repo 多个 checkout，各自跑独立的 Claude Code 实例
- `git worktree` 隔离并行任务
- tmux / SSH tunnels 管理远程 session

## 行动建议

1. **立即检查 `CLAUDE.md`。** 确保项目根有好用的 CLAUDE.md。放常用命令、架构决策、编码风格、核心文件路径。保持简洁。
2. **配置 #memory。** 当 Claude Code 某个行为不符合预期，直接 `#` 记住纠正规则，不再重复犯错。
3. **培养"先规划"的 Prompt 习惯。** 复杂任务务必加一句 "make a plan first, ask for confirmation before writing code"。
4. **找到你的迭代反馈闭环。** 前端给 Puppeteer 截图，后端给 unit/integration tests，让 Claude 能看见结果自我修正。
5. **团队级配置 MCP。** 把团队共用的 MCP server check-in 到 `.mcp.json`，一次配置全队受益。
6. **善用 `!` 和 pipe。** 长命令直接 `!` 执行进入 context；管道组合 `claude -p` 用做超级 Unix 工具。

## 相关笔记
- [[20260515-boris-cherny-opus-4-7-tips]] — Boris Cherny Opus 4.7 实操六条：从 Auto Mode 到自验证循环
- [[20260518-claude-code-large-codebases-best-practices]] — Claude Code 在大代码库中的工作方式：企业级部署最佳实践
- [[20260514-barrystop-agent-three-iron-rules]] — Barry Zhang (Anthropic) AI Engineer Summit：如何构建高效 Agent 的三条铁律
- [[20260514-openclaw-pi-coding-agent-framework]] — OpenClaw 背后框架 Pi：好的 Coding Agent 应该让用户决定需要什么
- [[20260513-complete-guide-building-claude-skills]] — Anthropic 官方 Claude Skills 构建完整指南：从设计到分发

## 来源

- 原始链接：https://x.com/i/status/2047877250184618248
- 视频：[[raw/assets/video/2047876749925683200/2047876749925683200.mp4]]
- 音频：[[raw/assets/audio/2047876749925683200.wav]]
- 转录稿：[[raw/transcripts/2047876749925683200_transcript.md]]
- FunASR JSON：`raw/transcripts/2047876749925683200.funasr.json`
