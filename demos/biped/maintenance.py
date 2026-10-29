#!/usr/bin/env python3
"""Demonstrate a local release state machine. This is not a production approval service."""
import argparse
import copy
from pathlib import Path
from run import ROOT, read, write, digest, now


class LocalRelease:
    def __init__(self):
        self.status = 'proposed'
        self.active = 'seed-v1'
        self.events = []

    def record(self, action, accepted, detail):
        event = {'at': now(), 'action': action, 'accepted': accepted,
                 'status': self.status, 'active_snapshot': self.active, 'detail': detail}
        self.events.append(event)
        return accepted

    def review(self, approval):
        valid = self.status == 'proposed' and approval.get('kind') == 'local_demo_fixture'
        if valid:
            self.status = 'reviewed'
        return self.record('review', valid, approval)

    def evaluate(self, report):
        expected_n = len(read(ROOT / 'data/cases.json'))
        valid = self.status == 'reviewed' and report['n'] == expected_n and report['passed'] == expected_n
        if valid:
            self.status = 'evaluated'
        return self.record('evaluate', valid, {'n': report['n'], 'passed': report['passed']})

    def publish(self):
        valid = self.status == 'evaluated'
        if valid:
            self.active, self.status = 'enriched-v2', 'published'
        return self.record('publish', valid, '只切换本地演练快照；不会发布游戏知识生产库。')

    def rollback(self):
        valid = self.status == 'published'
        if valid:
            self.active, self.status = 'seed-v1', 'rolled_back'
        return self.record('rollback', valid, '在隔离副本演练回滚，不修改主演练结果。')


def build(run_id):
    run_dir = ROOT / 'runs' / run_id
    summary = read(run_dir / 'summary.json')
    catalog = read(ROOT / 'data/knowledge.json')
    added = [x for x in catalog['snapshots']['enriched-v2'] if x not in catalog['snapshots']['seed-v1']]
    assert added == ['K-LOCAL-INPUT']
    source = next(s for s in read(ROOT/'data/sources.json') if s['source_id'] == 'S-STEAM')
    release = LocalRelease()
    release.record('propose', True, {
        'trigger': 'B06-before 出现知识缺口：本地输入设备组合',
        'change_type': 'verified_source_enrichment', 'added_evidence': added,
        'affected_cases': ['B06-before', 'B06-after'],
        'source': source['url'], 'locator': '系统需求 → 附注事项',
        'scope': '补入已公开的说明，不是假设游戏发生了版本更新。',
    })
    assert not release.publish(), 'Publishing an unreviewed candidate must fail'
    assert release.review({
        'kind': 'local_demo_fixture', 'actor': 'demo-maintainer-fixture',
        'source_check': '本次助手核对公开原文；没有独立游戏专家复核。',
        'permission_scope': 'local_demo_only',
    })
    assert not release.publish(), 'Publishing before evaluation must fail'
    approved = release.evaluate(summary['arms']['skill'])
    published = release.publish() if approved else False
    rollback_drill = copy.deepcopy(release)
    rollback_ok = rollback_drill.rollback() if published else False
    result = {
        'run_id': run_id, 'generated_at': now(), 'kind': 'local_management_exercise',
        'source_of_change': 'verified public documentation enrichment',
        'approval_is_simulated': True, 'production_publish': False,
        'snapshot_evaluation': '两个快照预先作为离线评测 fixture；只有本地发布演练通过后才更新演练 active 指针。',
        'state': release.status, 'active_snapshot': release.active,
        'gate_result': 'passed' if published else 'blocked', 'events': release.events,
        'rollback_drill': {'passed': rollback_ok, 'active_snapshot': rollback_drill.active},
        'deterministic_gate_checks': {'block_unreviewed': True, 'block_unevaluated': True},
        'evaluation_report_sha256': digest(run_dir/'summary.json'),
        'missing_for_production': ['真实审批身份与权限服务', '目标游戏专家复核', '独立测试集与重复运行',
                                   '真实游戏版本与状态接口', '线上抽检和反馈闭环'],
    }
    write(run_dir / 'management.json', result)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('run_id')
    result = build(p.parse_args().run_id)
    print(result['gate_result'] + '; active=' + result['active_snapshot'])
