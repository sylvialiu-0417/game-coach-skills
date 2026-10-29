# Game Coach Skills

**方案核心是游戏 AI 教练知识库的管理与应用 Skill**，游戏观察提取和专家复盘标注作为配套能力。

本项目围绕已有游戏知识库的接入、来源治理、版本更新、审核发布、检索应用和持续评测展开设计。配套 Skill 分别提供动态观察输入和专家知识生产支持。目标游戏需要分别补齐知识、术语、状态来源、适配配置和评测；“流程可复用”尚不代表已在多款真实游戏验证。交付包括三个可独立加载的 `SKILL.md`、结构化契约、虚构游戏示例与校验脚本，并新增《只只大冒险 / Biped》公开知识的离线 Demo 与真实模型运行记录；尚未连接游戏状态或画面、训练模型或取得线上效果指标。

## 从这里开始

| 入口 | 解决的问题 |
| --- | --- |
| [游戏 AI 教练知识库管理与应用 Skill](game-coach-kb/SKILL.md) | 核心：管理知识来源、版本与更新，支持检索、问答、复盘及应用评测 |
| [游戏观察提取 Skill](game-coach-perception/SKILL.md) | 如何将获授权的 API、画面和音频整理为带时间和出处的观察 |
| [专家复盘标注 Skill](game-coach-annotation/SKILL.md) | 如何把事实标签与专家判断分开审定，制作训练、知识候选及评测资产 |
| [Biped Demo 与复现方法](demos/biped/README.md) | 查看真实模型回答、缺信息回退、知识补录与本地发布演练；记录模型及 harness |
| [Word 调研与方案报告](docs/game-coach-skills-report.docx) | 公开产品调研、设计边界、专家生产流程与评测方法 |

## 实际运行的 Demo

[打开 Biped Demo 回放](https://sylvialiu-0417.github.io/game-coach-skills/demo/) · [查看运行记录](demos/biped/runs/) · [本地复现说明](demos/biped/README.md)

以腾讯 NExT Studios 的《只只大冒险》第一部为例，从 4 张种子知识卡开始，补入 1 张官方设备说明卡。使用 `gpt-6.1-sol`、Codex CLI 和 Python RAG harness，配对运行普通 RAG 与加载核心 Skill 两组。页面回放的是保存的真实输出，不提供在线推理或游戏画面识别。

自动检查包含标准原因码和版本链，通过数不等于答案准确率；发布审批为本地演练 fixture，不能当作生产发布权限。精确配置、逐条结果与限制见 Demo 页面和运行清单。

## AI教练如何使用知识

![线上教练调用流程](docs/figures/online-coaching-flow.png)

`game-coach-perception` 输出的是观察；`game-coach-kb` 还要结合已发布知识和专业判据验证建议是否适用。缺少关键状态时，系统澄清、给条件式建议或停止主动提示。每个游戏使用自己的实体、模式、状态字段与判据，核心流程不依赖王者荣耀术语。

## 专家怎样补强AI教练

![专家复盘标注与数据分流](docs/figures/expert-annotation-flow.png)

`game-coach-annotation` 组织离线复盘标注，机器预标注保留草稿状态。专家先核对事实，再记录判断依据、适用条件、例外和分歧；拟发布判据及参考评测答案须独立复核。通过审核的标注也须按用途分流，模型训练与知识发布分别执行，独立测试数据保持冻结。

## 文件与契约

```text
game-coach-kb/          核心：知识库管理、检索应用、版本更新与评测
game-coach-perception/  多模态观察、时间定位、可见性与不确定性
game-coach-annotation/  事实核对、专家判断、审定与数据集隔离
docs/                  架构、公开调研、流程图与 Word 报告
demos/biped/           真实游戏公开知识、Codex 调用 harness、保存的运行与评测记录
validate_bundle.py     三包结构及共用观察契约检查
```

共用接口是 [`ObservationBundle`](game-coach-perception/schemas/observation-bundle.schema.json)，专家记录使用 [`AnnotationCase`](game-coach-annotation/schemas/annotation-case.schema.json)。这些 Schema 描述数据格式；权限、展示、训练和发布仍需宿主服务实现。

## 验证方法与当前结果

需要 Python 3，无第三方依赖：

```bash
python3 validate_bundle.py
```

原有 45 条执行或质量场景、64 条触发场景仍是模拟测试素材，不是目标模型效果成绩。新增 Biped Demo 单独保留真实调用与小样本自动检查；可运行 `python3 demos/biped/verify.py` 核对冻结输入、配对上下文、来源过滤、输出和本地发布门槛。真实验收仍需独立样本、专家复核、感知准确性、教练决策与授权对局的端到端评测。

可以先在 [架构说明](docs/architecture.md) 中看两条流程的交接，再按 [研究与参考资料](docs/research.md) 核对产品启发和证据等级。
