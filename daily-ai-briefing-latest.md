# 每日 AI 要闻

日期：2026-11-28
覆盖范围：过去 24 小时
版本：隔离质量恢复测试版

## 先说结论

- 蚂蚁灵波披露机器人跨任务复用空间记忆的评测。

- 机器人可复用已有地图，自行移动仍是研发团队的验证重点。

- 开发者评估接入时，应分开测试找目标和走到目标。

## 今日最值得关注的 5 件事

本期经核查选入5条主新闻。

### 1. 蚂蚁灵波披露长距离建图与跨任务导航评测

- 来源：蚂蚁灵波
- 链接：[蚂蚁灵波](https://www.sttinfo.fi/tiedote/72542772/robbyant-open-sources-lingbot-map-20-and-lingbot-navi-enabling-long-term-spatial-memory-and-autonomous-navigation-for-robots?publisherId=58763726)、[蚂蚁灵波](https://github.com/Robbyant/lingbot-navi)、[蚂蚁灵波](https://huggingface.co/robbyant/lingbot-navi)、[蚂蚁灵波](https://github.com/Robbyant/lingbot-map-v2)、[蚂蚁灵波](https://huggingface.co/datasets/robbyant/LingBot-Navi)
- 核查状态：已核实
- 影响对象：开发者 / 研究者 / 创业者
- 重要性评分：9
- 可信度：高

- 发生了什么：蚂蚁灵波于北京时间 11 月 27 日 16:10 分发建图与导航联合公告，披露长距离建图、跨任务空间记忆和导航的测试结果，并链接代码、权重和数据。

LingBot-Navi 在重建三维场景中锚定视觉特征，通过跨任务保留的空间记忆定位目标并规划路径。基于 Qwen3.5-4B 的 Navigation Transformer 负责场景推理，Local Planner 负责局部路径执行。

据灵波，GCR 在推理时复用已提取的局部几何来重对齐历史记忆，无须重新编码图像。在 VBR 一段 5.2 公里城市轨迹上，团队报告平均轨迹误差由 1.0 的 31.12 米降至 4.72 米，最佳外部回环对照为 9.98 米。

灵波报告，在 GOAT-Bench 子集中由模型选目标、模拟器执行移动时，成功率为 68.60%，比六种对照中的最佳结果高 10.36 个百分点。当模型同时负责规划和移动执行时，团队报告 GOAT-Bench 成功率为 56.09%，基于 36 处实采场地重建的自有评测集成功率为 32.36%。

- 为什么重要：重对齐历史地图有助于控制长距离建图的累积误差，跨任务记忆让机器人在找新目标时复用已重建的场景。模拟器代走侧重检验目标选择，模型自行移动还要检验路径执行。若要判断能否部署，应在目标场地测试定位、规划和移动能否连续完成。

- 备注：灵波导航仓库将推理代码、权重和数据集的首次公开记为 11 月 26 日，建图仓库将流式推理代码发布和评测补充分别记为 11 月 21 日和 23 日。

LingBot-Map 2.0 公开的流式基础版从 RGB 序列预测相机位姿、内参、深度和置信度。仓库注明基础版不含执行历史空间记忆重对齐的 GCR，团队原创代码和基础权重采用 CC BY-NC 4.0。

LingBot-Navi 的导航和局部规划权重采用 Apache 2.0，配套数据集采用 CC BY-NC-SA 4.0。仓库列出 511 个真实场景的重建数据，并注明 GOAT-Bench 任务和 HM3D 场景需要另行获取。

### 2. 欧盟 AI 办公室征集系统性风险模型的嵌入式评估方案

- 来源：欧盟 AI 办公室
- 链接：[欧盟 AI 办公室](https://digital-strategy.ec.europa.eu/en/news/call-participants-workshop-embedded-evaluations-gpai-models-systemic-risk)
- 核查状态：已核实
- 影响对象：企业 / 开发者 / 研究者
- 重要性评分：9
- 可信度：高

- 发生了什么：欧盟 AI 办公室 11 月 27 日征集嵌入式评估方案，计划于 2027 年 1 月举行线上研讨会，并将提交意向或方案的截止日定为 12 月 9 日。征集拟讨论如何让合格且独立的外部评估者在较长时间内获得接近员工级别的内部访问。

欧盟 AI 办公室将内部模型、训练数据、部署日志、监测系统和事故记录的访问范围与期限，以及结果发表权、删节条件、评估者轮换和冷静期列为研讨议题。公告将这些问题定位为讨论材料。

- 为什么重要：外部评估者若能持续查看训练材料、部署日志和事故记录，就可以把测试中发现的问题与部署后的实际表现相互印证。发表权、删节条件和人员轮换会影响外部团队能否独立报告发现。

### 3. 台湾上修今明两年增长预测，纳入 AI 算力需求与出口回温

- 来源：台湾主计总处、中央社
- 链接：[台湾主计总处](https://www.dgbas.gov.tw/News_Content.aspx?n=3602&s=236908)、[中央社](https://www.cna.com.tw/news/afe/202611270234.aspx)
- 核查状态：已核实
- 影响对象：投资者 / 企业 / 创业者
- 重要性评分：8
- 可信度：高

- 发生了什么：台湾主计总处 11 月 27 日将 2026 年实际 GDP 增速预测由 11.05% 上调 2.23 个百分点至 13.28%，并将 2027 年预测由 6.04% 上调 0.47 个百分点至 6.51%。

据中央社对主计总处简报的报道，云服务商扩大 AI 基础设施、推理需求扩大、记忆体与载板涨价和传统产品出口回温均纳入预测判断。主计总处将 2026 年商品及服务输出增幅预测上修至 23.96%。

- 为什么重要：云厂商扩大基础设施、推理需求增长，是主计总处判断出口的依据之一。零部件涨价和传统产品出口回温也进入预测。投资者若要判断 AI 硬件需求是否持续，可以分开观察出货量和价格。

### 4. OpenAI 在消费硬件商业秘密案中反诉苹果

- 来源：CBS News、Reuters
- 链接：[CBS News](https://www.cbsnews.com/news/openai-countersues-apple-trade-secrets-lawsuit/?intcid=CNI-00-10aaa3a)、[Reuters](https://www.theguardian.com/technology/2026/nov/27/openai-countersues-apple-trade-secrets)
- 核查状态：已核实
- 影响对象：创业者 / 企业 / 开发者
- 重要性评分：7
- 可信度：高

- 发生了什么：CBS News 与 Reuters 分别报道称，OpenAI 于美国当地 11 月 27 日在加州北区联邦法院对苹果提出反诉，涉及苹果围绕消费硬件研发及前员工提起的商业秘密诉讼。

- 为什么重要：这起争议涉及消费硬件研发中的人员流动，反诉进一步把离职流程和设备资料管理带入争议。AI 团队若从成熟硬件厂商招募工程师，可以在入职时明确前雇主资料的处理边界，让新项目的研发来源可查。

- 备注：OpenAI 在反诉中主张苹果的离职与设备管理安排使其容易对前员工和新雇主提起商业秘密指控，苹果发言人向 CBS 表示反诉意在转移对原诉的注意，双方的实体主张仍待裁判。

### 5. 帕西尼武汉具身数据工厂开业，同步采集触觉与动作

- 来源：闪电快讯、上海证券报、长江日报
- 链接：[闪电快讯](https://www.jiemian.com/article/15384902.html)、[上海证券报](https://finance.eastmoney.com/a/202611283942328041.html)、[长江日报](https://www.wuhan.gov.cn/sy/whyw/202603/t20260318_2742118.shtml)
- 核查状态：已核实
- 影响对象：开发者 / 研究者 / 创业者
- 重要性评分：7
- 可信度：高

- 发生了什么：帕西尼武汉具身超级数据工厂于 11 月 27 日在武汉东西湖区开业，现场同步发起华中具身智能生态联合体倡议，同一项目于 3 月已公布开工。

据现场报道，帕西尼使用五指和三指设备同步记录触觉、视觉、位姿和动作。公司称采集可脱离特定机器人本体，并计划用真机任务验证数据质量。

开业披露显示，帕西尼武汉工厂拥有 220 余个开放式采集单元和约 700 人采集团队。

- 为什么重要：同步记录接触、画面和动作，可以把操作过程与接触反馈对应起来。若同一批数据能在不同机器人本体上改善任务表现，研发团队就有依据估算复用数据能节省多少采集工作。

## 持续关注

- **SAP 回应减员报道，称尚未决定进一步措施**

11 月 26 日 Bloomberg 报道 SAP 可能大规模减员后，11 月 27 日 Dow Jones 刊出 SAP 发言人称尚未决定进一步措施的回应，Reuters 当天另引两名匿名人士称 SAP 正准备大幅减员。

若 SAP 随后确认涉及哪些岗位和业务，再据此判断调整范围及其与 AI 的关系。

- **GPT-6 Astra 辅助的量子引力预印本受到同行质疑**

Venkatesa Chandrasekaran 于 11 月 25 日提交的预印本提出从相交零锥上的引力约束构造四维真空广义相对论的量子化框架，方案的物理有效性仍待独立检验。

El País 于 11 月 27 日刊出对 GPT-6 Astra 辅助的量子引力预印本的同行采访。Alejandro Vilar 质疑方案的基本有效性，José Luis Barbón 指出其技术假设可能改变物理结论。

独立复核应检验相交零锥上的引力约束能否支撑论文提出的量子化框架，并验证受质疑的技术假设是否影响物理结论，以及可能影响哪些结论。

- **Notion 称正改善 AI 用量效率，具体安排待明确**

Notion 于 10 月 19 日宣布新的 AI 额度体系，并将现有客户的迁移日期定为 11 月 2 日。Standard 额度用于平台自动选模型，Select 额度用于自行指定模型或运行自定义代理。

Tom’s Guide 于 11 月 27 日报道，Notion 在答复记者时称正在提高 AI 功能的用量效率，并希望让用户更容易接入已在使用的 AI。公司在这篇报道中未给出上线时点或可量化的额度节省。

如果效率改进上线，付费团队可以用相同任务分别比较自动选模型和运行自定义代理的额度消耗，再决定是否调整预算。

## 对普通人的影响

- 空间记忆让机器人下次找东西时还能利用以前建好的地图。看演示时，可以分别留意它能否指出目标的位置，以及能否自己一路走到目标。

- 使用 Notion AI 的人可以先按现有额度规划工作量。公司已回应会提高用量效率，具体上线时间和可节省的额度仍待明确。

## 对学习者 / 开发者的影响

- 试跑 LingBot-Navi 时，分别记录目标定位和端到端任务成功率。复现前确认已取得 GOAT-Bench 任务与 HM3D 场景，并分别核对权重和数据许可。

- 用自己的长序列测试 LingBot-Map 流式基础版，记录位姿漂移。对照公告中的长轨迹成绩时，注明公开基础版缺少 GCR，说明两组测试的条件差异。

- 如果准备提交嵌入式评估方案，可以选一类部署风险，写清要访问哪些模型和日志、需要访问多久，以及发表发现时如何处理敏感内容。

## 对创业者的影响

- 如果考虑采购触觉训练数据，可以用自有机器人完成同一组任务，比较加入外采数据前后的成功率。用采集单元和团队规模估算供给，再用真机结果判断采购价值。

- 如果产品依赖 Notion 自定义代理，按现行 Select 额度估算高频用户的边际成本。把用量优化可能带来的节省留在备选情景，等扣费规则明确后再纳入定价。

- 如果正在组建消费硬件团队，可以在入职交接时明确前雇主资料和设备的处理规则，并记录关键设计的来源。研发资料的归属若受到质疑，团队就有记录可查。

## 我的判断

我最看重的是，AI 系统进入实际工作流程后，研发方能否拿出可复核的任务结果。灵波在模拟器代走和模型自行移动两种设置下的成绩，提示团队应把找对目标和完成任务分开验收。帕西尼采集的触觉数据若能在真机对照中改善特定动作，采购方就能据此估算训练收益。欧盟的征集涉及另一项条件。外部评估者若能追踪部署记录并保有发表权，测试发现就更容易接受独立检验。我会优先关注公开任务条件、对照结果和失败记录的进展。

## 来源链接

1. [蚂蚁灵波](https://www.sttinfo.fi/tiedote/72542772/robbyant-open-sources-lingbot-map-20-and-lingbot-navi-enabling-long-term-spatial-memory-and-autonomous-navigation-for-robots?publisherId=58763726)
2. [蚂蚁灵波](https://github.com/Robbyant/lingbot-navi)
3. [蚂蚁灵波](https://huggingface.co/robbyant/lingbot-navi)
4. [蚂蚁灵波](https://github.com/Robbyant/lingbot-map-v2)
5. [蚂蚁灵波](https://huggingface.co/datasets/robbyant/LingBot-Navi)
6. [欧盟 AI 办公室](https://digital-strategy.ec.europa.eu/en/news/call-participants-workshop-embedded-evaluations-gpai-models-systemic-risk)
7. [台湾主计总处](https://www.dgbas.gov.tw/News_Content.aspx?n=3602&s=236908)
8. [中央社](https://www.cna.com.tw/news/afe/202611270234.aspx)
9. [CBS News](https://www.cbsnews.com/news/openai-countersues-apple-trade-secrets-lawsuit/?intcid=CNI-00-10aaa3a)
10. [Reuters](https://www.theguardian.com/technology/2026/nov/27/openai-countersues-apple-trade-secrets)
11. [闪电快讯](https://www.jiemian.com/article/15384902.html)
12. [上海证券报](https://finance.eastmoney.com/a/202611283942328041.html)
13. [长江日报](https://www.wuhan.gov.cn/sy/whyw/202603/t20260318_2742118.shtml)
14. [Reuters](https://uk.marketscreener.com/news/sap-seeks-to-cut-sizeable-number-of-jobs-sources-say-ce7851d9dd8af32d)
15. [Dow Jones Newswires](https://www.marketscreener.com/news/sap-says-no-decisions-made-on-job-cuts-as-ai-reshapes-landscape-ce7851d9da8cf327)
16. [arXiv](https://arxiv.org/abs/2611.34924)
17. [El País](https://elpais.com/ciencia/2026-11-27/rebelion-cientifica-tras-el-anuncio-de-un-colaborador-de-openai-que-asegura-haber-resuelto-el-gran-problema-de-la-fisica.html)
18. [Notion](https://www.notion.com/blog/notion-ai-more-for-less)
19. [Tom’s Guide](https://www.tomsguide.com/ai/notion-confirms-itll-make-ai-token-usage-more-efficient-following-community-feedback)
20. [同期公开上界：agiright.org](https://agiright.org/topics)

## 核查说明

独立核查阶段依据已留存原文、风险复核和补充搜索审定事实；转载同一上游不视为独立交叉证实。固定窗口：2026-11-27T08:40:00+08:00 至 2026-11-28T08:40:00+08:00。定稿与语义审查禁用网页检索，模型推理通过在线服务完成。仅日期或未知时间的来源按结构化证据保留不确定性，同期公开上界链接已列于来源表。
