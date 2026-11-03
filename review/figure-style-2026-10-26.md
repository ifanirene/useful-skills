# Figure-style consolidation and Nature guidance

## Scope and authority

The owner requested consolidation of `figure-composer` into `figure-style`,
retirement of the separate root, Nature guidance, explicit colors, and adapted
Engreitz design/legend guidance. The owner subsequently rejected synthetic
teaching examples and required real inspected Nature panels for examples.
The draft simulations and their generation script were removed. No published
panel examples were verified, so none are included.

The owner initially instructed local edits on the current checkout and declined
a new review branch. On 2026-11-03, the owner explicitly requested a direct commit
and push to GitHub without a human review step, and asked to synchronize installed
copies. This supersedes the earlier local-only restriction for this change.
Independent human functional and privacy review was waived, not completed; the
registry's default review policy remains unchanged.

## Changes

- One active figure entrypoint with conditional composition, Nature, color,
  legend, and design references. Sequential work and delegation are both allowed.
- Retired the PNG-tiling and host-SDK composer root. The portable composition
  workflow favors a shared vector canvas or vector-preserving external assembly.
- Authored a shared YAML and independent Python helper: explicit overrides,
  missing-font errors, stable entity colors, fixed physical canvas, editable
  text settings, and export errors propagated to the caller.
- Added actual Nature source links and dated requirements; separated them from
  local design choices and target-journal/editor exceptions.
- Reconciled inherited color/title/layout rules with the new defaults. Removed
  the instruction to invent minimum review findings and fixed panel-count/grid
  prescriptions from the retired workflow.
- Updated manifest, index, profiles, README, agent router, provenance, changelog,
  paper-narrative handoffs, and CI tests.

## Sources and privacy

Public Nature figure/author guidance supplies submission facts. EngreitzLabAgents
at `bd501c4ec697a67fe94c6e7f6ed33ad5e8ae733f` supplies attributed design ideas and
legend-writing patterns. Prose, YAML, and new helper code are locally authored;
no upstream implementation/example text, private data, or artwork is copied.
Its upstream license remains unresolved. The historical Anthropic source URL
gap remains recorded. See the skill's `references/sources.md` for exact files.

X08 changed source use: Nature controls journal requirements; Engreitz informs
composition/legend choices. This avoided inheriting the upstream 247 mm height,
report-specific interpretation requirements, and unverified figure exemplars.
The source paper's artwork was not inspected, limiting example inclusion.

## Verification and limits

Eight helper tests exercise explicit font failure, override precedence and
entity identity, no hue recycling, exact PNG/PDF canvas under stale tight-crop
settings, vector PDF text/drawings, error propagation, raster DPI retention,
text bounds/size checks, and non-rendered off-axis ticks.

The temporary render experiment established export behavior only. It did not
establish visual quality, and the owner rejected those plots as teaching material.
They are not included. Style tests do not verify biology, statistical design,
all overlaps, or journal acceptance. PDF inspection in the test suite requires
PyMuPDF; CI installs it explicitly. Arial availability is checked at use time;
CI's font-independent fixtures are not Nature design exemplars.

Registry, public-content, whitespace, local-reference, and retirement checks are
run on the final local state. Independent agent review found conflicting legacy
color/title rules; these were corrected. No model-performance benchmark or real
manuscript figure production has been completed.

## 2026-11-03 revalidation and installed copies

- All eight figure-helper tests pass, including the PyMuPDF PDF inspections.
  Registry validation reports 24 skills and 24 profiles; the automated
  public-content scan and whitespace check pass. All 19 local Markdown links in
  the affected skill directories resolve. All nine pinned upstream worktrees are
  clean and match their registered commits; this is not an upstream version upgrade.
- The canonical registry already contains the owner's updated figure workflow.
  The remaining local drift came from an older installed `figure-style` directory,
  two `remote-compute-ssh` copies missing license metadata, and an installed retired
  `figure-composer`. Existing directories were moved to backups outside discovery
  before creating links or archiving the retired entry. All previously installed
  active registry skills now resolve to the canonical library.
- The installed-copy audit and backup paths remain in ignored local storage.
  No credentials, private project data, machine paths, or generated installation
  links are included in the public change. Export tests establish software
  behavior; they do not add published teaching examples or establish scientific
  validity or journal acceptance.
