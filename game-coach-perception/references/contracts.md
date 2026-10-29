# 观察包契约

输入需可信 `game_id/ruleset_id/session_id/viewpoint_id`、来源及授权范围。输出使用 [Schema](../schemas/observation-bundle.schema.json)，`status` 为 `usable/partial/unusable`。每项观察记录 `observation_id, kind, value, t0_ms, t1_ms, epistemic_status, visibility, evidence_refs`；另保留原媒体或 API 引用、时钟偏移、缺失字段、冲突和感知版本。

`observed` 表示证据中直接可见或 API 直接给出；`inferred` 表示依赖模型推断；`unknown` 表示无法确认。三者不可以只凭模型自报分数转换。游戏game-coach-kb 可以利用 `inferred` 提出条件式解释，不能用它满足要求直接观察的高风险战术前提。

状态字段的语义由游戏适配器定义。对同一字段，`missing` 表示没有观察，`false` 表示观察到否，二者不可互换。观察包不包含“应该怎么打”“失误类型”这类教练判断；这些必须用知识判据与观察共同推导。
