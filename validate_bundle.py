from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
for name in ('game-coach-kb', 'game-coach-perception', 'game-coach-annotation'):
    result = subprocess.run([sys.executable, str(root / name / 'scripts/validate_package.py')], check=True, capture_output=True, text=True)
    print(result.stdout.strip())
a = json.loads((root / 'game-coach-kb/schemas/observation-bundle.schema.json').read_text(encoding='utf-8'))
b = json.loads((root / 'game-coach-perception/schemas/observation-bundle.schema.json').read_text(encoding='utf-8'))
assert a == b, 'ObservationBundle schema drift between skills'
print('Cross-skill ObservationBundle contract matches.')
annotation_schema = json.loads((root / 'game-coach-annotation/schemas/annotation-case.schema.json').read_text(encoding='utf-8'))
assert {'objective_labels', 'expert_judgments', 'split'} <= set(annotation_schema['required'])
print('AnnotationCase keeps facts, judgments and dataset split separate.')
