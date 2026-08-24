# Contributing

## Add a Skill

1. Confirm the capability is reusable across projects.
2. Create `skills/<name>/SKILL.md`; the directory and frontmatter names must match.
3. Record the Skill in `manifest.json`, including its canonical source, provenance, license,
   category, compatibility, and complete file list.
4. Add it to `skills/INDEX.md` and relevant profiles.
5. Add a `CHANGELOG.md` entry and update README when the public catalog changes.
6. Run the validation commands from `AGENTS.md`.

If the Skill is maintained elsewhere, prefer a registry record or a small adapter over a
copied fork. Never guess an upstream URL or license.

## Update a Skill

Read the whole Skill and its source record first. Preserve portable behavior in `SKILL.md` and
put Agent-specific metadata in sidecars where possible. Describe behavior changes and any
project migration in the changelog.

## Remove or supersede a Skill

Remove it from `manifest.json`, the index, README, every profile, and any integration example.
State the reason and replacement in the changelog. Do not leave a broken public entry only to
preserve history; Git already preserves history.

## Review checklist

- The Skill objective, boundaries, inputs, outputs, and acceptance checks are clear.
- Examples are synthetic or public.
- Source and license are verifiable.
- No secret, personal path, private endpoint, identifier, or proprietary context is present.
- Registry, public-content, and diff checks pass.
- A human owner explicitly approves function and privacy before merge.
