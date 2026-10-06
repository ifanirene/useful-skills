# Set up an SSH account and connection sharing

Ask for an existing SSH alias first. Otherwise obtain the user's cluster login
hostname and username. For SCG use the user's own SUNet ID and the public login
host `login.scg.stanford.edu`. Account registration, lab affiliation, allocations,
and any required VPN access are separate from SSH setup; consult
[SCG Quick Start](https://login.scg.stanford.edu/quick_start/) for access steps.

## Sherlock first-time setup

For Sherlock, read the official [account prerequisites](https://www.sherlock.stanford.edu/docs/getting-started/)
and [connection guide](https://www.sherlock.stanford.edu/docs/getting-started/connecting/).
A new user needs an active SUNet ID and a Sherlock account. The sponsoring
Stanford faculty member requests the account from `srcc-support@stanford.edu`,
providing the research team members' names and SUNet IDs. A SUNet ID or an SCG
account alone does not establish Sherlock access.

Once the account is active, the user can connect from their own computer's
Terminal without an agent or this helper:

```bash
ssh YOUR_SUNET_ID@login.sherlock.stanford.edu
```

Compare the first-connection host-key fingerprint with the official connection
guide, then enter the SUNet password and complete Duo in Terminal/on the user's
device. Sherlock's [authentication guidance](https://www.sherlock.stanford.edu/docs/advanced-topics/connection/)
states that SSH public-key authentication is unsupported; do not suggest
`ssh-copy-id` or key-only login tests for Sherlock. Recheck site policy
if troubleshooting a changed authentication method.

For a convenient Terminal alias, add this focused block to `~/.ssh/config`,
using the file permissions and existing-config checks described below:

```sshconfig
Host sherlock
    HostName login.sherlock.stanford.edu
    User YOUR_SUNET_ID
    ControlMaster auto
    ControlPath ~/.ssh/cm-%C
    ControlPersist 12h
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

Then `ssh sherlock` opens a normal interactive session. From the skill directory,
`bash scripts/ssh-connect --host sherlock` establishes/verifies a reusable
connection; subsequent agent calls add `--non-interactive`. Connection sharing
reduces repeated Duo prompts while that authenticated connection remains alive.
Keep computation in Slurm jobs rather than on login nodes.

## Connect without an existing alias

Use the user's own account and the supplied hostname:

```bash
bash scripts/ssh-connect --host login.scg.stanford.edu --user YOUR_CLUSTER_USERNAME
```

The helper uses standard OpenSSH and creates private connection-sharing state
if needed. It does not require a pre-existing SSH config or another agent's
files. Select another state directory with `--socket-dir PATH` if desired.
Use the same host/user/socket options when another agent invokes the helper.
After initial authentication, agent calls should add `--non-interactive` and
can add `--command 'hostname; whoami'` to execute through that connection.

## Optionally configure a local alias

First inspect the relevant existing configuration with `ssh -G SSH_ALIAS`.
If setup is requested, add a focused entry without replacing unrelated blocks.
Have the user replace `YOUR_CLUSTER_USERNAME` with their own account:

```sshconfig
Host scg
    HostName login.scg.stanford.edu
    User YOUR_CLUSTER_USERNAME
    ControlMaster auto
    ControlPath ~/.ssh/cm-%C
    ControlPersist 12h
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

Use a different alias/hostname for another cluster. A 12-hour idle period is a
convenience suggestion, subject to the user's preferences and site rules. Keep
the socket in a directory only the user can access. Create `~/.ssh` if needed
with mode 700; keep a newly created config private with mode 600. Never commit
the populated configuration. Verify the effective hostname, username, and
ControlPath before connecting. SCG documents connection reuse in its
[ControlMaster guide](https://login.scg.stanford.edu/tutorials/ssh_controlmaster/).

For a new host, confirm its host-key fingerprint against a trusted site source
before accepting it. Resolve host-key changes through the site administrator.

## Authenticate using the bundled helper

From the skill directory, run in a user-interactive terminal:

```bash
bash scripts/ssh-connect --host scg
```

Complete authentication in the terminal and any Duo approval on the user's own
device. Future calls can use `--non-interactive`; this mode never asks for a
password. It exits with an actionable message if recovery needs user input.

The helper verifies the shared socket and live remote response. It creates
connection-sharing state when absent, but does not edit SSH configuration.
Exit codes: 0 = connection verified; 2 = connection/setup/input failure.
Remote commands and authentication may return OpenSSH's or the command's
own exit code; a failed remote command is not itself an authentication failure.

## Optional SSH key setup

Follow the cluster's key policy. Reuse an appropriate existing key; do not
overwrite one. When key setup is requested and allowed, help the user generate
a dedicated key with a passphrase and register only its public half using an
authenticated connection or the site's approved procedure. Keep private keys
on the user's machine and never collect them in chat or the shared skill.
Do not promise key-only login: two-factor requirements can still apply.

The helper source is bundled in `scripts/ssh-connect`. Run it from the skill
directory; no separate helper installation or agent-specific files are needed.
