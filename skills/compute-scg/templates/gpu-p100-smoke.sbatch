#!/usr/bin/env bash
# SCG GPU detection template, authored 2026-10-05; not run as supplied.
# Historical 2026-07-09 evidence covers partition/account/P100 detection only;
# the CPU/memory/time values below are new modest suggestions.
# Replace REPLACE_LAB_ACCOUNT; check current GRES/access and GPU authorization.
#SBATCH --job-name=scg-p100-smoke
#SBATCH --account=REPLACE_LAB_ACCOUNT
#SBATCH --partition=nih_s10
#SBATCH --gres=gpu:p100:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:05:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

set -euo pipefail
export PYTHONUNBUFFERED=1
printf 'Job %s on %s\n' "$SLURM_JOB_ID" "$(hostname)"
printf 'CUDA_VISIBLE_DEVICES=%s\n' "${CUDA_VISIBLE_DEVICES:-unset}"
nvidia-smi -L
nvidia-smi --query-gpu=name,memory.total,utilization.gpu --format=csv
# Add the project's framework/allocation check separately; detection alone
# does not validate application compatibility or scientific results.
