---
title: Anthropic Prompting 101 结构化笔记
created: 2026-04-28
updated: 2026-04-28
type: query
tags: [video, transcript, methodology, multi-modal, agent]
sources: [raw/transcripts/x-2048592344552010061_transcript.md, raw/assets/video/x-2048592344552010061.mp4]
confidence: medium
---

# Anthropic Prompting 101 结构化笔记

## 核心观点

Prompt engineering 不是一次性写出“聪明提示词”，而是围绕具体任务做经验性迭代：明确任务、补足上下文、组织输入、给出示例、约束推理顺序、限定输出格式，并用失败案例持续修正。视频用一个瑞典车险理赔的 multi-modal prompting 场景说明：当输入包含表格、手绘草图和外语材料时，Claude 的表现高度依赖 prompt 是否提供足够的任务背景、领域知识和分析步骤。

更实用的结论是：业务级 prompt engineering 应把 prompt 当作可测试、可演化的系统接口，而不是聊天文本。好的 prompt 需要服务后续解析、数据库入库、人类复核和自动化流程。

## 关键要点

1. **先定义任务场景，再给模型材料**  
   初始 prompt 只说“分析事故表单和判断责任”，Claude 会把车祸误解成滑雪事故。加入“这是瑞典车险理赔、目标是帮助 claims adjuster 判断事故责任”等背景后，模型才进入正确的问题空间。

2. **固定背景知识适合放进 system prompt**  
   表单结构、17 个 checkbox 的含义、车辆 A/B 的列结构、人工填写可能有圈画或涂写等信息不会随每次请求变化，适合放入 system prompt，也适合做 prompt caching。

3. **结构化输入能降低歧义**  
   视频推荐用 XML tags、Markdown 等 delimiter 组织材料，让 Claude 知道每段信息的角色。例如把用户偏好、表单说明、图片内容、任务指令分别包起来，方便模型在后文引用。

4. **Few-shot examples 用来覆盖灰区案例**  
   对容易误判、边界模糊或业务专家已有标注的案例，可以把输入样例和正确分析过程写入 prompt。示例不是装饰，而是把人类标签数据转成模型可复用的判断依据。

5. **分析顺序会影响多模态判断质量**  
   对事故表单和草图这类输入，应该先读结构化表单，再看手绘草图。视频强调不要让模型直接从模糊草图猜测，而是先建立事实基础，再用草图做交叉验证。

6. **最终提醒用于降低幻觉和过度断言**  
   prompt 末尾应重复关键约束：只在有信心时判断，不要编造未看到的 checkbox，不要从模糊草图硬推结论，并要求每个事实性判断能回指到表单或草图证据。

7. **输出格式是产品接口的一部分**  
   对真实应用来说，冗长解释未必可用。视频示例把最终判断包在 XML tag 中，便于程序只提取 verdict；也提到 prefilled response 可用于引导 JSON 或 XML 输出。

8. **Extended thinking 可作为 prompt 调试工具**  
   对 Claude 3.7 和 Claude 4 这类 hybrid reasoning model，可以利用 extended thinking 观察模型如何处理数据，再把稳定有效的步骤固化进 system prompt。

## 行动建议

1. 给复杂任务写 prompt 时，先列出“任务背景、输入材料、领域背景、步骤、输出格式、禁止事项”，不要直接从一句自然语言需求开始。
2. 对固定不变的业务知识，放入 system prompt；对每次变化的材料，放入 user prompt；对长且稳定的系统背景，优先考虑 prompt caching。
3. 多模态任务要显式指定分析顺序，例如“先读表单，再看图片，再综合判断”，避免模型从视觉材料中过早猜测。
4. 为高风险判断加入证据要求：每个结论必须说明依据来自哪个字段、图片区域、checkbox 或文本片段。
5. 把输出格式设计成可解析接口，例如 XML tag 或 JSON schema；不要让下游系统依赖自然语言段落截取。
6. 建立 prompt regression set：收集误判、边界案例和专家标注，用作 few-shot examples 或测试集。
7. 对 ASR 生成的英文转录稿，引用时应做人工校对；本次 FunASR 可读性较好，但仍有 `Claude`/`cloud`、`prompt`/`problem` 等错听。

## 可复用 Prompt 结构

```text
┌──────────────────────┐
│ Task context          │
├──────────────────────┤
│ Tone and constraints  │
├──────────────────────┤
│ Stable background     │
├──────────────────────┤
│ Dynamic content       │
├──────────────────────┤
│ Examples              │
├──────────────────────┤
│ Ordered instructions  │
├──────────────────────┤
│ Final reminder        │
├──────────────────────┤
│ Output format         │
└──────────────────────┘
```

## 来源路径

- 视频：[[raw/assets/video/x-2048592344552010061.mp4]]
- 音频：[[raw/assets/audio/x-2048592344552010061.wav]]
- 转录稿：[[raw/transcripts/x-2048592344552010061_transcript.md]]
- FunASR 输出：`raw/transcripts/x-2048592344552010061.funasr.json`
- ASR 后端：FunASR `iic/SenseVoiceSmall`
- 时间戳模式：`approximate`
