---
title: "Codex-maxxing：Jason Liu 的持久化工作线程方法论——让工作在离开后继续推进"
created: 2026-05-19
updated: 2026-05-19
type: query
tags: [clipping, codex, agent, workflow, memory, durable-threads, heartbeats, computer-use]
sources: [Clippings/Codex-maxxing - Jason Liu.md]
source_url: https://jxnl.github.io/blog/writing/2026/05/10/codex-maxxing/
confidence: high
rating: 7
---

# Codex-maxxing：Jason Liu 的持久化工作线程方法论

## 核心观点

Jason Liu 对 Codex 的使用已经超越了"写代码的工具"——他把 Codex 变成了**"工作居住的地方"**。核心转变来自一套操作循环：持久线程 + 共享内存 + 操作电脑的工具 + 操纵任务方向的能力 + 审查成果的界面。这套循环让工作在你离开后继续推进，而不是每次回到电脑前都从零开始。

**"Not that an agent can write code for me, but that more of my work can keep moving after I leave."**

## 关键要点

### 1. Durable Threads：每个工作流一个置顶长线程

不再是短对话，而是**数月中持续 compact 的 megathread**。每个重要工作流一个：

- Chief of Staff 线程
- Agents SDK 线程
- OpenAI CLI 线程
- Codex for OSS 线程
- Twitter 监控线程

**关键取舍**：长线程回访时可能不在缓存中，成本比新开短线程高。但对重要工作流，连续性值得这个代价。

快捷键：`Cmd-1` 到 `Cmd-9` 直接跳到置顶线程。

### 2. Voice Input：让 Agent 拿到未编辑的思考

语音的价值不在速度，而在**Agent 能拿到你未经编辑的原始思考**。

> "我记得 Slack 上有个叫 Ben 的人提到过这个，但我记不清具体内容了，你去查一下。" —— 这句话打字太模糊也太麻烦，说出来却非常自然。

同样的原理适用于文字记录：打电话录音、面对面聊天用 Granola 转录 → 作为写作原料。模型接触到思维的 messy version，往往比 polished version 产出更好的计划。

### 3. Steering：Agent 工作时持续注入意图

无需等待每一步完成才决定下一步。Agent 在运行时不断追加指令：

```
make this smaller
this copy is wrong
the spacing between these two things feels off
once this is done, open a PR
wait for the preview deploy
send the preview link to the person on Slack
```

你不需要盯着屏幕。走开时，队列已经成型。之后 Heartbeats 继续监控 PR 或 Slack 线程。

### 4. Memory as Files：Obsidian Vault 作为 Agent 的家

```
vault/
├── TODO.md
├── people/
├── projects/
├── agent/
└── notes/
```

**关键设计原则：**
- Vault 独立于任何项目仓库，是 Agent 的"家"
- 仓库放代码，Vault 放滚动上下文：人员、决策、开放循环、项目状态
- Vault 作为 GitHub 仓库托管 → **diff 变成记忆的审查界面**
- 当 Agent 更新 Vault 时，读 diff 就能看到它认为什么值得记住——这个审查步骤至关重要
- **文件迫使 Agent 将经验压缩成可以存活超过线程的形式**

Codex 也有第一方记忆功能（`Settings > Personalization > Memories`），Jason 视其为本地回忆层，但不替代显式的 Vault。Chronicle 功能可以利用屏幕上下文构建记忆，但他尚未深度使用。

**这是 Steph Ango 的 File over App 哲学在 Agent 时代的工程实现。**

### 5. Computer & Browser Use：三级访问模型

| 工具 | 用途 | 典型场景 |
|------|------|---------|
| `$browser` | 本地 Web 界面检查和注释 | 迭代本地 app、查看 `index.html` |
| `@chrome` | 已登录浏览器多标签页 | 多条认证会话并行，不占用主浏览器 |
| `@computer` | GUI 独有操作 | 点击桌面应用、上传文件 |

**三级选择的决策逻辑**：
- 本地 app 迭代 → `$browser`
- 需已登录浏览器会话 → `@chrome`
- 只能通过桌面应用点击完成 → `@computer`

Connectors（`$slack`、`$gmail`、`$calendar`）把这些延伸到工作的其他部分。

### 6. Heartbeats：线程本地自动化——让线程自我调度

不是全局 cron，是**线程级自动化**。线程可以自行调度、多计划并行、达到条件后停止、随时间调整频率。

