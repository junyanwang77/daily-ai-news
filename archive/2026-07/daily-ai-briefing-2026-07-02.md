# 每日 AI 要闻

日期：2026-07-02
覆盖范围：过去 24 小时
版本：当日自动生成版

## 先说结论

Claude Code被曝暗藏代码识别中国用户，Anthropic承认将撤回。事件涉及AI工具透明度与中美AI竞争，开发者、企业均受影响。建议开发者关注官方后续更新，企业审视工具信任与合规风险。

## 今日最值得关注的 4 件事

过去24小时内可核实且足够重要的AI新闻不足5条，因此本期只收录4条（详见"核查说明"）。

### 1. Claude Code 被曝暗藏代码识别中国用户，Anthropic 承认并将撤回

* 来源：The Information、cybersecuritynews.com、IT之家、虎嗅、开发者 X 平台披露
* 链接：https://www.theinformation.com/briefings/anthropic-backtracks-spyware-targeting-chinese-users-controversy ；https://www.ithome.com/0/971/118.htm ；https://cybersecuritynews.com/anthropic-claude-hidden-code/
* 核查状态：部分核实
* 发生了什么：开发者 LegitMichel777 于6月30日披露，Claude Code 自今年4月2日发布的2.1.91版本起，暗藏根据系统时区（如 Asia/Shanghai、Asia/Urumqi）和代理服务器域名识别中国用户的逻辑，通过系统提示词中不可见的 Unicode 字符替换和日期格式变化打标记，且发布日志未披露。Anthropic 员工 Thariq Shihipar 在 X 上回应称，这是今年3月启动的"反转售/反模型蒸馏"实验，将在下一版本中删除。
* 为什么重要：涉及未向用户披露的追踪机制，引发对 AI 编程工具透明度和信任的广泛质疑，且发生在中美 AI 竞争与此前 Anthropic 指控阿里关联方规模化"蒸馏"其模型的背景下，具有较强敏感性。
* 影响对象：开发者、企业、AI学习者、普通用户
* 重要性评分：8
* 可信度：中
* 备注：目前主要依据开发者社区的逆向工程分析和多家科技媒体转述，尚未看到独立第三方代码审计或 Anthropic 完整官方声明；该机制与6月10日 Anthropic 指控阿里关联实体"蒸馏"Claude 模型（约2900万次对话、约2.5万个账号）之间的关联，官方未明确说明，请勿过早下结论。

### 2. 美国商务部解除对 Anthropic Fable 5 / Mythos 5 出口管制，模型全球恢复访问

* 来源：Anthropic 官方新闻稿、CNBC、Forbes、The Hacker News
* 链接：https://www.anthropic.com/news/redeploying-fable-5 ；https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html
* 核查状态：已核实
* 发生了什么：Fable 5 与 Mythos 5 于6月9日发布，6月12日因亚马逊研究人员发现的越狱漏洞被美国商务部实施出口管制，禁止所有非美籍用户（含海外员工）访问；6月30日管制解除，7月1日起全球用户可通过 Claude Platform、Claude.ai、Claude Code、Claude Cowork 重新访问，Pro/Max/Team及部分Enterprise用户到7月7日前可用最多50%的周使用额度免费试用。
* 为什么重要：这是前沿AI模型因具体安全事件遭美国出口管制、又因风险评估完成而解除的典型案例，反映监管与模型安全事件的直接联动，对企业合规评估和国际用户访问有直接影响。
* 影响对象：企业、开发者、投资者、普通用户
* 重要性评分：7
* 可信度：高
* 备注：无

### 3. Anthropic 与 OpenAI 同日杀入"AI for Science"赛道：Claude Science 对垒 GeneBench-Pro

* 来源：TechFundingNews、Dataconomy、HPCwire/AIwire、新浪科技
* 链接：https://techfundingnews.com/anthropic-launches-claude-science-and-google-and-openai-are-already-racing-to-match-it/ ；https://finance.sina.com.cn/tech/roll/2026-07-02/doc-inifkqfw0383467.shtml
* 核查状态：已核实
* 发生了什么：6月30日，Anthropic 推出科研工作台"Claude Science"，接入60多个科研数据库和技能包，面向 Pro/Max/Team/Enterprise 付费用户开放 macOS/Linux 端 beta 测试，并资助最多50个 AI4S 项目（申请截止7月15日）；同日 OpenAI 发布评测基准"GeneBench-Pro"，涵盖基因组学等10个领域共129道真实科研任务题，其最强模型 GPT-5.6 Sol 仅完成28.7%（Pro模式下31.5%）。
* 为什么重要：两大模型公司的竞争焦点从聊天机器人、编程转向科研工作流，行业判断是 AI4S 的瓶颈已不在模型能力本身，而在端到端可靠性，这将影响科研机构、药企、高校采用AI的路径选择。
* 影响对象：研究者、企业、开发者、投资者
* 重要性评分：7
* 可信度：高
* 备注：无

