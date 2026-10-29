from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
assert skill.startswith("---\n"), "missing YAML frontmatter"
head = skill.split("---", 2)[1]
assert re.search(r"^name: game-coach-kb$", head, re.M), "invalid skill name"
assert re.search(r"^description: .+", head, re.M), "missing description"
assert re.search(r'^\s+version: "6\.1"$', head, re.M), "missing version metadata"
assert "王者" not in skill and "英雄" not in skill, "game-specific vocabulary in core"
for md in ROOT.rglob("*.md"):
    for rel in re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", md.read_text(encoding="utf-8")):
        if not rel.startswith("http"):
            assert (md.parent / rel).exists(), f"missing reference: {md}: {rel}"

for path in (ROOT / "schemas").glob("*.json"):
    obj = json.loads(path.read_text(encoding="utf-8"))
    assert obj.get("$schema") and obj.get("type") == "object", path

adapters = [json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "examples").glob("*.adapter.json")]
assert len(adapters) >= 2 and len({a["game_type"] for a in adapters}) >= 2
assert all(a["game_id"] and a["adapter_version"] for a in adapters)
coaches = json.loads((ROOT / "examples/coach-configs.json").read_text(encoding="utf-8"))
assert all(c["game_id"] in {a["game_id"] for a in adapters} for c in coaches)
assert all(set(c["tasks"]) <= {"explain", "recommend", "live_tip", "review", "training_plan", "feedback"} for c in coaches)
traces = json.loads((ROOT / "examples/paired-traces.json").read_text(encoding="utf-8"))
request_schema = json.loads((ROOT / "schemas/coach-request.schema.json").read_text(encoding="utf-8"))
response_schema = json.loads((ROOT / "schemas/coach-response.schema.json").read_text(encoding="utf-8"))
evidence_schema = json.loads((ROOT / "schemas/knowledge-evidence.schema.json").read_text(encoding="utf-8"))
state_schema = json.loads((ROOT / "schemas/game-state.schema.json").read_text(encoding="utf-8"))

def validate_example(obj, schema, label):
    assert isinstance(obj, dict), label
    assert set(schema["required"]) <= set(obj), f"missing {label} fields"
    assert set(obj) <= set(schema["properties"]), f"unexpected {label} fields"
    for field, value in obj.items():
        descriptor = schema["properties"][field]
        if "enum" in descriptor:
            assert value in descriptor["enum"], f"bad {label}.{field}"
        allowed = descriptor.get("type")
        if allowed is not None:
            allowed = [allowed] if isinstance(allowed, str) else allowed
            actual = "null" if value is None else ("boolean" if isinstance(value, bool) else "integer" if isinstance(value, int) else "string" if isinstance(value, str) else "array" if isinstance(value, list) else "object" if isinstance(value, dict) else "unknown")
            assert actual in allowed, f"bad type {label}.{field}"
        if isinstance(value, str) and "minLength" in descriptor:
            assert len(value) >= descriptor["minLength"], f"empty {label}.{field}"
        if isinstance(value, dict) and "required" in descriptor:
            validate_example(value, descriptor, f"{label}.{field}")

assert {t["request"]["game_id"] for t in traces} == {a["game_id"] for a in adapters}
for trace in traces:
    for key, schema in (("request", request_schema), ("response", response_schema), ("retrieved_evidence", evidence_schema), ("state", state_schema)):
        validate_example(trace[key], schema, key)
    assert trace["request"]["game_id"] in {a["game_id"] for a in adapters}
    assert trace["request"]["coach_id"] in {c["coach_id"] for c in coaches}
    assert trace["response"]["game_id"] == trace["request"]["game_id"] == trace["retrieved_evidence"]["game_id"]
    assert trace["response"]["coach_id"] == trace["request"]["coach_id"]
    assert trace["retrieved_evidence"]["status"] == "published"
    assert trace["retrieved_evidence"]["ruleset_scope"] == trace["request"]["ruleset_id"]
    assert trace["request"]["mode_id"] in trace["retrieved_evidence"]["mode_scope"]
    assert trace["response"]["evidence_ids"] == [trace["retrieved_evidence"]["evidence_id"]]

cases = [json.loads(line) for line in (ROOT / "evals/cases.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(cases) >= 12 and len({c["id"] for c in cases}) == len(cases)
assert {c["game_id"] for c in cases} == {a["game_id"] for a in adapters}
assert {c["task"] for c in cases} >= {"explain", "recommend", "live_tip", "review", "onboard", "maintenance"}
triggers = [json.loads(line) for line in (ROOT / "evals/trigger-cases.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(triggers) >= 20 and len({t["id"] for t in triggers}) == len(triggers)
assert {t["expected"] for t in triggers} == {"trigger", "skip", "boundary"}
print(f"Static validation passed: {len(adapters)} game types, {len(coaches)} coach configs, {len(traces)} paired traces, {len(cases)} runtime cases, {len(triggers)} trigger cases.")
print("Behavioral results require an actual model, knowledge base, tools and expert review.")
