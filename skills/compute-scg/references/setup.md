# SCG connection from the user's computer

Use the official [SCG Quick Start](https://login.scg.stanford.edu/quick_start/)
for enrollment and [connection guide](https://login.scg.stanford.edu/tutorials/connecting/)
for current authentication policy. An active SUNet ID alone does not grant SCG
membership; follow SCG's access process for the user's lab.

On macOS/Linux, the user can open Terminal and connect without an agent:

```bash
ssh YOUR_SUNET_ID@login.scg.stanford.edu
```

Check a new host's fingerprint against a trusted site source before acceptance.
Complete authentication in Terminal and Duo on the user's own device. Public
keys are a first factor, not a promise of login without Duo. For Windows,
ordinary SSH can run from its OpenSSH client; the bundled Bash helper requires
a compatible Unix environment such as WSL, with separate local configuration.

## Optional local alias

Inspect an existing alias with `ssh -G scg`; preserve unrelated configuration.
When setup is requested, add a focused block to the user's `~/.ssh/config`:

```sshconfig
Host scg
    HostName login.scg.stanford.edu
    User YOUR_SUNET_ID
    ControlMaster auto
    ControlPath ~/.ssh/cm-%C
    ControlPersist 12h
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

Create `~/.ssh` with mode 700 if absent and a new config with mode 600. The user
can then run `ssh scg` for a shell. Connection sharing follows SCG's
[ControlMaster guidance](https://login.scg.stanford.edu/tutorials/ssh_controlmaster/).

From the skill directory, run the bundled helper in the user's Terminal:

```bash
bash scripts/ssh-connect --host scg
# Without an alias:
bash scripts/ssh-connect --host login.scg.stanford.edu --user YOUR_SUNET_ID
```

The helper verifies remote responsiveness and reuses an authenticated master.
When sharing settings are absent it creates private socket state under
`~/.ssh/ssh-connect`; it does not edit SSH config. Later agent calls use the
same host/user/socket options, adding `--non-interactive` and optionally
`--command 'hostname; whoami; pwd'`. Plain SSH shares the connection only when
its socket settings match. Do not copy credentials or sockets between users.

The helper defaults to 12 hours of idle persistence when no effective timeout
is present. Existing configured timeouts are preserved, except the helper
currently treats numeric `0` as unset; use `ControlPersist yes` for indefinite
client-side persistence. Network/server interruptions, sleep or shutdown can
end it earlier. A master opened from Terminal survives closing the chat app.

## Explicit shutdown

When the user requests shutdown, inspect the effective socket and confirm the
target. With the alias configuration above, `ssh -O exit scg` closes the master
and can disconnect its attached sessions. For helper-created settings, use
`ssh -S /ABSOLUTE/CONTROL_SOCKET -O exit TARGET` with the matching resolved socket
and host; do not guess a socket. Submitted Slurm jobs continue independently.

This variant does not require Claude Science or its app-specific socket links.
