---
name: remote-compute-ssh
description: Set up or reuse a user's SSH connection to SCG or another Slurm cluster, recover shared authentication, transfer files, and submit or monitor jobs. Includes a standalone, agent-independent connection helper.
license: NOASSERTION
---

# Remote compute over SSH

Use the terminal or remote-execution tools available in the current agent.
All helper code is included in this skill. Runtime requirements are Bash 3.2+
and OpenSSH with `ssh -G`, plus standard Unix utilities on macOS or Linux.
Other platforms can use a compatible Unix environment.

## Establish the user's settings

Ask for the user's existing SSH alias or their cluster hostname and username.
`scg` is a suggested alias, not an assumed account. For SCG, the public login
hostname is `login.scg.stanford.edu`; each person supplies their own SUNet ID.
If the user lacks an account, direct them to the cluster's official access
process; SSH configuration cannot grant cluster membership.
For first-time SCG or Sherlock access and local Terminal aliases, read
[references/setup.md](references/setup.md). Sherlock uses
`login.sherlock.stanford.edu`; its documented authentication does not support
SSH public keys, so skip key setup and key-only tests for that cluster.

Inspect only the relevant alias with `ssh -G SSH_ALIAS`. Confirm the resolved
hostname and username before connecting. If the alias is absent or resolves
to a different account, use explicit `--host HOSTNAME --user USERNAME` settings
or [references/setup.md](references/setup.md) to help configure an alias.
Preserve unrelated SSH settings. Keep usernames, private keys,
passwords, lab allocations, and private storage paths out of the shared skill.
Use the active user's local configuration; never copy another person's setup.

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

Keys may replace the first authentication factor while the cluster still
requires Duo. Do not assume an installed or accepted key gives unattended
access. SCG describes keys as a first factor in its
[connection guidance](https://login.scg.stanford.edu/tutorials/connecting/).
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
- Keep login nodes for light inspection, orchestration, and job monitoring.
  Run analyses through Slurm. Discover available tools, accounts, partitions,
  and limits from project instructions or read-only scheduler queries. Login
  node hardware is not a resource budget. SSH access does not imply GPU access.
- Obtain the user's allocation and resource budget before a billed or expensive
  submission. Every job needs explicit walltime, CPUs, and memory; request GPUs
  only when needed. Reuse suitable environments and respect project installation
  rules. Store durable data on the user's confirmed shared storage.
- Stage authorized inputs with `scp`, `sftp`, or `rsync`; verify paths and
  transfers. Keep large remote datasets remote and retrieve selected outputs.
- Submit prepared scripts with `sbatch --parsable`; retain the script,
  environment, job ID, working directory, and output paths. Inspect existing
  jobs before resubmitting. Monitor with `squeue`/`sacct`; do not duplicate a
  job whose status is unknown or increase costs without authorization.
- Check scheduler state, exit code, logs, and output files before claiming
  completion. SSH disconnection does not itself cancel submitted jobs. Retain
  results unless cleanup is part of the request.

## Completion and portability

Report the connection mode actually verified, remote identity, jobs run,
deliverable paths, and remaining failures. When already on the cluster, use
local commands rather than this workstation's SSH recovery workflow.

Share the whole skill directory, including `scripts/` and `references/`.
Do not distribute credentials, sockets, personal SSH config, or local job data.
For bundled helper tests, run `python3 -m unittest discover -s tests` from the
skill directory; Python is needed only for these tests, not for the helper.
