---
title: "Claude Code 在大代码库中的工作方式：企业级部署最佳实践"
created: 2026-05-18
updated: 2026-05-18
type: query
tags: [article, clipping, agents, architecture, methodology]
sources: ["Clippings/How Claude Code works in large codebases Best practices and where to start.md"]
source_url: https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
confidence: high
rating: 7
---

# Claude Code 在大代码库中的工作方式

## 核心观点

Anthropic Applied AI 团队基于数百家企业的 Claude Code 部署经验，总结出三个反直觉发现：
1. **Harness（扩展体系）比模型本身更能决定效果**——CLAUDE.md + Hooks + Skills + Plugins + MCP 五层扩展的搭建顺序和投入决定了 Claude Code 的上限
2. **Agentic Search（像工程师一样 grep/读文件/追引用）击败了 RAG 方案**——嵌入式索引在大代码库中永远是过时的，agentic 方式工作在实时代码上
3. **CLAUDE.md 需要随模型升级主动修剪**——为旧模型写的补偿性规则在新模型下会变成束缚。每 3-6 个月必须审查一次

## 关键要点

### 1. Agentic Search vs RAG：两种根本不同的代码库导航

| 方式 | RAG（嵌入式索引） | Agentic Search（Claude Code） |
|------|------------------|------------------------------|
| 原理 | 对整个代码库做 embedding，查询时检索相关 chunk | 遍历文件系统、grep、读文件、追引用 |
| 索引维护 | 需要持续重建（跟不上活跃团队） | **不需要** |
| 数据新鲜度 | 几小时到几周前的快照 | **实时** |
| 失败模式 | 返回已重命名的函数、已删除的模块，无提示 | 需要足够起始上下文来知道往哪找 |
| 对大型 monorepo | 索引管道跟不上数千工程师的提交 | 每个开发者实例工作在实时代码上 |

**关键 insight**：如果一个函数两周前被改名，RAG 可能返回旧名且无提示。Agentic search 每次都是读当前文件系统。Clipping 原文明确强调 Claude Code 不需要构建、维护或上传代码库索引，而是工作在开发者本机的 live codebase 上。

**但 Agentic Search 也有代价**：如果起始上下文不足，Claude 不知道往哪里找。这就是为什么 CLAUDE.md 的层次化配置至关重要。

### 2. The Harness：五层扩展体系（按搭建顺序）

```
CLAUDE.md  ──>  Hooks  ──>  Skills  ──>  Plugins  ──>  MCP Servers
  基础上下文      自改进      按需加载      打包分发      外部连接
                                  │
                          LSP 集成 + Subagents
                          符号级精度   上下文隔离
```

**CLAUDE.md（第一优先）**
- 根目录文件 = 大局观（指针 + 关键陷阱），子目录文件 = 本地约定
- 每个 session 自动加载 → 只放适用范围广的内容
- 错误做法：把所有东西塞进根 CLAUDE.md，变成性能拖累

**Hooks（让配置自改进）**
- Stop hook 的真正价值不是阻止错误，而是 **session 结束后自动提议 CLAUDE.md 更新**
- Start hook 动态加载团队专属上下文
- 格式化/lint 用 hook 强制比让 Claude 记住指令更可靠

**Skills（渐进式披露）**
- 大代码库有几十种任务类型，不需要所有 expertise 在每个 session 里
- Skill 按需加载，可以 **绑定到特定路径**（如 payments 团队的部署 skill 只在 payments/ 目录激活）
- 这是"context budget"管理的关键手段

**Plugins（打破部落知识）**
- 好的配置往往停留在老员工的本地。Plugin 把 skills + hooks + MCP 打包成可安装包
- 新工程师装一个 plugin = 立刻拥有和老员工相同的 context 和能力
- 通过 managed marketplace 跨组织分发

**MCP Servers（扩展边界）**
- 高级团队构建暴露结构化搜索的 MCP server，让 Claude 直接调用
- 也可以连接到内部文档、ticket 系统、分析平台

**LSP 集成（符号级精度）**
- Grep 搜一个常见函数名 → 几千个匹配 → Claude 烧 context 打开文件判断哪个对
- LSP 只返回指向**同一个符号**的引用 → 过滤在 Claude 读任何东西之前完成
- **对多语言代码库，这是 ROI 最高的单项投资**

**Subagents（分离探索与编辑）**
- 独立 Claude 实例 + 独立上下文窗口
- 读-only subagent：映射子系统 → 写发现到文件 → 主 agent 带着全貌做编辑

这套结构可以理解为：

```text
CLAUDE.md ──> Hooks ──> Skills ──> Plugins ──> MCP Servers
    │           │          │           │             │
    ▼           ▼          ▼           ▼             ▼
 broad       events    on-demand   distribution   tools/data
 context   automation  expertise      layer       integration

            + LSP integrations + Subagents
```

### 3. 三种成功的配置模式

