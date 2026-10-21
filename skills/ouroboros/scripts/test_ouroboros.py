import json
from datetime import date
from pathlib import Path
import random
import subprocess

import pytest

import ouroboros as ob


def sh(cwd, *args):
    subprocess.run(['git', '-C', str(cwd), *args], check=True, capture_output=True)


@pytest.fixture(autouse=True)
def identity(monkeypatch):
    for key in ('AUTHOR', 'COMMITTER'):
        monkeypatch.setenv(f'GIT_{key}_NAME', 'Test')
        monkeypatch.setenv(f'GIT_{key}_EMAIL', 'test@example.org')


def remote(tmp_path):
    work = tmp_path / 'work'
    (work / 'wiki').mkdir(parents=True)
    (work / 'resources').mkdir()
    (work / 'other').mkdir()
    (work / 'resources' / 'a [v1].txt').write_text('registered')
    (work / 'resources' / 'b.txt').write_text('not registered')
    (work / 'other' / 'code.py').write_text('print(1)')
    (work / 'wiki' / 'index.md').write_text('# Index\n')
    (work / 'wiki' / 'questions.md').write_text('# Questions\n')
    (work / 'wiki' / 'source-manifest.json').write_text(json.dumps({'files': [{'path': 'resources/a [v1].txt'}]}))
    sh(tmp_path, 'init', '--quiet', '-b', 'main', str(work))
    sh(work, 'add', '-A')
    sh(work, 'commit', '--quiet', '-m', 'start')
    bare = tmp_path / 'remote.git'
    subprocess.run(['git', 'clone', '--quiet', '--bare', str(work), str(bare)], check=True)
    sh(work, 'remote', 'add', 'origin', str(bare))
    return work, bare


def journal(tmp_path, bare):
    j = tmp_path / 'journal'
    ob.init(j)
    (j / 'config.toml').write_text(f'[[wiki]]\nname = "proj"\nrepo = "o/r"\nurl = "file://{bare}"\n')
    return j


def push(work, path, text, message):
    (work / path).write_text(text)
    sh(work, 'add', '-A')
    sh(work, 'commit', '--quiet', '-m', message)
    sh(work, 'push', '--quiet', 'origin', 'main')


def brief(ids, lead_words=620):
    lead = ' '.join(['vessel'] * lead_words)

    def block(slot, idea, n):
        return (f'## {slot} · [{idea}] A specific idea\n\n{" ".join(["word"] * n)}\n\n**Trigger:** [index](x)\n'
                f'**Cheapest check:** reanalyse\n**Evidence:** speculation\n**Verdict:**\n\n')
    return (f'# Ouroboros brief\n\n## Lead · [{ids[0]}] Lead idea\n\n{lead}\n\n**Trigger:** [index](x)\n'
            f'**Cheapest check:** reanalyse\n**Evidence:** verified [1]\n**Verdict:**\n\n'
            + block('Short', ids[1], 120) + block('Wildcard', ids[2], 120)
            + '## Maintenance\n\n- none\n\n## Discarded\n\n- a\n- b\n- c\n\n## References\n\n1. Ref.\n')


def complete(j, result):
    packet = json.loads((Path(result['directory']) / 'packet.json').read_text())
    path = Path(result['directory']) / 'brief.md'
    path.write_text(brief(packet['idea_ids']))
    return ob.finish(j, result['key'], 'complete', 'ok', path), packet


def test_snapshot_contains_only_wiki_and_registered_sources(tmp_path):
    work, bare = remote(tmp_path)
    j = journal(tmp_path, bare)
    result = ob.prepare(j, 'auto', None, date(2026, 10, 20))
    assert result['status'] == 'reserved' and result['mode'] == 'nightly'
    snap = j / 'cache' / 'proj'
    assert (snap / 'wiki' / 'index.md').is_file()
    assert (snap / 'resources' / 'a [v1].txt').is_file()
    assert not (snap / 'resources' / 'b.txt').exists()
    assert not (snap / 'other' / 'code.py').exists()
    packet = (Path(result['directory']) / 'packet.md').read_text()
    assert 'wiki/index.md' in packet and 'Dreamer 2' in packet and 'Wildcard' in packet