### 4. 软银完成对 OpenAI 第二笔100亿美元追加投资，累计投资突破600亿美元

* 来源：SoftBank Group 官方新闻稿
* 链接：https://group.softbank/en/news/press/20260701
* 核查状态：已核实
* 发生了什么：软银通过 SoftBank Vision Fund 2 于7月1日（日本时间）完成对 OpenAI 追加投资的第二笔100亿美元，这是此前2月27日宣布的总额300亿美元追加投资计划的一部分；软银为此在3月27日签署的过桥贷款协议下借款100亿美元，第三笔100亿美元计划于10月1日完成。
* 为什么重要：这是软银对 OpenAI 持续加码的最新确认动作，反映投资方对 OpenAI 长期发展的资金承诺，其借款结构和分期节奏也是观察 OpenAI 资金链和潜在上市安排的重要窗口。
* 影响对象：投资者、企业、创业者
* 重要性评分：6
* 可信度：高
* 备注：另有美国媒体报道软银正就一笔以 OpenAI 股权为抵押的100亿美元保证金贷款进行谈判，这是与上述追加股权投资不同的另一笔交易，截至目前尚未确认达成，请勿与本条追加投资混淆。

## 持续关注

- **Claude Sonnet 5 正式发布**（首次报道：2026-06-30）：已成为 Claude 免费版和 Pro 版的默认模型，并在 Claude Code、Claude Platform 上线，通过8月31日的优惠定价期正在推广中；后续值得关注其代理能力表现和优惠期结束后的定价变化。
- **DeepSeek 遗留 API 模型名将于7月24日下线**（首次报道：2026年4月）：`deepseek-chat`、`deepseek-reasoner` 两个旧模型名将在7月24日彻底停用并路由变化，开发者需在此前完成向 `deepseek-v4-flash`/`deepseek-v4-pro` 的迁移，距离截止日期仅剩约3周。
- **软银百亿美元保证金贷款谈判**（首次报道：2026-07-01）：据报道软银正就一笔以 OpenAI 股权为抵押的100亿美元贷款续谈并追加条件，尚无最终结果，值得关注是否落地及对软银财务杠杆的影响。

## 对普通人的影响

今天的AI新闻主要发生在企业和技术层面，对普通用户直接影响有限，但有两点值得留意。一是如果你使用 Claude Code 这类AI编程工具，要知道曾出现未披露的用户识别代码，公司已表示会撤回，但这提醒大家使用AI工具时要关注隐私和透明度问题，非必要不必恐慌，也不必只看单一信息源就下结论。二是 Anthropic 的 Fable 5、Mythos 5 模型已重新对所有地区用户开放，如果你之前无法使用可以再试试。目前这些消息大多来自科技媒体和公司官方声明，整体可信度较高，但关于"隐藏代码"事件的完整细节仍在核实中，建议理性看待，不必过度解读为"AI监控用户"的确定结论。

## 对学习者 / 开发者的影响

* 如果你在用 Claude Code，建议关注 Anthropic 后续版本更新说明，了解相关识别逻辑是否已按承诺删除，这也是学习AI编程工具安全审计思路的一个真实案例（对应新闻1）。
* 如果你的应用调用 DeepSeek 旧版 `deepseek-chat`/`deepseek-reasoner` API，应尽快测试迁移到 `deepseek-v4-flash` 或 `deepseek-v4-pro`，避免7月24日后接口路由变化影响生产环境（对应"持续关注"）。
* 关注 Claude Science 和 GeneBench-Pro 释放的信号：科研类AI应用的重点正从"模型够不够强"转向"工作流是否可靠端到端完成任务"，做科研或医疗、生物方向AI应用的开发者可以研究这两套工具/评测的设计思路（对应新闻3）。

## 对创业者的影响

