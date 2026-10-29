# 公开调研与参考资料

调研整理日期：2026 年 10 月 29 日。来源区分厂商公开说明、创始人采访、社区原型与论文；它们不构成本项目效果证明。

| 参考方向 | 纳入设计的部分 | 使用边界 |
| --- | --- | --- |
| GameSkill 创始人访谈 | 专业复盘、专家判据、端侧响应思路 | 访谈中的效果自述没有转成本项目指标 |
| Doubao 电竞教练社区实践 | 分片时间戳、专项分析、单场与多场汇总 | 多 Agent 拆分仍需独立评测 |
| 蛋蛋君与 WeGame | 版本化知识、新手引导、构筑与装备建议 | 未推测其内部模型或知识库接口 |
| Xbox、NVIDIA ACE、Ubisoft、Razer | 按需观察、快速响应、Agent 与知识检索的分工 | 区分游戏助手、可行动队友、实验原型与教练 |
| GameplayQA、Video-Arena | 3D 角色归因、事件、状态更新与追踪评测 | 论文结果不等于本包性能 |

- [[1] 品玩访谈 陈迪 GameSkill](https://www.pingwest.com/a/310291)：创始人自述专业训练、专家数据与端侧方向。
- [[2] 火山引擎社区 Doubao 电竞教练](https://developer.volcengine.com/articles/7641552307030949942)：作者实践中的专项分析、分片与分层复盘。
- [[3] 腾讯 SPARK 2026 发布会](https://www.tencent.com/zh-hk/tencent-games-spotlights-future-player-experiences-with-45-major-updates-at-spark-2026/)：腾讯游戏年度发布会背景。
- [[4] 流放之路降临主创采访](https://news.17173.com/content/08232025/070005359.shtml)：蛋蛋君的初期体验与探索边界；功能细节另参见发布会报道。
- [[5] Xbox Gaming Copilot Game Bar](https://news.xbox.com/en-us/2025/08/06/gaming-copilot-beta-begins-rolling-out-to-xbox-insiders-on-game-bar-today/)：截图辅助和玩家设置。
- [[6] NVIDIA 访谈 PUBG Ally](https://developer.nvidia.com/blog/how-krafton-built-pubg-ally-a-co-playable-character-powered-by-nvidia-ace/)：实时协作、行为树、小模型与评测。
- [[7] NVIDIA Game Agent SDK GitHub](https://github.com/NVIDIA/game-agent-sdk)：Agent、Chat 与 RAG 接口开源实现。
- [[8] Ubisoft Teammates 官方介绍](https://news.ubisoft.com/en-us/article/3mWlITIuWuu0MoVuR6o8ps/ubisoft-reveals-teammates-an-ai-experiment-to-change-the-game)：语音助手与可行动 NPC 原型。
- [[9] Razer Project AVA 官方介绍](https://www.razer.com/newsroom/product-news/project-ava)：PC Vision 与电竞教练概念。
- [[10] GameplayQA ACL 2026](https://aclanthology.org/2026.acl-long.1585/)：3D 多主体视频理解误差与评测。
- [[11] Video-Arena 2026 预印本](https://arxiv.org/abs/2610.14158)：事件、状态变化和追踪评测。
- [[12] jcc-replay-analyst GitHub](https://github.com/HuanNan520/jcc-replay-analyst/)：社区原型：OCR、CV、VLM 观察层与复盘链路。
- [[13] NVIDIA ACE SDK 技术说明](https://developer.nvidia.com/blog/build-on-device-ai-companions-with-the-nvidia-ace-game-agent-sdk-and-unreal-engine-5-plugins/)：游戏状态、RAG 与端侧集成参考。
- [[14] 腾讯游戏 AI 应用进展报道](https://www.cgames.com/contents/2/11617.html)：蛋蛋君的 BD 推荐与市集装备分析。
- [[15] 腾讯技术工程 Skill 实战手册](https://zhuanlan.zhihu.com/p/2045872710375428908)：Description、单一职责、示例、检查点与工程化评测。

## 新增 Biped Demo 的一手来源与实验边界

为了把核心 Skill 应用到一个资料范围可控的目标游戏，本次选择《只只大冒险 / Biped》第一部。选题依据是可收窄的操作与合作机制，不是对全网资料总量的统计。

- [[16] NExT Studios 官方介绍](https://www.nextstudios.com/next/index_en.html)：核实腾讯工作室归属与 Biped 产品关系。
- [[17] Biped Steam 产品页](https://store.steampowered.com/app/1071870/Biped/?l=schinese)：单人及双人模式、双摇杆、创意工坊，以及系统需求附注中的本地双人输入设备组合。本 Demo 不收录价格或评分。
- [[18] 开发者 Biped 设计复盘](https://www.gamedeveloper.com/design/postmortem-a-rationally-designed-funny-game---the-making-of-biped-in-hindsight)：两条腿的操作原理，以及沟通、制定计划与协同行动。只采用与公开产品说明相互印证的原则，不把历史原型当作当前规则。
- [[19] Codex 非交互模式官方文档](https://learn.chatgpt.com/docs/non-interactive-mode)：本地 CLI 登录复用、结构化输出与 JSONL 事件的实现依据。

以上页面于 2026 年 10 月 29 日核对。知识卡是必要信息的转述，保留来源、定位、适用范围与核对日期。`seed-v1 → enriched-v2` 表示知识补录，没有伪造游戏补丁变更；真实游戏 build 与用户当局状态均未核实。

模型显式请求别名为 `gpt-6.1-sol`。Python harness 固定执行上下文获取和关键词检索，再将同一批资料交给普通 RAG 与显式加载核心 Skill 的两组模型调用。该实验没有测试自动发现 Skill、模型自主工具选择、视觉感知或真实游戏操作。用例和评分规则在运行前记录哈希；它们是开发者编写的小样本，不是独立盲测或专家质量验收。

自动评分同时检查决策和接口字段。原因码不同会影响通过数，因此不能把差异称为答案准确率提升。运行参数、逐条输出与本地管理演练均见 [Demo 说明](../demos/biped/README.md)；审批身份是明确标注的本地演练 fixture。
