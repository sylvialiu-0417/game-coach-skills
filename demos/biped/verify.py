#!/usr/bin/env python3
"""Verify reproducibility and interface invariants without making model calls."""
import copy
import json
from run import ROOT, REPO, read, digest, prepare, prompt_for, schema, grade


def normalize(payload):
    payload = copy.deepcopy(payload)
    payload['trusted_host_context']['versions']['skill'] = 'normalized'
    for card in payload['retrieval_result']['evidence']:
        card['retrieved_at'] = 'normalized'
    return payload


def main():
    run_id = read(ROOT / 'runs/latest.json')['run_id']
    path = ROOT / 'runs' / run_id
    manifest = read(path / 'manifest.json')
    assert manifest.get('completed_at'), 'Run is incomplete'
    for relative, expected in manifest['frozen_sha256'].items():
        assert digest(REPO / relative) == expected, 'Frozen input changed: ' + relative
    assert read(path/'response.schema.json') == schema()
    cases = read(ROOT / 'data/cases.json')
    rubric = read(ROOT / 'data/rubric.json')['cases']
    cards = read(ROOT / 'data/knowledge.json')['records']
    source_ids = {s['source_id'] for s in read(ROOT/'data/sources.json')}
    assert all(c['source_ref'] in source_ids for c in cards if not c.get('test_fixture'))
    for case in cases:
        inputs = []
        for arm in manifest['arms']:
            folder = path / arm / case['case_id']
            payload, output = read(folder/'input.json'), read(folder/'output.json')
            execution = read(folder/'execution.json')
            assert set(output) == set(schema()['required'])
            assert execution['status'] == 'completed' and execution['exit_code'] == 0
            assert execution['prompt_sha256'] == digest(folder/'prompt.txt')
            assert (folder/'prompt.txt').read_text() == prompt_for(payload, arm)
            assert 'required_evidence' not in (folder/'prompt.txt').read_text()
            assert read(folder/'grade.json') == grade(case, output, execution, payload, rubric[case['case_id']])
            for ev in payload['retrieval_result']['evidence']:
                assert ev['game_id'] == payload['trusted_host_context']['game_id']
                assert ev['status'] == 'published'
                assert not ev['evidence_id'].startswith('FIXTURE')
            events = [json.loads(x) for x in (folder/'events.public.jsonl').read_text().splitlines() if x]
            assert all(e['type'] in ('agent_message','turn.completed') for e in events)
            assert json.loads([e['text'] for e in events if e['type']=='agent_message'][-1]) == output
            assert [e['usage'] for e in events if e['type']=='turn.completed'][-1] == execution['usage']
            inputs.append(normalize(payload))
        assert inputs[0] == inputs[1], 'Pair has different tools/knowledge/context: ' + case['case_id']
    unknown = {'case_id':'filter-check','snapshot':'seed-v1','task':'explain','game_id':'unknown', 'user_text':'操作'}
    assert prepare(unknown, manifest['model_requested'])[0]['retrieval_result']['evidence'] == []
    management = read(path/'management.json')
    assert management['approval_is_simulated'] is True and management['production_publish'] is False
    premature = [e for e in management['events'] if e['action']=='publish' and not e['accepted']]
    assert len(premature) == 2 and {e['status'] for e in premature} == {'proposed','reviewed'}
    if management['gate_result'] == 'passed':
        assert management['active_snapshot'] == 'enriched-v2' and management['rollback_drill']['passed']
    print('PASS: frozen inputs, paired contexts, provenance filters, original outputs, public logs and local release gates')
    print('Verified ' + str(len(cases)*len(manifest['arms'])) + ' real saved model responses; no model calls were made.')


if __name__ == '__main__':
    main()
