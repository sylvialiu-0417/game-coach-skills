#!/usr/bin/env python3
"""Ask one new question through the same core harness. Saves local, ungraded outputs."""
import argparse
from datetime import datetime, timezone
import subprocess
from run import ROOT, REPO, HARNESS_VERSION, SKILL_FILES, call_model, codex_path, digest, now, read, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--question', required=True)
    parser.add_argument('--snapshot', choices=['seed-v1','enriched-v2'], default='enriched-v2')
    parser.add_argument('--task', choices=['explain','recommend'], default='explain')
    parser.add_argument('--model', default='gpt-6.1-sol')
    args = parser.parse_args()
    cli = codex_path()
    stamp = datetime.now(timezone.utc).strftime('adhoc-%Y%m%dT%H%M%SZ')
    folder = ROOT / '.local-runs' / stamp
    if folder.exists():
        raise SystemExit('A local run with this timestamp exists; try again later.')
    case = {'case_id':'ad-hoc','label':'本地新问题','snapshot':args.snapshot,
            'task':args.task,'user_text':args.question}
    manifest = {
        'started_at':now(),'mode':'single_question_ungraded','harness':HARNESS_VERSION,
        'model_requested':args.model,'auth':'local ChatGPT login',
        'cli_version':subprocess.run([cli,'--version'],text=True,capture_output=True,check=True).stdout.strip(),
        'file_sha256':{str(p.relative_to(REPO)):digest(p) for p in [ROOT/'run.py',ROOT/'ask.py',
                         ROOT/'data/knowledge.json',ROOT/'data/adapter.json',*[REPO/f for f in SKILL_FILES]]},
    }
    write(folder/'manifest.json',manifest)
    output, execution, _ = call_model(case,'skill',args.model,folder,cli)
    manifest['completed_at']=now()
    write(folder/'manifest.json',manifest)
    print(output['decision']+' / '+output['reason_code'])
    print(output['player_text'])
    print('Local ungraded trace: '+str(folder))


if __name__ == '__main__':
    main()
