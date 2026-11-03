# Remote compute unification

## Scope and authority

The owner requested one `remote-compute-ssh` entrypoint, selective loading of SCG
information, optional connections to multiple servers, and retirement of
`compute-scg` after confirming complete migration. The owner's standing instruction
in this chat is to commit and push directly without a separate human review step.
This change follows that instruction on `main`; the registry's default review
policy remains unchanged. Independent human review is waived, not recorded as done.

## File and behavior preservation audit

The baseline is commit `9c4707483c7ebf152e34b5bbdaa0dfebb1c1c867`. All eight files
from `compute-scg` are accounted for below. Exact source hashes and the destination
map are retained in the surviving skill's `references/scg-provenance.json`.

| Retired file | Destination under `remote-compute-ssh` | Preservation check |
| --- | --- | --- |
| `SKILL.md` | `SKILL.md` and `references/scg-operations.md` | SCG routing, access, authorization, resource sizing, templates, environment checks, job records, pending/completed distinctions, output verification, and source limits retained. The competing entrypoint is removed. |
| `references/setup.md` | `references/setup.md` and `references/scg-operations.md` | SCG enrollment, direct SSH and alias setup, first-factor/key policy, host verification, Windows/WSL distinction, authentication reuse, persistence caveat, explicit shutdown, and no app dependency retained. Common mechanics have one home. |
| `references/scg-operations.md` | `references/scg-operations.md` | All original sections and dated observations retained. Added SCG-only routing, migrated template links, and explicit private-overlay precedence. |
| `references/provenance.json` | `references/scg-provenance.json` | Original source metadata, license standing, and bundled hashes retained; historical identity and consolidation map added. |
| `scripts/ssh-connect` | `scripts/ssh-connect` | Byte-for-byte identical to the existing generic helper; one copy remains. |
| `templates/cpu.sbatch` | `templates/scg-cpu.sbatch` | Byte-for-byte identical, including placeholders and unvalidated-template caveat. |
| `templates/gpu-p100-smoke.sbatch` | `templates/scg-gpu-p100-smoke.sbatch` | Byte-for-byte identical, including historical detection-only limits. |
| `tests/test_connection_helper.py` | `tests/test_connection_helper.py` | The original suites were identical. All ten original tests remain, with two new multi-server behavior checks. |

The SCG entrypoint's explicit account/partition requirement and approved-resource
envelope handling are retained. `sbatch --test-only` remains an acceptance check,
not execution evidence. A GPU detection check remains distinct from an application
or scientific validation. No source observations were promoted into current access,
free-capacity, runtime, or queue-time guarantees.

## Routing, multiple servers, and private state

The surviving entrypoint names the conditions for reading SCG details, first-time
setup, and multiple-server instructions. SCG material is loaded only for a selected
SCG target. The helper continues to accept one target per invocation; independent
verified calls may run concurrently. Per-target records separate remote identity,
control sockets, paths, environments, authorization, and target/job-ID pairs.
Existing literal socket collisions must be resolved before dispatch.

New SCG configuration may use the consuming project overlay or the ignored
`.local/remote-compute-ssh/scg-settings.json`. The existing ignored
`.local/compute-scg/settings.json` is preserved and remains a supported fallback.
Project configuration takes precedence, then the new location, then the legacy
file; conflicting settings require resolution. Private settings are read as data,
never shell-sourced or copied into public files. Installed `remote-compute-ssh`
links already resolve to this checkout; no installed `compute-scg` entry exists
in the checked discovery directories.

## Validation and limits

- Twelve helper tests pass, covering all ten inherited behaviors plus concurrent
  distinct-server sockets and all four combinations of two hosts/two accounts.
  Real OpenSSH expands configuration; fake remote responses and temporary local
  sockets avoid credentials and cluster access. These tests do not demonstrate
  live SCG/Sherlock authentication or concurrent cluster jobs.
- Helper and both Slurm templates pass Bash syntax checks. The templates remain
  starting points that require actual user settings, current access checks, and
  authorized submission.
- Registry validation passes with 23 skills and 23 profiles. The public-content
  scan, whitespace, all 11 local Markdown links, source-preservation audit, and
  retired-discovery checks pass. Installed Codex and Claude links resolve to the
  updated canonical source. CI now runs the remote-compute helper tests alongside
  the existing registry/figure checks.
- The public diff contains reusable workflow text, public source links, templates,
  and synthetic test identities. Private settings and machine-specific installation
  details remain outside the public change. No cluster connection, job submission,
  cancellation, or dataset transfer is part of this task.
