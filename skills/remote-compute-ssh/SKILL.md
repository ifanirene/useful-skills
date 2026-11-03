---
name: remote-compute-ssh
description: Set up or reuse SSH connections to one or more servers, including SCG and Sherlock, transfer files, and submit or monitor Slurm jobs. Includes selective SCG guidance and a standalone connection helper.
license: NOASSERTION
---

# Remote compute over SSH

Use the terminal or remote-execution tools available in the current agent.
All helper code is included in this skill. Runtime requirements are Bash 3.2+
and OpenSSH with `ssh -G`, plus standard Unix utilities on macOS or Linux.
Other platforms can use a compatible Unix environment.

## Establish the user's settings

Establish the selected server or servers, their existing SSH aliases or hostnames,
and the user's accounts. Ask only for settings missing from the request or known
project configuration. Account enrollment and compute allocations are separate
from SSH setup.

- For a selected **SCG** target, read [SCG operations](references/scg-operations.md)
  before onboarding or preparing jobs. It contains SCG access, private lab
  configuration, CPU/GPU sizing, templates, and dated observations. Load it only
  for SCG; its accounts and partitions do not apply to other clusters.
- For first-time access or local aliases, read [connection setup](references/setup.md).
  Its Sherlock section covers enrollment and authentication. Sherlock's documented
  policy does not support SSH public keys, so skip key setup and key-only tests there.

Inspect only the relevant alias with `ssh -G SSH_ALIAS`. Confirm the resolved
hostname and username before connecting. If the alias is absent or resolves
to a different account, use explicit `--host HOSTNAME --user USERNAME` settings
or [references/setup.md](references/setup.md) to help configure an alias.
Preserve unrelated SSH settings. Keep usernames, private keys,
passwords, lab allocations, and private storage paths out of the shared skill.
Use the active user's local configuration; never copy another person's setup.

## One or several servers

A single-server task uses one helper invocation per operation. When the user
selects several targets, read [multiple servers](references/multiple-servers.md)
before connecting or dispatching commands. Keep each target's connection, working
directory, environment, authorization, and job records separate. Successful
authentication or job approval on one target does not establish either on another.

## Reuse and recover connections

Resolve bundled paths relative to the directory containing this `SKILL.md`.
The helper source is [scripts/ssh-connect](scripts/ssh-connect).
Run it directly from the skill; it does not require installation in a user's
home directory or another agent's APIs. Substitute the confirmed SSH alias:

```bash
bash scripts/ssh-connect --host SSH_ALIAS --non-interactive
```

For a user without an SSH alias, use their supplied host and account:

```bash
bash scripts/ssh-connect --host HOSTNAME --user USERNAME --non-interactive
```

The helper reuses existing SSH settings. If connection sharing is absent, it
creates a private socket directory and sets sharing options for its own calls,
without rewriting SSH configuration. An optional `--socket-dir PATH` selects
the state location; `--identity PATH` selects the user's own key. The default
socket location is `~/.ssh/ssh-connect`, created as needed, not a required
pre-existing file. The OpenSSH connection hash separates host/account targets.

Successful output proves the server responds, unlike `ssh -O check`, which
proves only that a local master process exists. Any agent with terminal access
can reuse the helper with the same host/user/socket options:

```bash
bash scripts/ssh-connect --host HOSTNAME --user USERNAME --non-interactive --command 'hostname; whoami'
```

Use `--command` for subsequent operations when the helper created the socket
settings. Plain `ssh SSH_ALIAS` will reuse them only if the alias already has
matching sharing configuration. Do not ask for authentication again just
because a new task or turn started. Sharing applies within the same OS user
and workstation; this does not distribute credentials to other machines/users.

If no authenticated connection is available, have the user run the same
bundled helper once in their Terminal, omitting `--non-interactive`, and finish
any password/Duo prompts there. Never request credentials in chat. The helper
will not prompt through a noninteractive terminal, terminate a master, or
rewrite SSH configuration. A locally alive but unresponsive master needs
diagnosis, not an automatic disconnect of the user's sessions.

Distinguish authentication failure from DNS, VPN, timeout, and host-key errors.
Do not disable host-key verification. Retry verification once after recovery;
if it fails, inspect the error instead of looping the helper or repeatedly
asking the user for the same action. Keep an unanswered authentication request
pending. Use the setup reference for account enrollment or an optional alias.

## Keys and two-factor authentication

Follow the selected server's authentication policy. Keys may replace the first
authentication factor while the server still requires Duo; an installed or
accepted key does not establish unattended access.
Reusing a master avoids repeated prompts without changing server requirements.
Connection persistence is an idle period, not a Slurm job time limit.

Only test fresh key-only login when diagnosing authentication or when requested:

```bash
ssh -o ControlPath=none -o BatchMode=yes -o PreferredAuthentications=publickey -o ConnectTimeout=10 SSH_ALIAS 'echo OK'
```

"Partial success" means another factor is required. A successful test establishes
key-only access for that user and host at the time of testing.

## Remote files and jobs

- Discover remote identity, home, and paths with a lightweight command such as
  `bash scripts/ssh-connect --host SSH_ALIAS --non-interactive --command 'hostname; whoami; pwd'`.
  Ask for the project's storage location; do not assume a lab name or Oak path.
- Inspect remote project instructions and environments before editing or
  running analyses. Local files and environments are not automatically remote.
- On Slurm clusters, keep login nodes for light inspection, orchestration, and
  job monitoring; run analyses through Slurm. Discover tools, accounts, partitions,
  and limits from project instructions or read-only scheduler queries. Login
  node hardware is not a resource budget. SSH access does not imply GPU access.
- Carry forward existing authorization for the selected target. Obtain any
  missing approval for billed submissions, GPUs, large arrays, cancellation or
  resubmission, and material budget increases. Do not ask again for jobs within
  an approved envelope. Every job needs explicit walltime, CPUs, and memory;
  request GPUs only when useful. Reuse suitable environments,
  respect installation permissions, and keep durable results on confirmed shared
  storage. Use Slurm commands only on targets running Slurm.
- Stage authorized inputs with `scp`, `sftp`, or `rsync`; verify paths and
  transfers. Keep large remote datasets remote and retrieve selected outputs.
- Submit prepared scripts with `sbatch --parsable`; retain the script,
  account/partition, environment, target plus job ID, working directory, and output
  paths. Inspect existing jobs before resubmitting. Monitor with `squeue`/`sacct`;
  do not duplicate a job whose status is unknown or increase costs without authorization.
- Check scheduler state, exit code, logs, and output files before claiming
  completion. SSH disconnection does not itself cancel submitted jobs. Retain
  results unless cleanup is part of the request.

## Completion and portability

Report per target the connection mode actually verified, remote identity, jobs
run or still pending, checked outputs, deliverable paths, and remaining failures.
When already on the cluster, use local commands rather than this workstation's
SSH recovery workflow.

Share the whole skill directory, including `scripts/`, `references/`, and `templates/`.
Do not distribute credentials, sockets, personal SSH config, or local job data.
For bundled helper tests, run `python3 -m unittest discover -s tests` from the
skill directory; Python is needed only for these tests, not for the helper.
