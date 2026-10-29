from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
skill = (root / 'SKILL.md').read_text(encoding='utf-8')
assert skill.startswith('---\n')
head = skill.split('---', 2)[1]
assert re.search(r'^name: game-coach-annotation$', head, re.M)
assert re.search(r'^description: .+', head, re.M)
assert re.search(r'^\s+version: "1\.0"$', head, re.M)
assert len(skill.splitlines()) < 500
for md in root.rglob('*.md'):
    for rel in re.findall(r'\]\(([^)#]+)(?:#[^)]+)?\)', md.read_text(encoding='utf-8')):
        if '://' not in rel:
            assert (md.parent / rel).exists(), f'missing link {md}: {rel}'

schema = json.loads((root / 'schemas/annotation-case.schema.json').read_text(encoding='utf-8'))
assert schema['$schema'].endswith('2020-12/schema')
examples = json.loads((root / 'examples/annotation-cases.json').read_text(encoding='utf-8'))
assert len(examples) >= 3
ids = set()
match_splits = {}
player_splits = {}
for case in examples:
    assert set(schema['required']) <= set(case)
    assert set(case) <= set(schema['properties'])
    assert case['schema_version'] == '1.0'
    assert case['case_id'] not in ids
    ids.add(case['case_id'])
    assert case['t0_ms'] <= case['t1_ms']
    observations = {x['observation_id'] for x in case['objective_labels']}
    assert len(observations) == len(case['objective_labels'])
    for label in case['objective_labels']:
        assert set(schema['properties']['objective_labels']['items']['required']) <= set(label)
        assert case['t0_ms'] <= label['t0_ms'] <= label['t1_ms'] <= case['t1_ms']
        if case['review_status'] == 'approved':
            assert label['verification'] == 'expert_verified'
    for judge in case['expert_judgments']:
        assert set(schema['properties']['expert_judgments']['items']['required']) <= set(judge)
        assert set(judge['observation_ids']) <= observations
        assert judge['reviewer_id'] in case['reviewers']
    if case['review_status'] == 'approved':
        assert len(set(case['reviewers'])) >= 2, 'approved cases need independent review'
        assert all(j['judgment_status'] != 'disputed' for j in case['expert_judgments'])
    if any(j['judgment_status'] == 'disputed' for j in case['expert_judgments']):
        assert case['split'] == 'none', 'disputed cases cannot enter train/dev/test'
    if case['split'] != 'none':
        match_splits.setdefault(case['match_id'], set()).add(case['split'])
        player_splits.setdefault(case['player_id_hash'], set()).add(case['split'])
assert all(len(v) == 1 for v in match_splits.values()), 'match leakage across splits'
assert all(len(v) == 1 for v in player_splits.values()), 'player leakage across splits'

def jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]

cases = jsonl(root / 'evals/cases.jsonl')
triggers = jsonl(root / 'evals/trigger-cases.jsonl')
assert len(cases) >= 10 and len({x['id'] for x in cases}) == len(cases)
assert len(triggers) >= 20 and len({x['id'] for x in triggers}) == len(triggers)
assert {x['expected'] for x in triggers} == {'trigger', 'skip', 'boundary'}
print(f'Static validation passed: {len(examples)} annotation examples, {len(cases)} quality cases, {len(triggers)} trigger cases.')
print('Expert agreement and model quality require real reviewed media and human adjudication.')
