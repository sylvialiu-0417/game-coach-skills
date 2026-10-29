from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
skill = (root / 'SKILL.md').read_text(encoding='utf-8')
assert skill.startswith('---\n')
head = skill.split('---', 2)[1]
assert re.search(r'^name: game-coach-perception$', head, re.M)
assert re.search(r'^description: .+', head, re.M)
assert re.search(r'^\s+version: "2\.1"$', head, re.M)
for md in root.rglob('*.md'):
    for rel in re.findall(r'\]\(([^)#]+)(?:#[^)]+)?\)', md.read_text(encoding='utf-8')):
        if '://' not in rel:
            assert (md.parent / rel).exists(), f'missing link {md}: {rel}'

schema = json.loads((root / 'schemas/observation-bundle.schema.json').read_text(encoding='utf-8'))
assert schema['$schema'].endswith('2020-12/schema')
items = json.loads((root / 'examples/observation-bundles.json').read_text(encoding='utf-8'))
assert len(items) >= 3 and {'official_api', 'screenshot', 'audio'} <= {x['source_type'] for x in items}
for bundle in items:
    assert set(schema['required']) <= set(bundle)
    assert set(bundle) <= set(schema['properties'])
    assert bundle['schema_version'] == '1.0'
    assert bundle['status'] in schema['properties']['status']['enum']
    item_schema = schema['properties']['observations']['items']
    for obs in bundle['observations']:
        assert set(item_schema['required']) <= set(obs)
        assert set(obs) <= set(item_schema['properties'])
        assert 0 <= obs['t0_ms'] <= obs['t1_ms']
        assert obs['epistemic_status'] in item_schema['properties']['epistemic_status']['enum']
        assert obs['visibility'] in item_schema['properties']['visibility']['enum']
        assert obs['evidence_refs'], 'observations require evidence'
        for ref in obs['evidence_refs']:
            ref_schema = item_schema['properties']['evidence_refs']['items']
            assert set(ref_schema['required']) <= set(ref)
            assert set(ref) <= set(ref_schema['properties'])
    if bundle['source_type'] == 'official_api':
        assert bundle['model_version'] == 'none'

def read_jsonl(path):
    return [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]

cases = read_jsonl(root / 'evals/cases.jsonl')
triggers = read_jsonl(root / 'evals/trigger-cases.jsonl')
assert len(cases) >= 10 and len({x['id'] for x in cases}) == len(cases)
assert len(triggers) >= 15 and len({x['id'] for x in triggers}) == len(triggers)
assert {x['expected'] for x in triggers} == {'trigger', 'skip', 'boundary'}
print(f'Static validation passed: {len(items)} observation bundles, {len(cases)} perception cases, {len(triggers)} trigger cases.')
print('Real perception accuracy and latency require target game data and model runs.')
