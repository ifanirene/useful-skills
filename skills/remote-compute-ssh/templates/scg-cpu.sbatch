#!/usr/bin/env bash
# SCG CPU starting template, authored 2026-10-05; not cluster-run as supplied.
# Replace all REPLACE_* tokens; verify access/limits and authorize submission.
# Historical modest interactive shape, not the validated 120G analysis itself.
#SBATCH --job-name=scg-cpu
#SBATCH --account=default
#SBATCH --partition=interactive
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --chdir=REPLACE_ABSOLUTE_WORK_DIR
#SBATCH --output=REPLACE_ABSOLUTE_LOG_DIR/%x-%j.out
#SBATCH --error=REPLACE_ABSOLUTE_LOG_DIR/%x-%j.err

set -euo pipefail
# Create log directories BEFORE submission. SBATCH directives are literal.
JOBDIR="${SLURM_SUBMIT_DIR:-$PWD}"
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export OPENBLAS_NUM_THREADS="$OMP_NUM_THREADS"
export MKL_NUM_THREADS="$OMP_NUM_THREADS"
CONDA_BASE='REPLACE_ABSOLUTE_CONDA_BASE'
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate 'REPLACE_ENV_NAME_OR_PREFIX'
printf 'Job %s; submission directory %s\n' "$SLURM_JOB_ID" "$JOBDIR"
python -u 'REPLACE_ABSOLUTE_ANALYSIS_SCRIPT' \
    --input 'REPLACE_ABSOLUTE_INPUT' --output 'REPLACE_ABSOLUTE_OUTPUT'
# Replace the command/arguments with the project's actual interface.
# For billed batch: change partition/account only after access and budget checks.
