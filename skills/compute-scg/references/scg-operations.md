# SCG Slurm and project operations

## Sources and evidence status

Derived from investigator-supplied Claude Science compute notes covering
2026-07-09 through 2026-08-09, selected by the investigator on 2026-10-05:
account/partition and billing rules; dated CPU/GPU settings; parameterized
environments/storage; unbuffered logs, SIGPIPE and absolute input paths.
Personal paths, internal endpoints and app-specific authentication mechanics
were removed. No cluster login or job was performed when creating this skill.

Official references checked 2026-10-05:
[accounts](https://login.scg.stanford.edu/faqs/account/),
[job scripts](https://login.scg.stanford.edu/tutorials/job_scripts/),
[GPUs](https://login.scg.stanford.edu/tutorials/gpus/), and
[Quick Start](https://login.scg.stanford.edu/quick_start/).
Live scheduler state takes precedence over dated examples. Record observation
date, account/partition/QOS and validation level when refreshing a lab profile.

## Private lab configuration

Keep real accounts, usernames, environment paths and storage in an ignored
project overlay or `.local/compute-scg/settings.json` in this registry. A lab
can distribute that overlay privately. Do not commit it or assume it accompanies
a public clone. Example fields (placeholders, not executable configuration):

```json
{
  "ssh_alias": "YOUR_ALIAS",
  "accounts": {"interactive": "default", "batch": "LAB_ACCOUNT",
    "nih_s10": "LAB_ACCOUNT", "gpu_short": "LAB_ACCOUNT",
    "gpu_normal": "LAB_ACCOUNT", "gpu_long": "LAB_ACCOUNT"},
  "billing_requires_approval": true,
  "gpu_requires_approval": true,
  "conda_base": "ABSOLUTE_CONDA_BASE",
  "environment": "ENV_NAME_OR_ABSOLUTE_PREFIX",
  "work_dir": "ABSOLUTE_SHARED_PROJECT_DIRECTORY"
}
```

These mappings reflect one user's historical lab profile, not access granted
to all users. Discover each member's actual associations first. Use the approved
user-facing lab account; do not substitute a hidden/internal remapped account
merely because it appears in accounting output. The source profile treats batch
as billed and requires approval for GPU/NIH requests; preserve already-granted
authorization and confirm current billing policy with the lab.

## Discover access, limits and GPU state

Run lightweight read-only queries on SCG:

```bash
scgwhoami
sinfo -o '%P %a %l %D %t %G'
sinfo -N -o '%N %P %t %G'
scontrol show partition interactive
sacctmgr -n -P show qos format=Name,MaxTRESPU
squeue -u "$USER"
```

Inspect the chosen partition and applicable account associations/QOS, not just
all QOS records. If the accounting query is unavailable, report that limit and
use project instructions/admin guidance. `sinfo` reports partition time limits,
node states and configured GRES; it alone does not establish user access, QOS
ceilings or exact free GPUs on a mixed node. For candidate nodes, inspect
`scontrol show node NODE_NAME` (including configured/allocated TRES). User access,
GPU model/VRAM, current allocation and pending reasons are separate observations.
Idle hardware does not guarantee scheduling priority. Start estimates, when
available from `squeue --start -j JOBID`, are tentative.

## Dated observations from the source notes

| Date | Settings/observation | Evidence and use |
| --- | --- | --- |
| 2026-07-09 | `nih_s10`, approved lab account, `--gres=gpu:p100:1` | `nvidia-smi` completed on P100 16 GB. Detection smoke only; test current access and application compatibility. |
| 2026-07-09 | H200 on `gpu_short`; A100 on `batch` | Submissions accepted, remained pending for Priority, cancelled before execution. No successful run evidence or reusable wait-time estimate. |
| 2026-07-09 | `interactive`, `default`, `--gres=gpu:1` | Rejected: no GPU GRES exposed at that snapshot. Official GPU documentation describes interactive GPUs; resolve this discrepancy through live state and `sbatch --test-only`. |
| 2026-07-31 | Interactive QOS reported CPU 16, memory 128G, GPU 1; partition time 24h | QOS GPU allowance does not establish partition GPU hardware/access. Recheck applicable limits and concurrent per-user usage. |
| 2026-07-31 | CPU 12, memory 120G on interactive | Source reports successful submissions. These are workload-specific settings, not a new-user default. |
| 2026-08-08 | Interactive, CPU 8, memory 120G | Source reports repeated successful approximately 2h Scanpy runs on 190k cells. A 180G request was rejected; use another authorized partition for genuine higher-memory needs. |

These are reports supplied by the investigator, not independently revalidated
job records. P100 detection says nothing about H200/A100 runtime readiness.

## Resource selection and submission

Start small for exploration (historical suggestion: 2-4 CPUs, 32-64G, 2-4h),
but choose from data size, algorithm, effective parallelism and pilot evidence.
Do not turn these into required minimums; GPU detection needs much less.
Use completed job `seff`/`sacct` CPU efficiency, peak memory and elapsed time to
adjust the next request with sensible headroom. Peak memory may be reported
per step/task and may miss brief peaks; interpret it with logs and job shape.
A faster GPU is useful only when VRAM, supported CUDA/framework versions and
workload scaling justify it. Request one GPU for initial compatibility checks.

Normally set `--nodes=1 --ntasks=1`, explicit `--cpus-per-task`, `--mem` and
`--time`; bind application thread counts to the allocation. Arrays suit
independent samples, subject to authorized total size and concurrency.
Render template placeholders before submission: `#SBATCH` values do not expand
shell variables. Ensure output directories exist before `sbatch` (Slurm opens
logs before shell commands run). `sbatch --test-only SCRIPT` checks acceptance;
it does not run the script, check its environment or prove immediate capacity.
After authorization, submit with `sbatch --parsable SCRIPT`; record its job ID
and check `squeue`, `sacct`, logs and intended outputs. Do not duplicate a job
whose state is unknown or cancel/resubmit outside existing authorization.

## Project environments and durable storage

Read remote project instructions. Discover available modules (`module avail`),
existing Conda environments (`conda env list`) and project dependency files.
Confirm the environment with version/import checks inside a small Slurm job;
login-node success does not establish compute-node compatibility.
Source `CONDA_BASE/etc/profile.d/conda.sh` using the user's discovered base, then
activate the confirmed environment name/prefix. An absolute interpreter path
may suffice for simple Python work; use activation when hooks/libraries need it.

Historical source examples include Seurat 4/R 4.2 and a Python 3.12 Scanpy
project environment. Do not prescribe those versions or another user's paths.
Install into an authorized project environment, respecting current permissions;
never alter system/base environments. The source notes both ask-before-install
and later user-specific permission to install; that later permission does not
apply to other lab members.

Historical nodes had GCC 4.8.5 and glibc 2.17. Check `gcc --version` and
`ldd --version` on the target nodes before choosing binaries/build tools.
Prefer compatible Conda binaries; for pip, require available compatible wheels
when no suitable compiler exists. Older notes suggest Python 3.11 for wheel
coverage, not a permanent version rule. Avoid blindly recreating personal
`pip freeze` exports or changing `.condarc` defaults. Store durable inputs,
outputs and environments on the user's confirmed shared home/Oak/lab storage;
node-local temporary storage is disposable, not the sole result copy.

## Reliable paths, live logs and exit diagnosis

- Resolve inputs and output paths before `cd`; capture
  `JOBDIR="${SLURM_SUBMIT_DIR:-$PWD}"` when staged files are relative to the
  submission directory. Prefer explicit absolute arguments for durable files.
- Use `export PYTHONUNBUFFERED=1` or `python -u` for live Python progress.
  `conda run --no-capture-output` alone does not disable Python buffering.
- Under `set -o pipefail`, `producer | head` can cause producer SIGPIPE and
  exit 141. Avoid truncating diagnostic pipelines this way; inspect logs and
  outputs before diagnosing failure. Do not globally ignore exit 141.
- In GPU jobs, record `nvidia-smi -L` and `CUDA_VISIBLE_DEVICES`. Physical GPU
  listings can include GPUs outside the allocation; use the job's visible
  devices. For application jobs, log GPU utilization over time when useful;
  a detection-only smoke test does not demonstrate useful GPU utilization.
