# Work with several servers

Use this reference when the user selects two or more remote targets. One Mac
can keep independent SSH connections to SCG, Sherlock, and other servers, and
submit separate jobs to their schedulers. A single-server task needs no extra
connections. The helper accepts one target per invocation; repeat it for each
selected server rather than passing several `--host` options to one call.

## Identify each target

Keep a private per-target record of the alias, resolved hostname/user/port,
effective control socket, project directory, environment, and authorized resource
envelope. For a Slurm target, include account, partition, and job IDs. Establish
these settings from the user's request and each target's project instructions;
one server's access, filesystem, environment, or approval does not establish
another's. Load the SCG reference only for SCG targets.

Inspect each alias with `ssh -G SSH_ALIAS`. A shared socket directory is fine,
but different host/user/port targets must resolve to distinct sockets. The helper's
default `cm-%C` incorporates the destination identity. If existing configuration
uses one literal `ControlPath` for several servers, choose distinct
`--socket-dir` values or correct the relevant alias configuration before commands
are sent. Preserve an existing working connection while resolving another target.
See [OpenSSH ControlPath and tokens](https://man.openbsd.org/ssh_config).

## Connect and dispatch

For confirmed aliases, establish each connection once in the user's Terminal,
completing each target's required authentication separately:

```bash
bash scripts/ssh-connect --host scg
bash scripts/ssh-connect --host sherlock
```

These are illustrative selected targets, not instructions to connect to both for
every task. Aliases must already point to the user's intended accounts. Later
operations use the same target/user/socket options and `--non-interactive`:

```bash
bash scripts/ssh-connect --host scg --non-interactive --command 'hostname; whoami; pwd'
bash scripts/ssh-connect --host sherlock --non-interactive --command 'hostname; whoami; pwd'
```

Authenticate interactively one target at a time. Independent verified operations
may run concurrently using separate helper processes when authorized. Direct every
command to its explicit target and use that target's confirmed absolute paths and
environment. A connection failure on one server should not restart or close the
other servers' sessions. Report each result separately.

## Jobs, transfers, and completion

- Track jobs by **target plus job ID**. Job IDs can overlap between clusters;
  run `squeue`, `sacct`, or an authorized cancellation on the recorded target.
- Discover each cluster's accounts, partitions, limits, and environment. Use the
  SCG templates only for SCG; Sherlock and other targets need their own settings.
- Record output paths with their target. Data may be shared or separate; verify
  visibility instead of assuming a matching pathname identifies the same file.
  Move data only within the requested scope, with explicit source/destination
  servers and verification after transfer. Connection setup alone does not
  authorize copying datasets between servers.
- Report per target: connection verification, submitted/running/completed jobs,
  output checks, and remaining failures. Distinguish a queued job, a completed
  detection smoke test, and a verified application result.
- Shut down only the requested target using the matching socket and host/user
  options in [connection setup](setup.md). Closing SSH does not itself cancel
  submitted Slurm batch jobs.