**Chief of Staff（每 30 分钟）：**
```
Every 30 minutes, check Slack and Gmail for unanswered messages.
Help me prioritize what matters most.
If someone asks me a question, research the answer and draft a reply,
but do not send it.
```
回到 Slack 时，回复已经在草稿箱里。收集上下文的昂贵部分已完成。

**跨越工具边界的反馈循环（动画项目）：**
```
每 15 分钟检查 Slack 帖子 → 收到评论 → Remotion 重新渲染 → @computer 点上传按钮 → 回复帖子标记审阅者
```
这是 Heartbeats + Connectors + Computer Use 合在一起的威力——不再感觉是独立功能，而是一个持续运行的反馈循环。

**Get a refund（等客服时）：**
```
Every 5 minutes, check if customer support has joined.
If they have, get me a refund.
Once they reply, switch to checking every minute.
```
洗完澡出来，退款已完成。

### 7. Goals：野心需要验证

强 Goal ≠ 执行 Markdown 计划。强 Goal = **真正可验证的成功标准**。

Jason 的例子：将 Python Rich 库迁移到 Rust，但必须通过原库的所有单元测试。"测试套件给这次运行提供了一个真正的 oracle：Rust 移植版直到通过与原 Python 库相同测试才算完成。"

**"Ambition without verification is just a wish."**

### 8. Side Panel：工作发生的地方

Side panel 让 Codex 不再只是聊天应用。三个功能：
- **检查成果**：Markdown（可注释）、电子表格（公式+单元格编辑）、CSV（表格渲染）、PDF（直接渲染）、幻灯片
- **操作 Web 界面**：`index.html`、Storybook、Remotion Studio、Slidev、Streamlit
- **审查变更**：查看和评论 Agent 正在操作的同一对象

**"不是 Codex 能生成产物——而是我可以在不打破循环的情况下检查和注释它们。"**

最简版本往往最好：一个 `index.html` + JS + CSS，无需服务器。Jason 甚至用 Heartbeats 随时间更新同一个 `index.html`，每次回到线程都有新鲜产物等着。

### 9. 架构总览

```
                        ┌──────────────────┐
                        │   Obsidian Vault  │  ← 持久化记忆（文件系统）
                        │  (GitHub repo)    │     diff = 审查界面
                        └────────┬─────────┘
                                 │ 读写
    ┌────────────────────────────┼────────────────────────────┐
    │                    Codex Thread                          │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
    │  │ Heartbeats│  │ Voice   │  │ Steering │  │ Side    │ │
    │  │ (自我调度)│  │ (原始输入)│  │ (持续注入)│  │ Panel   │ │
    │  └──────────┘  └──────────┘  └──────────┘  │ (审查)  │ │
    │                                            └─────────┘ │
    │  ┌──────────────────────────────────────────────────┐   │
    │  │ Tools: $browser | @chrome | @computer            │   │
    │  │ Connectors: $slack | $gmail | $calendar          │   │
    │  └──────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
                 Slack       Browser      Desktop
                 Gmail       Storybook    Apps
                 Calendar    Remotion
```

## 与已有知识的关联

- [[20260518-obsidian-ceo-stephango-note-system]] — Steph Ango 的 File over App + Vault 哲学，Jason 的 Obsidian Vault 作为 Agent 记忆库是其实践版
- [[20260519-codex-goals-guide]] — Goals 六要素与 Jason 的 "Ambition without verification is just a wish" 完全一致
- [[20260519-multi-agent-collaboration-survey]] — Heartbeats 是队列触发（timer 型）的精妙实现；durable thread 与 durable board 同构
- [[20260519-karpathy-claude-md-viral]] — MEMORY.md + ERRORS.md 与 Jason 的 Vault 记忆系统目标相同但实现路径不同（文件 vs thread state）
- [[20260518-claude-code-large-codebases-best-practices]] — Claude Code 的 Harness 五层与 Codex 的 Thread+Memory+Tools+Heartbeats 体系对比

## 行动建议

- **建立你的持久线程**：每个重要工作流一个置顶线程，compact 而非新开
- **用语音输入思考，而非打字**：让 Agent 拿到未编辑版本
- **创建 Agent Vault**：独立于项目仓库的文件夹，Agent 在其中读写决策、人员、状态。提交到 Git，diff 审查 Agent 认为值得记住的事
- **给长任务配 Heartbeat**：不必盯着屏幕，让线程自我调度
- **用 Side Panel 产物而非纯文本作为交付物**：`index.html` 比 Markdown 更适合 Agent 产出

## 来源

- [[Clippings/Codex-maxxing - Jason Liu.md]]
- https://jxnl.github.io/blog/writing/2026/05/10/codex-maxxing/
