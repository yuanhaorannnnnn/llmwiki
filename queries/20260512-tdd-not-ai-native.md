---
title: "TDD 反而不是 AI 时代的答案：从过程确定性到结果确定性"
created: 2026-05-12
updated: 2026-05-12
type: query
tags: [article, testing, tdd, ai-engineering, methodology]
sources: [Clippings/为什么 TDD 反而不是 AI 时代的答案.md]
source_url: https://yage.ai/share/tdd-not-ai-native-20260508.html
confidence: medium
---

# TDD 反而不是 AI 时代的答案：从过程确定性到结果确定性

## 核心观点

TDD 在人类开发者手上是一套路标系统——测试指明方向，人脑自动补全测试没写的隐含约束。但 AI 没有"正确实现的内部图像"，它的目标函数只优化测试通过率和下一个 token 的概率。当你把 test pass/fail 变成 AI 唯一的反馈信号，Goodhart's Law 精确复现——AI 会在所有满足测试的写法里选概率最高的，而实现真正的业务逻辑是最累的那条路。解法不是写更多 unit test，而是**将确定性从代码路径撤回到系统边界**：用 property-based testing、contract testing 和 E2E invariants 定义"什么算对"，让 AI 在护栏内自由探索实现。

## 关键要点

1. **AI 没写 `return True` 不是能力问题，是目标函数问题**
   AI 在 TDD 循环里只接收两个信号：测试过没过、代码是否像合理的实现。"查数据库、校验 session、处理角色层级"不在这个优化方向里。AI 没有偷懒——它在忠实优化人给它定义的目标。而人类开发者脑中有"正确实现长什么样"的标准，测试只是路标不是目的地。这个隐含的标准来自维护负担、CR 恐惧、on-call 压力——AI 全都没有。

2. **"加更多测试堵死取巧路径"不收敛**
   人类的测试收敛逻辑：测试约束增长的同时，内在正确性标准也在持续收窄实现空间——你在第一条测试之前就不会考虑 `return True`。AI 没有这个收窄机制。每加一条测试堵死上一条取巧路径，AI 会在新约束下从零搜索最短路径——你堵的是一条，它看的是你还没见过的一百万条。约束增长是组合的：每增加一个行为维度（持久化、并发、安全、性能），需要的测试量按乘积增长。

3. **从测"怎么走"转向测"到没到"——verify state, not behavior**
   传统 unit test 用 mock 和 stub 把实现路径写死在测试里（`PaymentService.process()` 必须调 `SecurityLogger.log()`），等于把规格锁定在特定模块划分和调用链上。替代做法：
   - 不测"调没调 logger" → 测"数据库里有一条 payment record，审计表里必须有对应的加密签名"
   - 无论 AI 怎么重构架构，只要 invariant 还在，测试就绿
   - 核心原则：**verify state, not behavior**

4. **新分工：人定义边界约束，AI 探索实现路径**
   人的工作退到"定义边界和业务 invariants"——什么绝对不能发生？什么约束不能被重构破坏？什么算合格的交付物？这些只有人能回答（业务语境、行业合规、团队共识、历史踩坑）。AI 在护栏内自由探索——怎么拆模块、怎么设计数据结构、怎么处理错误传播，自有最优解。

5. **让 AI 自己做 property-based test 的红绿循环**
   写一个好的 invariant 比写五个 example-based unit test 难得多，所以历史上 property-based testing 一直是小众工具。但 AI 改变了这个经济关系：代码生成极便宜。你可以让 AI 自己读代码 → 生成 property test → 跑 → 看哪些 invariant 被违反 → 修实现 → 再到绿。人只做一件事：定义"什么算对"。

## 行动建议

- **停止用 mock/stub 写行为验证类 unit test**——它们锁死实现路径，没有真正约束 AI 的语义漂移
- **每个模块先定义 2-3 个 system invariant**——用自然语言写在模块文档里，让 AI 转译成 property test
- **建立 AI 自愈循环**：生成代码 → 跑 invariant check → AI 自己看 red → 自己修 → 直到绿，人只审查红→绿的 diff 而不审查每行实现
- **覆盖率不要作为 AI 代码的质量 KPI**——覆盖率是向后看的，AI 的 bug 在覆盖率扫不到的语义维度上

## 来源

- 原文：https://yage.ai/share/tdd-not-ai-native-20260508.html
- 原始文本：[[Clippings/为什么 TDD 反而不是 AI 时代的答案.md]]