def test_auto_skips_without_changes_and_resumes_after_a_push(tmp_path):
    work, bare = remote(tmp_path)
    j = journal(tmp_path, bare)
    complete(j, ob.prepare(j, 'auto', None, date(2026, 10, 20)))
    assert ob.prepare(j, 'auto', None, date(2026, 10, 21))['status'] == 'skip'
    push(work, 'other/code.py', 'print(2)', 'unregistered change')
    assert ob.prepare(j, 'auto', None, date(2026, 10, 21))['status'] == 'skip'
    push(work, 'wiki/index.md', '# Index\n\nNew result.\n', 'wiki change')
    again = ob.prepare(j, 'auto', None, date(2026, 10, 21))
    assert again['status'] == 'reserved' and again['changed_files'] == 1


def test_deep_run_on_the_configured_weekday_and_duplicate_key(tmp_path):
    work, bare = remote(tmp_path)
    j = journal(tmp_path, bare)
    sunday = date(2026, 10, 25)
    result = ob.prepare(j, 'auto', None, sunday)
    assert result['mode'] == 'deep' and result['key'] == 'deep-2026-10-25'
    assert ob.prepare(j, 'deep', None, sunday)['claimed'] is False


def test_finish_rejects_invalid_briefs(tmp_path):
    work, bare = remote(tmp_path)
    j = journal(tmp_path, bare)
    result = ob.prepare(j, 'nightly', None, date(2026, 10, 20))
    ids = json.loads((Path(result['directory']) / 'packet.json').read_text())['idea_ids']
    path = Path(result['directory']) / 'brief.md'
    for bad in [brief(ids).replace('## Wildcard', '## Other'), brief(ids).replace('**Verdict:**\n\n## Short', '**Verdict:** pursue\n\n## Short'),
                brief(ids, lead_words=100), brief(ids).replace('## Discarded', '## Dropped')]:
        path.write_text(bad)
        with pytest.raises(ValueError):
            ob.finish(j, result['key'], 'complete', 'ok', path)
    path.write_text(brief(ids).replace(f'## Wildcard · [{ids[2]}] A specific idea', '## Wildcard · none survived'))
    record = ob.finish(j, result['key'], 'complete', 'ok', path)['record']
    assert record['ideas'] == ids[:2]


def test_harvest_records_investigator_verdicts_once(tmp_path):
    work, bare = remote(tmp_path)
    j = journal(tmp_path, bare)
    finished, packet = complete(j, ob.prepare(j, 'nightly', None, date(2026, 10, 20)))
    target = j / finished['record']['brief']
    first, second = packet['idea_ids'][:2]
    text = target.read_text().replace('**Verdict:**\n\n## Short', '**Verdict:** drop — already tested in 2025\n\n## Short', 1)
    text = text.replace('**Verdict:**\n\n## Wildcard', '**Verdict:** Pursue: worth a pilot\n\n## Wildcard', 1)
    target.write_text(text)
    found = ob.harvest(j)
    assert {(x['id'], x['verdict'], x['reason']) for x in found} == {(first, 'drop', 'already tested in 2025'),
                                                                    (second, 'pursue', 'worth a pilot')}
    assert ob.harvest(j) == []
    verdicts = (j / 'verdicts.md').read_text()
    assert verdicts.count(first) == 1 and 'Decided by: investigator' in verdicts
    ledger = {x['id']: x for x in ob.load_ledger(j)}
    assert ledger[first]['status'] == 'dropped' and ledger[second]['status'] == 'pursued'
    push(work, 'wiki/questions.md', f'# Questions\n\n- Proposed from {second}.\n', 'promote')
    ob.prepare(j, 'nightly', None, date(2026, 10, 22))
    assert {x['id']: x for x in ob.load_ledger(j)}[second]['status'] == 'promoted'


def test_patterns_escape_special_characters():
    assert ob.pattern('resources/a [v1].txt') == '/resources/a \\[v1\\].txt'
    assert ob.pattern('wiki', True) == '/wiki/'
    assert ob.pattern('#notes/!x*.md') == '/\\#notes/\\!x\\*.md'


def test_lens_sampling_is_deterministic_and_distinct():
    bank = ob.lens_bank()
    assert {x['id'][0] for x in bank} == {'A', 'B', 'C', 'W'}
    one = ob.pick_lenses(3, [], random.Random('k'))
    two = ob.pick_lenses(3, [], random.Random('k'))
    assert one == two
    ids = [x['id'] for group in one['dreamers'] for x in group]
    assert len(ids) == len(set(ids)) == 6 and one['wildcard']['id'].startswith('W')
