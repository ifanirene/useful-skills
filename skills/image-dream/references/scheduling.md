# Scheduled Image Dream

A skill supplies instructions; a scheduler supplies future execution. Keep this distinction
visible to the user. A saved configuration or generated prompt is not an active schedule.

## Establish the recurring contract

Resolve cadence, local time/timezone, series configuration, execution host, and occurrence key.
A daily series can use its scheduled local date as the key; a more frequent series needs the
full scheduled slot with offset. Repeated checks of the same slot must use the same key.
Skip older missed slots unless the user requests catch-up. A fixed source may inspire new
art even without a content change. Do not impose a source-change condition on creative runs.

Use the host's supported automation tool. In Codex, discover `automation_update` and follow
its live schema. A heartbeat attached to the current task is the default for recurring work;
use another kind only when the user's request and host rules call for it. Inspect existing
matching automations and update instead of duplicating them. Preserve unrelated fields and
notification settings. Do not install an OS cron job or a second scheduler as a workaround.

Before scheduling, establish that this execution host can read the configured paths and has
a working image backend for unattended runs. Use a first real dream as the functional check
when authorized by the setup request. A prior successful backend run may establish access;
a visible image tool in an interactive session alone does not prove scheduled availability.
If an unattended backend cannot yet be established, finish the reusable configuration and
state the limitation. Do not claim the schedule is operational until the host confirms it.

## Scheduler prompt template

Replace bracketed inputs with verified values; submit readable prose, not raw directives.

> Run Image Dream using the skill at [resolved skill path] and the private series configuration
> at [resolved config path]. The series is due [cadence, local time, timezone]. On each wake,
> calculate the newest due scheduled occurrence and use that stable slot as the reservation
> key. Read the configuration, inspect the selected repository element and relevant library
> references, and create one artistic image within the configured generation-call limit.
> Save the brief and complete prompt before generation. Inspect the generated image, update
> its run record and gallery, and show the completed image with a short source/style note.
> Preserve earlier images and source files. If this occurrence is already reserved, reconcile
> existing output and do not generate a duplicate. Do not replay missed older occurrences.
> Stay quiet when no occurrence is due or no new actionable result exists. Notify on each new
> completed dream, or a new/changed failure requiring user action; suppress unchanged blockers.

After tool-confirmed activation, store the automation ID and report its schedule and next run
when provided. If the first scheduled execution has not occurred, say so. On a later run that
cannot access the backend, record a blocked result and notify once; do not silently switch to
another paid provider or manufacture an image result. Changes to provider, count, or retry
budget follow the saved user choices and the current request.

The run helper guards one occurrence. When resuming an interrupted run, inspect its files and
backend response before any generation. A reservation with no record means initialization was
interrupted; do not treat that as a fresh unclaimed job. Human-requested retries should link
to the original occurrence and use a distinct key.
