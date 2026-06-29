# 每日 AI 要闻

日期：2026-06-29
覆盖范围：过去 24 小时
版本：当日自动生成版

## 先说结论

- 今天是周日，过去24小时内重大新事件较少，但本周多条重磅消息仍在持续发酵。
- OpenAI GPT-4.5 已于6月27日从 ChatGPT 正式退役，GPT-4 时代彻底终结。
- 开发者应关注推理芯片自研趋势和前沿模型延期对产品规划的影响。

## 今日最值得关注的 5 件事

### 1. OpenAI GPT-4.5 正式从 ChatGPT 退役，GPT-4 时代终结

- 来源：OpenAI 官方发布说明、TechRadar、Bleeping Computer
- 链接：[https\://help.openai.com/en/articles/6825453-chatgpt-release-notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- 核查状态：已核实
- 发生了什么：6 月 27 日，OpenAI 按照 5 月 28 日公布的 30 天过渡期计划，正式将 GPT-4.5 从 ChatGPT 中移除。这是 ChatGPT 内最后一个 GPT-4 系列模型，现有对话将自动迁移到 GPT-5.5。GPT-4.5 仍可通过 API 访问。
- 为什么重要：标志着 GPT-4 时代在消费端正式终结。依赖 GPT-4.5 特定行为的自定义 GPT 和工作流需要尽快迁移和测试。
- 影响对象：开发者 / 普通用户 / 企业
- 重要性评分：7
- 可信度：高
- 备注：该信息为 6 月 27 日生效，在过去 48 小时内。API 端 GPT-4.5 暂未退役。

### 2. OpenAI 与 Broadcom 联合发布首款自研推理芯片 Jalapeño

- 来源：OpenAI 官方博客、Broadcom 投资者新闻稿、TechCrunch、CNBC、Bloomberg、VentureBeat、Tom's Hardware
- 链接：[https\://openai.com/index/openai-broadcom-jalapeno-inference-chip/](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/)
- 核查状态：已核实
- 发生了什么：6 月 24 日，OpenAI 和 Broadcom 联合发布 Jalapeño——OpenAI 首款定制 AI 推理芯片。该芯片从设计到流片仅用 9 个月，专为大语言模型推理优化，早期测试显示每瓦性能显著优于现有方案，推理成本较传统 GPU 降低约 50%。计划 2026 年底小规模部署，2028 年上半年全面量产。
- 为什么重要：这是 OpenAI 向全栈自研迈出的关键一步，直接挑战 NVIDIA 在 AI 推理领域的主导地位。如果量产顺利，将大幅降低 ChatGPT 等产品的运营成本，并可能引发 AI 芯片价格竞争。
- 影响对象：开发者 / 企业 / 投资者 / 创业者
- 重要性评分：9
- 可信度：高
- 备注：该事件发生于 6 月 24 日，非过去 24 小时内首次发生，但影响重大且仍在持续讨论中。量产时间表（2027-2028）存在执行风险。

### 3. Anthropic 指控阿里巴巴 Qwen 团队发动史上最大规模模型蒸馏攻击

- 来源：Anthropic 致美国参议员正式投诉信、CNBC、TechCrunch
- 链接：[https\://www\.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html](https://www.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html)
- 核查状态：部分核实
- 发生了什么：6 月 24 日，Anthropic 向美国参议员 Warren 和 Scott 提交正式投诉，指控阿里巴巴旗下 Qwen AI 实验室通过约 25,000 个虚假账户，在 4 月 22 日至 6 月 5 日期间对 Claude 模型发起超过 2880 万次对话交互，目的是提取 Claude 的软件工程和智能体推理能力。该规模超过此前 DeepSeek、MiniMax、月之暗面三家蒸馏行为的总和。
- 为什么重要：模型蒸馏攻击正在成为 AI 行业严重的知识产权争端焦点。美国参议员已着手推动立法制裁此类行为，可能加剧中美 AI 领域的对抗。
- 影响对象：开发者 / 企业 / 投资者 / 研究者
- 重要性评分：8
- 可信度：中
- 备注：目前主要依据 Anthropic 单方面指控，阿里巴巴尚未公开回应。蒸馏行为的具体技术细节和法律定性仍有争议。可信度标为"中"是因为缺乏被指控方的回应和独立第三方验证。

### 4. Google DeepMind 六天内失去四名核心 AI 研究员

- 来源：Bloomberg、TechCrunch、The Next Web、Yahoo Finance
- 链接：[https\://techcrunch.com/2026/06/24/ai-researchers-continue-to-leave-google-for-its-rivals/](https://techcrunch.com/2026/06/24/ai-researchers-continue-to-leave-google-for-its-rivals/)
- 核查状态：已核实
- 发生了什么：6 月 18 日至 24 日期间，四名 Google DeepMind 高级研究员相继离职：Transformer 论文共同作者、Gemini 联合负责人 Noam Shazeer（加入 OpenAI）；诺贝尔奖得主、AlphaFold 负责人 John Jumper（加入 Anthropic）；Gemini AI 编程负责人 Jonas Adler 和预训练专家 Alexander Pritzel（均加入 Anthropic）。
- 为什么重要：这是 Google AI 历史上最严重的人才流失事件之一。核心研发人员的集中离开可能影响 Gemini 的迭代速度，同时显著增强 OpenAI 和 Anthropic 的研发实力。背后原因包括 OpenAI 和 Anthropic 即将 IPO 带来的财务激励，以及 Google 内部算力资源分配争议。
- 影响对象：开发者 / 企业 / 投资者 / 研究者
- 重要性评分：8
- 可信度：高
- 备注：该事件发生于 6 月 18-24 日，非过去 24 小时内首次报道，但仍是本周最重要的行业动态之一。Alphabet 股价因此及相关因素单周下跌，Nasdaq 单日下跌 2.21%。

### 5. 多款前沿模型（GPT-5.6、Gemini 3.5 Pro、Grok 5）确认延期至 7 月

- 来源：BuildFastWithAI、AI Updates Today（llm-stats.com）
- 链接：[https\://llm-stats.com/llm-updates](https://llm-stats.com/llm-updates)
- 核查状态：部分核实
- 发生了什么：原定 6 月发布的三款前沿模型——OpenAI GPT-5.6、Google Gemini 3.5 Pro、xAI Grok 5——均未能如期交付，预计推迟至 7 月。
- 为什么重要：三大模型同时延期在行业内罕见，可能表明前沿模型研发正在遭遇规模化瓶颈或内部质量标准提高。对于依赖特定模型能力规划产品的开发者和创业者，需要重新评估时间线。
- 影响对象：开发者 / 创业者 / 企业 / 研究者
- 重要性评分：7
- 可信度：中
- 备注：该信息主要来自 AI 新闻聚合网站，尚未看到三家公司各自的官方确认声明。GPT-5.6 和 Grok 5 的具体延期原因未知。Gemini 3.5 Pro 延期曾被 AIToolsRecap 报道。可信度标为"中"因为缺乏官方声明。

## 持续关注

- **DeepSeek V4.1 发布悬念**（首次报道：2026-05-08）：原定 6 月中旬发布的 V4.1（含原生 MCP 协议支持和全模态能力）至今未见官方发布公告，当前最新模型仍为 V4-Pro 和 V4-Flash。值得跟踪是否会进一步延期。
- **Anthropic 营收与算力扩张**（首次报道：2026-04-07）：Anthropic 年化营收已突破 300 亿美元，与 Google/Broadcom 签署约 3.5GW 算力协议（2027 年交付）。规模扩张速度是否可持续值得观察。
- **DeepSeek 510 亿元融资完成**（首次报道：2026-05-09）：DeepSeek 以约 4000 亿元估值完成首轮外部融资 510 亿元，投资方包括腾讯、宁德时代、京东、网易等。创始人梁文锋个人出资 200 亿元。该轮融资刷新中国 AI 行业单轮融资记录。

## 对普通人的影响

如果你是 ChatGPT 用户，最直接的变化是 GPT-4.5 已经不可用了，你的对话会自动切换到 GPT-5.5。对大多数人来说，GPT-5.5 性能更好，这个过渡应该是无感的。但如果你之前创建了依赖 GPT-4.5 的自定义 GPT，需要检查它们是否还能正常工作。

OpenAI 自研芯片的消息对普通人的短期影响不大，但中长期来看，推理成本降低意味着 AI 服务的价格可能进一步下降，免费额度可能增加。

关于 Anthropic 和阿里巴巴的蒸馏争端，这属于行业层面的知识产权之争，目前不会直接影响普通用户使用任何 AI 产品。但需要注意的是，中美 AI 领域的紧张关系可能影响某些模型和服务在不同地区的可用性。

提醒：部分消息（如模型延期、蒸馏指控）尚未完全核实，不宜过早下结论。

## 对学习者 / 开发者的影响

1. **迁移测试 GPT-4.5 依赖**：如果你有使用 GPT-4.5 的应用或自定义 GPT，现在需要在 GPT-5.5 上测试兼容性。API 端 GPT-4.5 暂未退役，但退役只是时间问题，建议尽早准备。（对应新闻 #1）
2. **关注推理芯片自研趋势**：OpenAI Jalapeño 芯片意味着 AI 推理架构正在从通用 GPU 向专用 ASIC 转型。对于做模型部署和推理优化的开发者，了解 LLM 推理的硬件瓶颈（内存带宽、算力利用率）将成为差异化能力。（对应新闻 #2）
3. **模型延期意味着当前版本窗口延长**：GPT-5.5、Claude Sonnet 4.6、DeepSeek V4-Pro 等当前模型的生命周期可能比预期更长。如果你正在选型或构建应用，不必急于等待下一代模型，可以基于现有模型稳定开发。（对应新闻 #5）

## 对创业者的影响

1. **AI 推理成本下降趋势明确**：OpenAI 自研芯片目标降低 50% 推理成本，叠加 Anthropic 大规模扩张算力，行业整体推理价格将继续下降。对于 AI 应用创业者，这意味着产品毛利空间将改善，但同时也意味着竞争门槛进一步降低——纯粹靠调用 API 构建的产品护城河将更窄。（基于新闻 #2，判断依据较充分但成本降低时间表存在不确定性）
2. **人才格局剧变带来的机会窗口**：Google DeepMind 的人才流失和各大公司的 IPO 预期正在重塑 AI 人才市场。对于创业公司来说，当大公司内部动荡时，反而可能有机会吸引到被忽视的优秀人才。但需注意，顶级研究员的薪酬预期已被 IPO 前期权推到极高水平。（基于新闻 #4）
3. **警惕模型蒸馏的法律风险**：Anthropic 对 Qwen 团队的指控如果引发立法行动，可能改变使用 AI 模型输出训练其他模型的法律边界。如果你的产品或训练流程涉及使用第三方模型的输出数据，现在就应该审查相关条款和合规风险。（基于新闻 #3，但立法进程尚不确定）

## 我的判断

我的判断：本周最值得关注的不是任何单一事件，而是一个明显的行业信号——前沿 AI 的竞争正在从"谁的模型更强"转向"谁的基础设施更深"。OpenAI 自研芯片、Anthropic 签下 3.5GW 算力、Google 核心人才外流，这三件事放在一起看，说明 AI 行业的真正战场正在下沉到芯片、算力和人才这些更基础的层面。模型能力的差距在缩小（多款前沿模型延期可能暗示着性能瓶颈），但基础设施和组织能力的差距在拉大。对于中国 AI 行业，DeepSeek 的巨额融资和 Qwen 蒸馏争端则提醒我们，自主研发能力和合规建设的紧迫性在上升。需要提醒的是，本期部分信息（模型延期时间表、蒸馏指控细节）尚未完全核实，以上判断可能需要根据后续信息调整。

## 来源链接

1. OpenAI 官方发布说明 - ChatGPT Release Notes：[https\://help.openai.com/en/articles/6825453-chatgpt-release-notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) （支持 GPT-4.5 退役信息）
2. OpenAI 官方博客 - Jalapeño 芯片发布：[https\://openai.com/index/openai-broadcom-jalapeno-inference-chip/](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/) （支持 Jalapeño 芯片信息）
3. Broadcom 投资者新闻稿：[https\://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-unveil-llm-optimized-intelligence-processor](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-unveil-llm-optimized-intelligence-processor) （交叉验证 Jalapeño 芯片信息）
4. TechCrunch - OpenAI Jalapeño 报道：[https\://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom/](https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom/) （交叉验证）
5. CNBC - Anthropic 指控阿里巴巴蒸馏：[https\://www\.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html](https://www.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html) （支持蒸馏攻击信息）
6. TechCrunch - Google AI 研究员离职：[https\://techcrunch.com/2026/06/24/ai-researchers-continue-to-leave-google-for-its-rivals/](https://techcrunch.com/2026/06/24/ai-researchers-continue-to-leave-google-for-its-rivals/) （支持人才流失信息）
7. Bloomberg - Google 研究员离职报道：[https\://www\.bloomberg.com/news/articles/2026-06-24/google-poised-to-lose-two-more-high-profile-ai-staffers-to-anthropic](https://www.bloomberg.com/news/articles/2026-06-24/google-poised-to-lose-two-more-high-profile-ai-staffers-to-anthropic) （交叉验证人才流失）
8. Anthropic 官方公告 - Google/Broadcom 算力合作：[https\://www\.anthropic.com/news/google-broadcom-partnership-compute](https://www.anthropic.com/news/google-broadcom-partnership-compute) （支持持续关注中 Anthropic 算力信息）
9. IT之家 - DeepSeek 融资报道：[https\://www\.ithome.com/0/965/686.htm](https://www.ithome.com/0/965/686.htm) （支持 DeepSeek 融资信息）
10. llm-stats.com - AI 模型更新追踪：[https\://llm-stats.com/llm-updates](https://llm-stats.com/llm-updates) （支持模型延期信息，但非官方一手来源）

## 核查说明

- **是否成功联网**：是，通过多个搜索引擎成功获取了实时信息。
- **主要参考来源类型**：公司官方博客与新闻稿（OpenAI、Broadcom、Anthropic）、权威科技媒体（TechCrunch、CNBC、Bloomberg）、行业追踪网站（llm-stats.com）、中文科技媒体（IT之家、量子位）。
- **是否存在未完全核实的信息**：是。第 3 条（Anthropic 蒸馏指控）仅有 Anthropic 单方面说法，阿里巴巴未回应；第 5 条（多款模型延期）缺乏各公司官方确认声明。
- **是否存在来源冲突**：未发现直接冲突，但蒸馏指控事件中，只有指控方的说法，缺乏被指控方回应，不构成冲突但构成信息不完整。
- **因无法核实而排除的信息**：排除了部分社交媒体上关于 DeepSeek V4.1 具体发布日期的传闻（多个说法不一致，官方未确认）。排除了关于 ChatGPT 市场份额跌破 50% 的说法（仅见于单一聚合网站，未找到原始数据来源）。

