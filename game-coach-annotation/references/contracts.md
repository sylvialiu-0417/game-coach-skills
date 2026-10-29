# 标注记录契约

[AnnotationCase Schema](../schemas/annotation-case.schema.json) 规定每条记录的身份、来源、版本、视角、时间段、事实标签、专家判断、复核状态和数据集用途。`t0_ms/t1_ms` 使用本场会话的全局时间，不使用切片局部时间；媒体引用必须可回到原录像或事件。公开资料与内部训练素材应保留不同的使用许可。

**事实标签**只描述可观察对象、数值、行为或事件，字段含 `observation_id, value, evidence_ref, t0_ms/t1_ms, visibility, verification`。模型预标注只是草稿；人工确认后才能作为感知参考标签。

**专家判断**是对事实与目标的解释，字段含 `claim, rationale, observation_ids, rubric_ref, applicability, exceptions, judgment_status`。`rubric_ref` 指向当前版本的判据；尚无判据时只能提出候选，不伪造已有引用。`insufficient_evidence`、`disputed` 和 `supported` 是不同状态。

**流转状态**为 `draft → reviewed → adjudicated/approved → retired`。`approved` 只表示这条标注完成审定，不等于知识已发布或模型已训练。`split` 是 `train/dev/test/none`；同一对局及同一玩家的高度重叠片段不得跨集合。发布与训练任务由独立服务执行。
