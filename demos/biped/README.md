# Biped 教练知识库 Demo

把**游戏 AI 教练知识库管理与应用 Skill**应用到腾讯 NExT Studios 的《只只大冒险 / Biped》第一部，验证一个有公开来源、范围可控的知识应用流程。游戏归属见 [NExT 官方介绍](https://www.nextstudios.com/next/index_en.html)。选择它是因为本次可把机制和资料范围收窄到操作与合作入门，没有测量全网资料总量。

## 可以看到什么

- 依据已发布知识回答操作、模式和一般合作练习问题。
- 机关与站位未知时先澄清；未开放实时提示时静默；无可靠证据时回退。
- 同一问题在补入官方设备说明前后的两次真实模型输出。
- 未审核、未评测时阻止本地发布，以及隔离副本的回滚演练。
- 同模型、同检索、同问题的普通 RAG 与加载 Skill 两组记录。

页面是**真实运行记录的交互回放**，不接收任意新问题，不在浏览器调用模型。未连接游戏、屏幕、游戏状态 API 或操作控制。本次只应用核心知识 Skill，未调用游戏观察提取 Skill 和专家复盘标注 Skill。

## 模型与 harness 分别是什么

| 项目 | 本次实现 |
| --- | --- |
| 模型 | 显式请求 `gpt-6.1-sol`；CLI 未返回不可变后端快照 ID，不把别名写成固定模型版本 |
| 认证 | 用户本机已有 ChatGPT 登录；没有复制密钥或认证文件 |
| 模型运行时 | Codex CLI；精确版本写入每次 `manifest.json` |
| harness | `biped-rag-harness-1.0`，Python 标准库编排上下文、关键词检索、Skill 加载、调用、记录与检查 |
| Skill 加载 | Skill 组显式注入原始 `SKILL.md`、`runtime.md`、`contracts.md`，保留文件 SHA-256 |
| 基线 | 相同宿主、知识、请求和 JSON 输出结构，不注入上述三份 Skill 文件；版本链中标为 `not_loaded` |
| 工具 | 宿主固定执行 `get_context` 和 `search_knowledge`；没有测模型自主选工具 |
| 检索 | 按游戏、公开说明适用范围、模式、发布状态和快照先过滤，再做关键词 top-3；无 embedding 模型 |
| 推理 | `low`；临时空目录、只读模式；关闭模型侧 shell、web、apps、plugins、multi_agent 和 hooks |
| 输出与日志 | 原始最终 JSON、公开事件、宿主轨迹、耗时和 token 用量；脚本不重写答案、不补引用、不重试挑结果 |

Codex CLI 是本次本地实验的模型调用方式，不等于面向玩家的生产服务架构。参见 [非交互模式官方说明](https://learn.chatgpt.com/docs/non-interactive-mode)。

保存的 prompt 文件是 harness 显式传入的文本。Codex CLI 自带的系统提示仍然存在，未完整导出；因此这里不声称记录了服务端收到的全部上下文。两组使用同一个 CLI 环境。

## 知识与版本边界

从“部分种子知识”开始：`seed-v1` 有 4 张知识卡；`enriched-v2` 新增 `K-LOCAL-INPUT`，来源是 [Steam 产品页](https://store.steampowered.com/app/1071870/Biped/?l=schinese)系统需求中的设备说明。补录是**知识更新**，没有假设游戏发布新补丁。

`ruleset_id=biped-steam-public-docs` 表示本次核对的第一部 Steam PC 公开说明范围，**不是游戏补丁号**。未读取任何用户安装版本。不能把本次回答外推为某个最新 build 的精确规则。来源、定位、日期和适用条件见 [sources.json](data/sources.json) 与 [knowledge.json](data/knowledge.json)。

资料补强主要处理两类问题：种子库没有设备组合时，正确动作是承认证据不足；找到并核对官方说明后，再形成新卡和独立快照。只有知识变了，游戏适配器与规则范围没有变化。

管理状态机在本地演练 `proposed → reviewed → evaluated → published`。审批使用明确标注的演练 fixture，非真实企业审批或独立专家审定。两个快照预先作为离线评测 fixture，不代表可以绕过生产审核；程序只在演练门槛通过后切换本地 active 指针。

## 如何复现

需要 Python 3 和可正常登录、支持所用参数的 Codex CLI。自行运行会使用运行者账号的模型额度。仓库没有认证文件，也没有配置任何公共推理服务。

先看保存的运行结果，无需登录或模型调用：

```bash
python3 demos/biped/verify.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

浏览器打开 `http://127.0.0.1:8765/demo/`，或直接打开 `docs/demo/index.html`。

重新调用模型并生成独立记录：

```bash
codex login
python3 demos/biped/run.py run --model gpt-6.1-sol --run-id my-biped-run
python3 demos/biped/maintenance.py my-biped-run
python3 demos/biped/build_demo.py my-biped-run
```

用相同核心 harness 实际回答一个新问题：

```bash
python3 demos/biped/ask.py --question '我们配合总失误，先怎么练？'
```

单次问答会调用模型，记录默认保存在不上传的 `.local-runs/`，没有预置评分；不会改写已发布的评测结果。

若 `codex` 不在 PATH，可通过 `CODEX_BIN` 指定可执行文件路径。模型若不在运行者账号可用列表中，请显式换成可用模型并在新运行记录里保留实际名称，不替换历史结果。

新增问题时修改 `data/cases.json`；正式评测应先冻结未参与调试的数据与评分标准，再另起一次 run。本 Demo 的 11 条是开发者编写的小样本，不是独立盲测。脚本固定记录用例、评分规则、知识、适配器、Skill 与 harness 的哈希。

## 如何读结果

`runs/<run_id>/manifest.json` 记录运行配置；每个分组和问题目录中保留输入、注入后的 prompt、检索轨迹、最终回答、耗时、用量和逐条检查。`summary.json` 为固定规则评分，`management.json` 为本地管理演练。期望输出没有注入模型。

自动检查的是决策、必需引用、缺失条件、标准原因码、版本链和意外工具调用。**原因码不同也会导致未通过，因此通过数不是回答正确率。** 对比时需看失败原因：两组可能都选择澄清，但基线没有按 Skill 的原因码词表输出。这种差异说明接口规范程度，不足以证明回答更安全或更有用。

公开事件只包含最终回答和用量；内部推理、完整传输 stderr 留在已忽略的 `.local-runs/`，不上传。CLI 耗时含启动和网络开销，不是实时教练延迟；没有把账号 token 统计换算成 API 费用。

## 尚待验证

这次没有测 Skill 自动触发、检索召回率、真实玩家体验、关卡攻略的专家质量、视觉识别或线上发布权限。下一步应建立独立样本和专家盲评、重复运行、分别测检索与回答，再接入获授权状态，按层验收观察与教练决策。
