# Project Integration

## Recommended: reference the library

Copy [`../templates/AGENTS.skill-library.md`](../templates/AGENTS.skill-library.md) into the
project's root `AGENTS.md`. Replace `<ABSOLUTE_PATH_TO_USEFUL_SKILLS>` with that machine's
checkout path.

This gives the project a small routing instruction while keeping Skill content centralized.
The Agent reads `manifest.json`, selects a relevant Skill, and loads only that Skill's
`SKILL.md`.

For Claude Code, keep one policy source by adding this to the project's `CLAUDE.md`:

```markdown
@AGENTS.md
```

If another Agent uses a different persistent instruction filename, place the same reference
block there. The contract is format-independent: locate the central checkout, read its
registry, then progressively load the selected `SKILL.md`.

## Optional: Agent-native discovery

Some Agents discover Skills only from their own user directories. Preview a profile first:

```bash
python3 scripts/link_skills.py --profile research --agent all
```

Apply it after reviewing the destinations:

```bash
python3 scripts/link_skills.py --profile research --agent all --apply
```

Built-in destinations are:

| Name | Destination |
| --- | --- |
| `codex` | `~/.agents/skills/` |
| `claude` | `~/.claude/skills/` |

These paths were checked on 2026-08-07 against the
[official Codex Skill documentation](https://learn.chatgpt.com/docs/build-skills) and
[official Claude Code Skill documentation](https://code.claude.com/docs/en/skills). Both
products support a Skill directory that is a symbolic link; Claude Code documents this for
version 2.1.203 and later.

For another Agent, provide its discovery directory explicitly:

```bash
python3 scripts/link_skills.py --profile research --target /absolute/agent/skills --apply
```

The tool creates per-Skill links, not a linked parent directory. It refuses to replace a real
file or directory and refuses to retarget an unrelated link.

## Multiple machines

Clone the same GitHub repository on each machine. Keep project Agent files machine-portable by
using a small local include or by replacing the path placeholder during machine setup. Do not
commit one person's `/Users/...`, `/home/...`, or mounted-volume path into a shared project.

Use Git tags or commit pins when a project must reproduce a historical workflow. A live
checkout is better for personal projects that should receive Skill edits immediately.

## Sharing improvements

Projects consume the library as read-only by default. When a project reveals a reusable
improvement:

1. remove project names, local paths, private data, and narrow assumptions;
2. update the canonical Skill in this repository on a review branch;
3. update registry projections and the changelog;
4. validate and obtain human review.

This is how Agents share one improvement without creating drifting project copies.