**模式一：让代码库可导航**
- CLAUDE.md 保持精简、层次化：根文件只有指针和关键陷阱
- **在子目录初始化 session，而非 repo 根目录**——Claude 会自动向上遍历加载所有 CLAUDE.md
- 每个子目录的 CLAUDE.md 指定**该目录专用的 test/lint 命令**（避免全量跑导致超时）
- `.claude/settings.json` 中提交 `permissions.deny` 规则排除生成文件、构建产物、第三方代码
- 目录结构不给力时：写一个轻量 `CODEBASE_MAP.md`，顶层文件夹一行描述，Claude 当目录扫描

**模式二：随模型升级主动维护 CLAUDE.md**
- 反例：一个 CLAUDE.md 规则要求"所有重构拆成单文件变更"——帮早期模型避免跑偏，但阻止新模型做跨文件协同编辑
- Hook/skill 给旧模型弱点打的补丁，在新模型中是纯开销
- **审查节奏：每 3-6 个月 + 每次大模型发布后**

**模式三：分配所有权**
- 最成功的部署在**大规模开放之前就完成了基础设施投资**——一个小团队（甚至一个人）先接好所有工具
- 新兴角色：**Agent Manager**（混合 PM/工程的职能，管理 Claude Code 生态）
- 最小可行版：一个 **DRI**（直接负责人）拥有 CLAME.md 约定、权限策略、plugin marketplace 的决策权
- 自下而上采用产生热情，但没有人集中化会碎片化——你需要一个人来"收集+布道"

### 4. 各组件速查表

| 组件 | 做什么 | 何时加载 | 常见错误 |
|------|--------|---------|---------|
| CLAUDE.md | 代码库上下文 | 每个 session 自动 | 太长、过时、放业务逻辑规则 |
| Hooks | 自动化检查 + 自改进 | 事件触发（pre/post tool） | 只用来阻止错误，不用来改进配置 |
| Skills | 专业工作流 | 按需（触发词或路径匹配） | 触发词太泛，每个 session 都加载 |
| Plugins | 打包分发 | 安装后可用 | 只打包 skills 不打包 hooks+MCP |
| MCP | 连接外部系统 | 配置后持久连接 | 工具设计太宽泛，返回太多数据 |
| LSP | 符号级导航 | 后台运行 | 没为每种语言安装正确的 server |
| Subagents | 上下文隔离 | 显式调用 | 给子 agent 的任务太模糊 |

### 5. 组织层面的建议

- **先建 infra，再推采用**——开发者的第一次体验必须是 productive 的
- **成立跨职能工作组**（工程 + 信息安全 + 治理），在 rollout 前一起定义需求和路线图
- **从有限范围开始**：批准的 skills 集合 + 强制 code review + 受限访问，随信心增长扩展
- 受监管行业的治理问题要提前回答：谁控制 skills/plugins 可用性？如何防止几千工程师重复造轮子？AI 生成的代码走同样的 review 流程吗？

## 与已有知识的关联

- **Harness > Model** 的论点与 Boris Cherny 的 "Opus 4.7 在老工作流中是 nice improvement，在优化后的工作流中是 significant leap" 完全一致 — 模型升级的边际收益取决于 harness 的成熟度
- **Skills as progressive disclosure** = `deep-research` skill 的 Phase 2 设计原则（用户 wiki → 项目 agent-state → agent workspaces，三层逐级收窄）
- **CLAUDE.md 分层** ≈ 你的 `~/.claude/CLAUDE.md`（全局）+ wiki 项目 `CLAUDE.md` symlink（项目级）
- **Agent Manager / DRI** 角色 = 你（作为个人开发者）本质上就是这个角色——你在维护 wiki 的 SCHEMA.md、skills、CLAUDE.md

## 行动建议

- **审查你的 CLAUDE.md**：里面有没有为旧模型写的补偿性规则？每 3 个月检查一次
- **利用 skills 的路径绑定**：如果你的 skills 中有只适用于 wiki 项目的，考虑绑定到 wiki 路径
- **个人版"agent manager"**：你已经有 SCHEMA.md、conversations/、log.md、CLAUDE.md——考虑写一个 stop hook 让 Claude 在 session 结束后自动提议 CLAUDE.md 更新
- **LSP 集成**：如果你在大型 C++/Python 项目中用 Claude Code，安装对应的 code intelligence plugin
- **CarlaUE5 优先级**：先做 `.claudeignore` / `permissions.deny` 排噪、根 `CLAUDE.md` 精简化、`CODEBASE_MAP.md` 顶层目录索引，再考虑更复杂的 MCP 或 subagent 工作流

## 相关笔记
- [[claude-code-practical-tips-note]] — Claude Code 实用技巧——官方核心开发者现场演示
- [[20260515-boris-cherny-opus-4-7-tips]] — Boris Cherny Opus 4.7 实操六条：从 Auto Mode 到自验证循环
- [[20260513-complete-guide-building-claude-skills]] — Anthropic 官方 Claude Skills 构建完整指南：从设计到分发
- [[20260512-perplexity-agent-skills-design]] — Perplexity Agent Skills 设计与维护方法论
- [[20260514-barrystop-agent-three-iron-rules]] — Barry Zhang (Anthropic) AI Engineer Summit：如何构建高效 Agent 的三条铁律

## 来源

- 原文：https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
- 剪藏：[[../Clippings/How Claude Code works in large codebases Best practices and where to start.md]]
