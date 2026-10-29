# 接入契约

字段为语义契约，实际传输可用 JSON、函数调用或 MCP 工具。示例 JSON Schema 位于 `schemas/`；并非声称已接入某游戏服务。

## 请求

`coach_request` 必含 `request_id, game_id, ruleset_id, mode_id, coach_id, task, surface, user_text, consent`。可选 `state_ref, observation_ref, history_ref, locale, trigger_event`。`game_id/ruleset_id/coach_id/consent` 必须由可信宿主注入并由服务端按会话校验，不允许玩家文本覆盖。`consent=false` 时仍可回答公开规则，但不得读取个人状态或历史记录。`observation_ref` 指向可追溯的观察包，不把原始截图塞进知识条目。

## 知识证据

`search_knowledge` 接收游戏、规则版本、模式、实体、知识类型和查询；返回 [证据 Schema](../schemas/knowledge-evidence.schema.json) 中的 `evidence_id, game_id, content, source_ref, source_tier, ruleset_scope, mode_scope, status, valid_from/to, applicability, retrieved_at`。检索适配器必须保证游戏隔离和已发布过滤，并保留原库条目 ID。缺少当前规则版本时不得把可能变化的规则当作当前事实；有冲突返回 `conflict`，不能静默吞掉。

## 状态与输出

`get_state` 返回 [状态 Schema](../schemas/game-state.schema.json) 中的 `observed_at, observable_fields, values, authority_scope`；也可返回game-coach-perception 的 `ObservationBundle` 引用。没有字段不等于其值为否，模型推断字段不等于直接观察。缺少同意或权限时不读取个人状态与历史记录。结果输出 `game_id, coach_id, decision, player_text, evidence_ids, missing_conditions, reason_code, versions, trace_id`；实际给出复盘诊断时，`diagnostics` 中逐项附 `observation_ids` 与 `rubric_ids`；主动提示另含 `display_ttl_ms`。不许把数值置信度当成证据充分性的替代。

## 维护端

管理工具接收 `change_id, game_id, affected_modes, old/new_ruleset, source_refs, affected_evidence_ids, evaluation_report, approver`；执行端检查权限与状态机：`proposed → reviewed → evaluated → published/rolled_back`。玩家反馈只可创建 `proposed` 候选，不可填 `approver` 或直接发布。

## 错误语义

`unsupported_game`：无适配器；`unsupported_capability`：教练未开放此任务；`version_unknown`：当前规则版本不明；`stale_evidence`：仅找到旧版资料；`no_evidence`：缺可靠知识；`conflicting_evidence`：当前版来源冲突；`state_missing` / `state_stale`：无法验证策略前提；`permission_denied`：工具无权限；`deadline_exceeded`：超过提示时限。Agent 应按原因码回退，不把工具失败伪装成已验证回答。