* AI工具的信任和透明度正成为竞争维度之一，如果你的产品涉及跨境用户或调用第三方大模型API，应提前审视自己的数据处理和用户识别逻辑是否披露充分，避免陷入类似信任危机（对应新闻1，基于目前有限信息，事件后续走向仍需观察）。
* 科研垂直领域的AI工具（Claude Science、GeneBench-Pro）显示"科研Agent+工作流"是巨头新的必争之地，中小创业者若想切入AI4S领域，更现实的机会可能在细分场景的工作流打磨，而非直接对标底层模型能力（对应新闻3）。
* 头部大模型公司资金持续加码（软银百亿美元级追加投资）意味着算力和资本门槛将进一步抬高，对依赖自研通用大模型的创业者是压力信号，但也意味着围绕Agent、垂直应用的生态位仍有空间（对应新闻4，短期融资节奏不宜过度解读为长期趋势判断）。

## 我的判断

我的判断：今天最值得关注的不是某个新模型发布，而是 Claude Code 隐藏识别代码事件——它暴露出AI工具供应商在"反滥用"与"用户知情权"之间的紧张关系，且尚未完全实锤，需要理性观望而非过度反应。Anthropic 一边解除出口管制恢复模型全球访问、一边被曝出未披露的追踪机制，说明信任建设是双向的、脆弱的。AI4S 赛道的同日布局和软银持续加码则显示，头部玩家的竞争正从模型参数转向工作流生态与资本厚度。今天信息质量总体尚可，但"隐藏代码"事件的完整技术细节和公司最终处理结果仍有待跟进，暂不宜作为定论传播。

## 来源链接

* https://www.anthropic.com/news/redeploying-fable-5 — Anthropic 官方公告，确认 Fable 5 出口管制解除及全球恢复访问细节
* https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html — CNBC 报道出口管制解除背景
* https://www.theinformation.com/briefings/anthropic-backtracks-spyware-targeting-chinese-users-controversy — The Information 报道 Claude Code 隐藏代码争议及 Anthropic 回应
* https://www.ithome.com/0/971/118.htm — IT之家关于 Claude Code 事件的中文报道及 Anthropic 回应内容
* https://cybersecuritynews.com/anthropic-claude-hidden-code/ — 英文科技媒体对该事件技术细节的报道
* https://techfundingnews.com/anthropic-launches-claude-science-and-google-and-openai-are-already-racing-to-match-it/ — 报道 Claude Science 发布及与 GeneBench-Pro 的竞争格局
* https://finance.sina.com.cn/tech/roll/2026-07-02/doc-inifkqfw0383467.shtml — 新浪科技对 AI4S 赛道竞争的中文报道
* https://group.softbank/en/news/press/20260701 — 软银官方新闻稿，确认对 OpenAI 第二笔100亿美元追加投资
* https://www.anthropic.com/news/claude-sonnet-5 — Anthropic 官方公告，Claude Sonnet 5 发布详情（持续关注部分参考）

## 核查说明

本次简报已成功联网检索。核查过程覆盖了强制清单要求的六类信息源：中文科技媒体（机器之心、量子位、36氪、晚点）、中国AI公司动态（DeepSeek、字节跳动、月之暗面、阿里通义、智谱）、Hugging Face新发布、arXiv论文、GitHub趋势项目，以及英文媒体与OpenAI/Anthropic/Google DeepMind官方博客。

在筛选中，本次排除了两条经进一步核查确认为"旧闻"的信息：搜索结果中提到的"OpenAI 停用 Sora"和"字节跳动 Seedance 2.0 因版权问题暂停海外上线"，经核实实际分别发生于2026年2-4月和2026年2-3月，并非过去24小时内的新事件，因此未纳入今日要闻。

对于 Claude Code 隐藏代码事件，本次采用了"部分核实"标注，因为核心技术细节主要来自开发者社区的逆向工程分析（Reddit/GitHub/X）和多家媒体转述，虽然 Anthropic 员工已公开回应确认存在该机制并将撤回，但尚未看到完整的官方声明或独立第三方代码审计报告，故未将其可信度标注为"高"。

Hugging Face 新模型发布、arXiv 当日论文、GitHub Trending 当日新增项目三类搜索均未能定位到明确归属于"2026-07-02当天"且可核实细节的具体条目，因此本期未在"今日最值得关注"中收录相关内容，也未强行编造凑数。

未发现来源之间存在实质性冲突的重要新闻；关于软银的两笔交易（第二笔追加股权投资 vs. 保证金贷款谈判）容易混淆，已在正文备注中明确区分。
