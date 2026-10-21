#!/usr/bin/env python3
"""Deterministic bookkeeping for Ouroboros runs: registered-only wiki snapshots, run gating,
packets, brief validation, idea ledger, and investigator verdicts. Makes no model calls."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import tomllib

SKILL = Path(__file__).resolve().parents[1]
LENS_BANK = SKILL / 'references' / 'lenses.md'
CONFIG_TEMPLATE = SKILL / 'templates' / 'config.toml'
AUDIT = SKILL.parent / 'living-wiki' / 'scripts' / 'wiki_audit.py'
WEEKDAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
LENS = re.compile(r'^- \*\*([A-Z]\d+) · ([^*]+?)\.?\*\*\s*(.+)$', re.M)
IDEA = re.compile(r'^## (Lead|Short|Wildcard) · \[(O-\d{8}-\d+)\] (.+)$')
NONE = re.compile(r'^## (Short|Wildcard) · none survived\s*$')
VERDICT = re.compile(r'^\*\*Verdict:\*\*[ \t]*(.*)$', re.M)
IDEA_ID = re.compile(r'\bO-\d{8}-\d+\b')
DREAMER_PLANS = [('A', 'C'), ('B', 'C'), ('B', 'A'), ('A', 'B')]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def load_config(journal: Path) -> dict:
    cfg = tomllib.loads((journal / 'config.toml').read_text(encoding='utf-8'))
    wikis, names = cfg.get('wiki', []), set()
    if not wikis:
        raise ValueError('config.toml needs at least one [[wiki]] entry')
    for w in wikis:
        if not w.get('name') or not (w.get('repo') or w.get('url')):
            raise ValueError('Each [[wiki]] needs name and repo (or url)')
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', w['name']) or w['name'] in names:
            raise ValueError(f"Wiki names must be unique lowercase slugs: {w['name']}")
        names.add(w['name'])
        w.setdefault('branch', 'main')
        w.setdefault('dir', 'wiki')
        w.setdefault('manifest', f"{w['dir']}/source-manifest.json")
    s = cfg.setdefault('schedule', {})
    for key, value in [('deep_weekday', 'sun'), ('first_run_days', 14), ('orphan_days', 60),
                       ('orphans_per_wiki', 2), ('nightly_dreamers', 2), ('deep_dreamers', 3)]:
        s.setdefault(key, value)
    if s['deep_weekday'] not in WEEKDAYS:
        raise ValueError(f"deep_weekday must be one of {WEEKDAYS}")
    cfg.setdefault('judgment', {}).setdefault('files', [])
    cfg.setdefault('voice', {}).setdefault('exemplars', [])
    return cfg


def read_json(path: Path, default):
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else default


def write_json(path: Path, value) -> None:
    pending = path.with_name(path.name + '.pending')
    pending.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    pending.replace(path)


def load_ledger(journal: Path) -> list[dict]:
    path = journal / 'ledger.jsonl'
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()] if path.is_file() else []


def save_ledger(journal: Path, ledger: list[dict]) -> None:
    pending = journal / 'ledger.jsonl.pending'
    pending.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in ledger), encoding='utf-8')
    pending.replace(journal / 'ledger.jsonl')


def git(cwd: Path | None, *args: str, stdin: str | None = None, check: bool = True) -> str:
    auth = ['-c', 'credential.helper=', '-c', 'credential.helper=!gh auth git-credential'] if shutil.which('gh') else []
    cmd = ['git', '-c', 'core.quotepath=off', *auth, *(['-C', str(cwd)] if cwd else []), *args]
    result = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(f"git {' '.join(args[:2])}: {result.stderr.strip()[:400]}")
    return result.stdout


def pattern(path: str, directory: bool = False) -> str:
    """Anchored, escaped no-cone sparse-checkout pattern for one repo-relative path."""
    escaped = re.sub(r'([\\*?\[\]!#])', r'\\\1', path.strip('/'))
    if escaped.endswith(' '):
        escaped = escaped[:-1] + '\\ '
    return '/' + escaped + ('/' if directory else '')


def sync(journal: Path, w: dict) -> dict:
    """Refresh a registered-only snapshot: the wiki folder plus files its manifest registers."""
    dest = journal / 'cache' / w['name']
    url = w.get('url') or f"https://github.com/{w['repo']}.git"
    if not (dest / '.git').is_dir():
        dest.parent.mkdir(parents=True, exist_ok=True)
        git(None, 'clone', '--quiet', '--filter=blob:none', '--no-checkout', '--branch', w['branch'], url, str(dest))
        git(dest, 'sparse-checkout', 'set', '--no-cone', '--stdin', stdin=pattern(w['dir'], True) + '\n')
        git(dest, 'checkout', '--quiet', w['branch'])
    else:
        git(dest, 'fetch', '--quiet', 'origin', w['branch'])
        git(dest, 'reset', '--quiet', '--hard', f"origin/{w['branch']}")
    manifest = dest / w['manifest']
    if not (dest / w['dir']).is_dir():
        raise RuntimeError(f"{w['dir']}/ is absent from {w['branch']} (not pushed yet?)")
    registered = [x['path'] for x in read_json(manifest, {'files': []}).get('files', [])]
    patterns = [pattern(w['dir'], True), pattern(w['manifest'])] + [pattern(p) for p in registered]
    git(dest, 'sparse-checkout', 'set', '--no-cone', '--stdin', stdin='\n'.join(patterns) + '\n')
    head = git(dest, 'log', '-1', '--format=%H%x02%cs').strip().split('\x02')
    return {'name': w['name'], 'status': 'ok', 'snapshot': str(dest), 'sha': head[0], 'commit_date': head[1],
            'registered': registered}


def in_scope(path: str, w: dict, registered: set[str]) -> bool:
    return path.startswith(w['dir'].rstrip('/') + '/') or path in registered or path == w['manifest']


def changes(snap: dict, w: dict, since: str | None, first_days: int) -> dict:
    dest, registered = Path(snap['snapshot']), set(snap['registered'])
    known = since and not subprocess.run(['git', '-C', str(dest), 'cat-file', '-e', since + '^{commit}'],
                                         capture_output=True).returncode
    span = [f'{since}..HEAD'] if known else [f'--since={first_days}.days', 'HEAD']
    log = git(dest, 'log', '--no-renames', '--name-only', '--date=short', '--format=%x01%h%x02%ad%x02%s', *span)
    commits, files = [], set()
    for block in log.split('\x01')[1:]:
        head, _, names = block.partition('\n')
        short, day, subject = head.split('\x02', 2)
        hit = sorted(n for n in names.splitlines() if n and in_scope(n, w, registered))
        if hit:
            commits.append({'sha': short, 'date': day, 'subject': subject, 'files': hit})
            files.update(hit)
    return {'range': span[0] if known else f'last {first_days} days', 'commits': commits, 'files': sorted(files)}


def orphans(snap: dict, w: dict, days: int, k: int, rng: random.Random) -> list[str]:
    dest = Path(snap['snapshot'])
    recent = set(git(dest, 'log', '--no-renames', '--name-only', '--format=', f'--since={days}.days', 'HEAD').split('\n'))
    pages = sorted(p.relative_to(dest).as_posix() for p in (dest / w['dir']).rglob('*.md')
                   if not {'evidence', 'templates'} & set(p.relative_to(dest / w['dir']).parts))
    stale = [p for p in pages if p not in recent]
    return sorted(rng.sample(stale, min(k, len(stale))))


def local_status(w: dict) -> dict | None:
    local = Path(w['local']) if w.get('local') else None
    if not local or not (local / '.git').exists():
        return None
    dirty = [x for x in git(local, 'status', '--porcelain', '--', w['dir'], check=False).splitlines() if x.strip()]
    ahead = git(local, 'log', '--oneline', f"origin/{w['branch']}..HEAD", '--', w['dir'], check=False).splitlines()
    result = {'uncommitted_wiki_files': len(dirty), 'unpushed_wiki_commits': len(ahead)}
    if AUDIT.is_file():
        run = subprocess.run([sys.executable, str(AUDIT), '--root', str(local)], capture_output=True, text=True)
        try:
            report = json.loads(run.stdout)
            new = report.get('new_errors', report.get('errors', []))
            result['audit'] = {'errors': len(new) + len(report.get('known_errors', [])), 'new_errors': new[:10],
                               'known_errors': len(report.get('known_errors', [])),
                               'warnings': len(report.get('warnings', []))}
        except json.JSONDecodeError:
            result['audit'] = {'unavailable': (run.stderr or run.stdout).strip()[:300]}
    return result


def lens_bank() -> list[dict]:
    return [{'id': m[1], 'name': m[2].strip(), 'text': m[3].strip()} for m in LENS.finditer(LENS_BANK.read_text(encoding='utf-8'))]


def pick_lenses(dreamers: int, history: list[dict], rng: random.Random) -> dict:
    bank, used = lens_bank(), {x for run in history[-4:] for x in run.get('lenses', [])}
    taken, plan = set(), []

    def draw(group: str) -> dict:
        pool = [x for x in bank if x['id'][0] == group and x['id'] not in taken]
        fresh = [x for x in pool if x['id'] not in used] or pool
        choice = rng.choice(fresh)
        taken.add(choice['id'])
        return choice

    for i in range(dreamers):
        plan.append([draw(g) for g in DREAMER_PLANS[i % len(DREAMER_PLANS)]])
    return {'dreamers': plan, 'wildcard': draw('W')}


def idea_sections(text: str) -> list[tuple[str, str, str, str]]:
    sections, lines, current = [], text.splitlines(), None
    for line in lines + ['## end']:
        if line.startswith('## '):
            if current:
                sections.append((*current[:3], '\n'.join(current[3])))
            match = IDEA.match(line)
            current = (match[1], match[2], match[3].strip(), []) if match else None
        elif current:
            current[3].append(line)
    return sections


def harvest(journal: Path) -> list[dict]:
    """Copy investigator verdicts written under ideas into the ledger and verdicts.md."""
    ledger, recorded = load_ledger(journal), []
    by_id = {x['id']: x for x in ledger}
    for brief in sorted((journal / 'briefs').glob('*.md')):
        for _, idea, title, body in idea_sections(brief.read_text(encoding='utf-8')):
            line = VERDICT.search(body)
            parsed = re.match(r'(?i)(pursue|drop)\b[\s:—–-]*(.*)$', line[1].strip()) if line else None
            record = by_id.get(idea)
            if not parsed or not record:
                continue
            verdict, reason = parsed[1].lower(), parsed[2].strip()
            if (record.get('verdict'), record.get('reason')) == (verdict, reason):
                continue
            previous = record.get('verdict')
            record.update(verdict=verdict, reason=reason, verdict_date=date.today().isoformat(),
                          status='pursued' if verdict == 'pursue' else 'dropped')
            recorded.append({**record, 'previous': previous})
    if recorded:
        save_ledger(journal, ledger)
        path = journal / 'verdicts.md'
        out = path.read_text(encoding='utf-8') if path.is_file() else VERDICTS_HEADER
        for r in recorded:
            out += (f"\n## {r['verdict_date']} · {r['id']} · {r['verdict']}\n\n- Idea: {r['title']} "
                    f"([brief]({r['brief']}))\n- Decided by: investigator (verdict written under the idea)\n"
                    f"- Reason: {r['reason'] or 'not stated'}\n")
            if r['previous']:
                out += f"- Supersedes the earlier verdict: {r['previous']}\n"
        path.write_text(out, encoding='utf-8')
    return recorded


VERDICTS_HEADER = ('# Investigator verdicts on Ouroboros ideas\n\nEach entry records the investigator\'s own '
                   'verdict and reason, harvested from the brief where it was written. Idea text is an agent '
                   'proposal; only the verdict and reason are investigator decisions.\n')


def commit(journal: Path, message: str) -> None:
    if (journal / '.git').is_dir():
        git(journal, 'add', '-A')
        if git(journal, 'status', '--porcelain'):
            git(journal, 'commit', '--quiet', '-m', message)


def init(journal: Path) -> dict:
    journal.mkdir(parents=True, exist_ok=True)
    for sub in ('briefs', 'runs'):
        (journal / sub).mkdir(exist_ok=True)
    created = []
    for name, content in [('config.toml', CONFIG_TEMPLATE.read_text(encoding='utf-8')), ('ledger.jsonl', ''),
                          ('verdicts.md', VERDICTS_HEADER), ('state.json', '{}\n'), ('.gitignore', 'cache/\n*.pending\n')]:
        if not (journal / name).exists():
            (journal / name).write_text(content, encoding='utf-8')
            created.append(name)
    if not (journal / '.git').exists():
        git(None, 'init', '--quiet', str(journal))
    return {'journal': str(journal), 'created': created, 'next': 'Edit config.toml, then run prepare.'}


def next_ids(ledger: list[dict], day: str, count: int = 3) -> list[str]:
    stamp = day.replace('-', '')
    used = [int(x['id'].rsplit('-', 1)[1]) for x in ledger if x['id'].startswith(f'O-{stamp}-')]
    start = max(used, default=0) + 1
    return [f'O-{stamp}-{n}' for n in range(start, start + count)]


def prepare(journal: Path, mode: str, key: str | None, today: date | None = None) -> dict:
    journal, today = journal.resolve(), today or date.today()
    cfg, state = load_config(journal), read_json(journal / 'state.json', {})
    found = harvest(journal)
    snaps, problems = [], []
    for w in cfg['wiki']:
        try:
            snap = sync(journal, w)
            snap['changes'] = changes(snap, w, state.get('wikis', {}).get(w['name'], {}).get('sha'),
                                      cfg['schedule']['first_run_days'])
            snaps.append(snap)
        except (RuntimeError, OSError, ValueError, json.JSONDecodeError) as exc:
            problems.append({'name': w['name'], 'status': 'blocked', 'problem': str(exc)})
    changed = sum(len(s['changes']['files']) for s in snaps)
    weekday = WEEKDAYS[today.weekday()]
    if mode == 'auto':
        last_deep = state.get('last_deep')
        due = weekday == cfg['schedule']['deep_weekday'] and (not last_deep or (today - date.fromisoformat(last_deep)).days >= 6)
        mode = 'deep' if due and snaps else 'nightly' if changed else 'skip'
    if mode == 'skip':
        if found:
            commit(journal, f'ouroboros: record {len(found)} verdict(s)')
        reason = 'all wikis blocked' if not snaps else 'no registered wiki content changed since the last brief'
        return {'status': 'skip', 'reason': reason, 'problems': problems, 'verdicts_recorded': len(found)}
    key = key or (f'{mode}-{today.isoformat()}' if mode != 'manual' else f"manual-{datetime.now():%Y-%m-%d-%H%M}")
    if not re.fullmatch(r'[A-Za-z0-9._-]+', key):
        raise ValueError('Run keys may contain only letters, digits, dot, dash and underscore')
    run = journal / 'runs' / key
    run.parent.mkdir(parents=True, exist_ok=True)
    try:
        run.mkdir()
    except FileExistsError:
        return {'status': 'exists', 'claimed': False, 'directory': str(run), 'record': read_json(run / 'run.json', {})}
    if not snaps:
        blocker = '; '.join(f"{p['name']}: {p['problem']}" for p in problems)
        notify = blocker != state.get('last_blocker')
        state['last_blocker'] = blocker
        write_json(journal / 'state.json', state)
        write_json(run / 'run.json', {'key': key, 'mode': mode, 'status': 'blocked', 'created_at': now(), 'note': blocker})
        commit(journal, f'ouroboros: {key} blocked')
        return {'status': 'blocked', 'directory': str(run), 'problem': blocker, 'notify': notify}
    rng = random.Random(key)
    dreamers = cfg['schedule']['deep_dreamers' if mode == 'deep' else 'nightly_dreamers']
    lenses = pick_lenses(dreamers, state.get('lens_history', []), rng)
    by_name = {w['name']: w for w in cfg['wiki']}
    mentioned = set()
    for s in snaps:
        s['orphans'] = orphans(s, by_name[s['name']], cfg['schedule']['orphan_days'],
                               cfg['schedule']['orphans_per_wiki'] * (2 if mode == 'deep' else 1), rng)
        s['local'] = local_status(by_name[s['name']])
        for page in (Path(s['snapshot']) / by_name[s['name']]['dir']).rglob('*.md'):
            mentioned.update(IDEA_ID.findall(page.read_text(encoding='utf-8', errors='replace')))
    ledger = load_ledger(journal)
    promoted = [x for x in ledger if x.get('status') == 'pursued' and x['id'] in mentioned]
    for x in promoted:
        x['status'] = 'promoted'
    if promoted:
        save_ledger(journal, ledger)
    packet = {'key': key, 'mode': mode, 'date': today.isoformat(), 'created_at': now(), 'directory': str(run),
              'idea_ids': next_ids(ledger, today.isoformat()), 'lenses': lenses, 'wikis': snaps, 'blocked': problems,
              'judgment': cfg['judgment']['files'], 'voice': voice_paths(cfg, snaps), 'verdicts_recorded': found}
    write_json(run / 'packet.json', packet)
    (run / 'packet.md').write_text(render_packet(packet, ledger, by_name), encoding='utf-8')
    write_json(run / 'run.json', {'key': key, 'mode': mode, 'status': 'reserved', 'created_at': now()})
    state.pop('last_blocker', None)
    write_json(journal / 'state.json', state)
    return {'status': 'reserved', 'claimed': True, 'key': key, 'mode': mode, 'directory': str(run),
            'packet': str(run / 'packet.md'), 'changed_files': changed, 'blocked': problems,
            'verdicts_recorded': len(found)}


def voice_paths(cfg: dict, snaps: list[dict]) -> list[dict]:
    snapshots = {s['name']: s for s in snaps}
    out = []
    for item in cfg['voice']['exemplars']:
        name, _, rel = item.partition(':')
        snap = snapshots.get(name)
        ok = bool(snap) and rel in snap['registered'] and (Path(snap['snapshot']) / rel).is_file()
        out.append({'exemplar': item, 'path': str(Path(snap['snapshot']) / rel) if snap else None,
                    'status': 'ok' if ok else 'unavailable or not registered'})
    return out


def render_packet(p: dict, ledger: list[dict], by_name: dict) -> str:
    out = [f"# Ouroboros packet — {p['key']} ({p['mode']})", '',
           f"Run directory: `{p['directory']}`. Idea IDs to use, in slot order: {', '.join(p['idea_ids'])}.", '',
           '## Readable scope', '',
           'Read only inside these snapshots (wiki folder plus registered sources), the judgment files, '
           'and this skill. Never open other project files.', '']
    for s in p['wikis']:
        w = by_name[s['name']]
        out.append(f"- **{s['name']}**: `{s['snapshot']}` at `{s['sha'][:7]}` ({s['commit_date']}); wiki `{w['dir']}/`, "
                   f"{len(s['registered'])} registered sources; questions `{w['dir']}/questions.md`, decisions `{w['dir']}/decisions.md`, log `{w['dir']}/log.md`.")
        if s['local'] and (s['local']['uncommitted_wiki_files'] or s['local']['unpushed_wiki_commits']):
            out.append(f"  - Not visible to this run: {s['local']['uncommitted_wiki_files']} uncommitted and "
                       f"{s['local']['unpushed_wiki_commits']} unpushed wiki changes in the local checkout.")
    for b in p['blocked']:
        out.append(f"- **{b['name']}**: blocked — {b['problem']}")
    out += ['', '## Changes since the last brief', '']
    for s in p['wikis']:
        c = s['changes']
        out.append(f"### {s['name']} ({c['range']}; {len(c['files'])} files)")
        out += [f"- {x['date']} `{x['sha']}` {x['subject']} — {', '.join(x['files'][:12])}"
                + (' …' if len(x['files']) > 12 else '') for x in c['commits']] or ['- No in-scope changes.']
        out.append('')
    out += ['## Orphan sample (pages unchanged for a while)', '']
    out += [f"- {s['name']}: {', '.join(s['orphans']) or 'none'}" for s in p['wikis']]
    out += ['', '## Lenses for this run', '']
    for i, lenses in enumerate(p['lenses']['dreamers'], 1):
        out.append(f"- Dreamer {i}: " + '; '.join(f"{x['id']} · {x['name']} — {x['text']}" for x in lenses))
    wc = p['lenses']['wildcard']
    out += [f"- Wildcard (last dreamer adds one candidate): {wc['id']} · {wc['name']} — {wc['text']}", '',
            '## Judgment files (load only after the first dreaming pass, and for the critic)', '']
    out += [f'- `{x}`' for x in p['judgment']] or ['- None configured.']
    out += ['', '## Voice exemplars (investigator\'s own registered writing)', '']
    out += [f"- {v['exemplar']}: `{v['path']}` ({v['status']})" for v in p['voice']] or ['- None configured.']
    out += ['', '## Past ideas (do not re-propose without new evidence)', '']
    out += [f"- {x['id']} · {x.get('status', 'open')} · {x['title']}" + (f" — reason: {x['reason']}" if x.get('reason') else '')
            for x in ledger] or ['- None yet.']
    pending = [x for x in ledger if x.get('status') == 'pursued']
    out += ['', '## Pursued ideas awaiting promotion into a wiki', '']
    out += [f"- {x['id']} · {x['title']} ([brief]({x['brief']}))" for x in pending] or ['- None.']
    out += ['', '## Maintenance findings (local audit)', '']
    for s in p['wikis']:
        a = (s['local'] or {}).get('audit')
        if not a:
            out.append(f"- {s['name']}: no local audit (no local checkout or living-wiki audit).")
        elif 'unavailable' in a:
            out.append(f"- {s['name']}: audit unavailable — {a['unavailable']}")
        else:
            out.append(f"- {s['name']}: {a['errors']} errors ({a['known_errors']} known), {a['warnings']} warnings.")
            out += [f'  - new: {e}' for e in a['new_errors']]
    if p['verdicts_recorded']:
        out += ['', '## Verdicts recorded at the start of this run', '']
        out += [f"- {x['id']} · {x['verdict']} — {x['reason'] or 'no reason given'}" for x in p['verdicts_recorded']]
    return '\n'.join(out) + '\n'


def words(text: str) -> int:
    body = [ln for ln in text.splitlines() if not ln.startswith('**')]
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", '\n'.join(body)))


def validate(text: str, ledger_ids: set[str]) -> tuple[list[str], list[tuple[str, str, str]]]:
    problems, lines = [], text.splitlines()
    if not lines or not lines[0].startswith('# '):
        problems.append('The brief must start with a level-1 title.')
    sections = idea_sections(text)
    slots = [s[0] for s in sections]
    nones = {m[1] for m in (NONE.match(x) for x in lines) if m}
    if slots.count('Lead') != 1:
        problems.append('Exactly one Lead idea is required.')
    for slot in ('Short', 'Wildcard'):
        if slots.count(slot) + (slot in nones) != 1:
            problems.append(f'Exactly one {slot} slot is required (an idea or "## {slot} · none survived").')
    ids = [s[1] for s in sections]
    if len(ids) != len(set(ids)) or set(ids) & ledger_ids:
        problems.append('Idea IDs must be new and unique; use the IDs given in the packet.')
    for slot, idea, _, body in sections:
        for label in ('Trigger', 'Cheapest check', 'Evidence'):
            if f'**{label}:**' not in body:
                problems.append(f'{idea} lacks a **{label}:** line.')
        verdict = VERDICT.search(body)
        if not verdict:
            problems.append(f'{idea} lacks an empty **Verdict:** line.')
        elif verdict[1].strip():
            problems.append(f'{idea}: leave the verdict empty; only the investigator fills it.')
        n = words(body)
        if slot == 'Lead' and not 450 <= n <= 1100:
            problems.append(f'Lead argument has {n} words; write about 600–900.')
        if slot != 'Lead' and n > 300:
            problems.append(f'{idea} has {n} words; keep short ideas near 150.')
    for heading in ('Maintenance', 'Discarded'):
        if not re.search(rf'^## {heading}\s*$', text, re.M):
            problems.append(f'Missing section: ## {heading}')
    if re.search(r'\[\d+\]', text) and not re.search(r'^## References\s*$', text, re.M):
        problems.append('Numbered citations need a ## References section.')
    return problems, [(s[0], s[1], s[2]) for s in sections]


def finish(journal: Path, key: str, status: str, note: str, brief: Path | None) -> dict:
    journal = journal.resolve()
    run = journal / 'runs' / key
    record = read_json(run / 'run.json', {})
    if record.get('key') != key or record.get('status') != 'reserved':
        raise ValueError('Only a matching reserved run can be finished')
    if status not in {'complete', 'failed', 'blocked'} or not note.strip():
        raise ValueError('Use complete, failed or blocked with a nonempty note')
    packet, fields = read_json(run / 'packet.json', {}), {}
    ledger = load_ledger(journal)
    if status == 'complete':
        real = brief.resolve() if brief else None
        if not real or not real.is_relative_to(run) or not real.is_file():
            raise ValueError('The brief must be a file inside this run directory')
        text = real.read_text(encoding='utf-8')
        problems, ideas = validate(text, {x['id'] for x in ledger})
        if problems:
            raise ValueError('Brief failed validation: ' + ' | '.join(problems))
        target = journal / 'briefs' / f"{packet['date']}-{packet['mode']}.md"
        n = 2
        while target.exists():
            target, n = journal / 'briefs' / f"{packet['date']}-{packet['mode']}-{n}.md", n + 1
        target.parent.mkdir(exist_ok=True)
        target.write_text(text, encoding='utf-8')
        rel = target.relative_to(journal).as_posix()
        ledger += [{'id': idea, 'date': packet['date'], 'key': key, 'slot': slot, 'title': title, 'brief': rel,
                    'status': 'open', 'verdict': None} for slot, idea, title in ideas]
        save_ledger(journal, ledger)
        state = read_json(journal / 'state.json', {})
        for s in packet['wikis']:
            state.setdefault('wikis', {})[s['name']] = {'sha': s['sha'], 'brief': rel}
        if packet['mode'] == 'deep':
            state['last_deep'] = packet['date']
        lenses = [x['id'] for group in packet['lenses']['dreamers'] for x in group] + [packet['lenses']['wildcard']['id']]
        state['lens_history'] = (state.get('lens_history', []) + [{'key': key, 'lenses': lenses}])[-20:]
        write_json(journal / 'state.json', state)
        fields = {'brief': rel, 'ideas': [i for _, i, _ in ideas]}
    marker = run / '.finish-claimed'
    try:
        with marker.open('x') as stream:
            stream.write(now())
    except FileExistsError as exc:
        raise ValueError('Finalization already claimed; inspect the run before recovery') from exc
    record.update(status=status, finished_at=now(), note=note, **fields)
    write_json(run / 'run.json', record)
    commit(journal, f'ouroboros: {key} {status}')
    return {'directory': str(run), 'record': record}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('init', 'prepare', 'finish', 'harvest'):
        cmd = sub.add_parser(name)
        cmd.add_argument('--journal', type=Path, required=True)
        if name == 'prepare':
            cmd.add_argument('--mode', choices=['auto', 'nightly', 'deep', 'manual'], default='auto')
            cmd.add_argument('--key', help='Override the run key, e.g. for a requested retry')
        if name == 'finish':
            cmd.add_argument('--key', required=True)
            cmd.add_argument('--status', choices=['complete', 'failed', 'blocked'], required=True)
            cmd.add_argument('--note', required=True)
            cmd.add_argument('--brief', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            result = init(args.journal)
        elif args.command == 'prepare':
            result = prepare(args.journal, args.mode, args.key)
        elif args.command == 'finish':
            result = finish(args.journal, args.key, args.status, args.note, args.brief)
        else:
            found = harvest(args.journal.resolve())
            commit(args.journal.resolve(), f'ouroboros: record {len(found)} verdict(s)') if found else None
            result = {'verdicts_recorded': [{k: x[k] for k in ('id', 'verdict', 'reason')} for x in found]}
    except (OSError, ValueError, RuntimeError, tomllib.TOMLDecodeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
