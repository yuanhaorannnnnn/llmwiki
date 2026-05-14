# Conversation Recap - wiki

## Conversation Summary
- 本会话围绕微信公众号文章自动化摄入：创建 `wechat-mp-to-markdown` 用于把公开 `mp.weixin.qq.com/s/...` 文章转换为 Markdown，并用“智能车参考”文章完成真实抓取验证。
- 进一步创建 `wechat-mp-url-discovery` 用 Tavily Search 发现公众号文章 URL；测试发现 Search API 适合主题检索，但不适合作为“某公众号最新文章”的唯一数据源。
- 修正了两个实现问题：WeChat HTML 中 `mp/getverifyinfo` 被误判为验证码页、URL discovery 把 `https://mp.weixin.qq.com/s/` 空 slug 当成文章 URL。

## Current Objective
- 完成微信公众号文章抽取与 URL discovery 两个 skill 的阶段性收尾，保存当前结论，并避免把无关 wiki 改动混入提交。

## Key Decisions
- 文章转换与 URL 发现拆成两个 skill：`wechat-mp-to-markdown` 负责文章到 Markdown，`wechat-mp-url-discovery` 负责生成 URL list。
- Tavily 作为候选 URL 搜索源；浏览器控制只适合合集页、已登录列表页或用户提供的具体列表页 fallback。
- “公众号最新文章”不能自动加入某篇文章标题词，例如 `Waymo`；最新模式应只按公众号名召回候选，再抓取文章元数据过滤 `account` 并按 `published` 排序。
- 仅凭 Tavily account-only query 对“智能车参考”召回不足，严格 `--latest` 测试返回 0 个可验证 URL；需要公众号合集、本机微信数据、具体列表页或 URL seed 才能稳定获取最新文章。

## Constraints
- 简体中文回复；技术名词、路径、命令保持 English。
- 不绕过微信登录、验证码、付费墙、关注可见或访问控制。
- 不把 Tavily API key 写入 skill 文件、报告、URL list、shell 脚本或 Markdown 输出；该 key 已在对话中出现，流程稳定后建议轮换。
- 当前创建的 skill 位于 `/home/yhr/.codex/skills/`，该目录不是 `/media/yhr/2T/files/wiki` git 仓库的一部分。

## Open Questions
- 若目标是稳定获取某公众号最新文章，需要确定首选数据源：公众号合集 URL、本机微信 `wechat-cli` 数据、浏览器控制具体列表页，或用户维护的 URL seed。

## Active Tasks

### wechat-mp-to-markdown
- [x] 创建 skill：`/home/yhr/.codex/skills/wechat-mp-to-markdown`
- [x] 实现 `scripts/wechat_article_to_markdown.py`
- [x] 修正 `verify` 误判验证码页的问题
- [x] 将微信 Unix 发布时间规范化为 `YYYY-MM-DD`
- [x] 用 `https://mp.weixin.qq.com/s/FTyaA5WX0bRYtquzU9DzTA` 真实验证并生成 Markdown

### wechat-mp-url-discovery
- [x] 创建 skill：`/home/yhr/.codex/skills/wechat-mp-url-discovery`
- [x] 实现 Tavily URL discovery 脚本
- [x] 修正空 slug `https://mp.weixin.qq.com/s/` 误收录问题
- [x] 增加 `--latest`：抓取候选文章元数据、按 account 过滤、按 published 排序
- [x] 记录 Tavily 对 account-only 最新文章召回不足的限制
- [ ] 选择更稳定的“最新文章”数据源并实现 fallback

## Known Issues
- Tavily account-only query 对“智能车参考”最新文章召回不足，严格 `--latest` 返回 0 个 URL。
- 当前 repo 中存在多项与本任务无关的未提交改动，应避免在本次提交中混入。

## Key Context
- Wiki repo: `/media/yhr/2T/files/wiki`
- Article conversion skill: `/home/yhr/.codex/skills/wechat-mp-to-markdown`
- URL discovery skill: `/home/yhr/.codex/skills/wechat-mp-url-discovery`
- Generated test files in repo include `wechat_article_FTyaA5WX0bRYtquzU9DzTA.md`, `wechat_urls_zhinengche*.txt/json`, `wechat_discovery_zhinengche*.md`, and `wechat_test_article_*.md`.
