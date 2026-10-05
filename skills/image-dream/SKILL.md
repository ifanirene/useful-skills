---
name: image-dream
description: Turn a selected repository element and a personal reference library into recurring artistic cover images. Use to set up Image Dream, generate a dream now, explore styles, or configure its scheduled runs.
license: NOASSERTION
---

# Image Dream

Create a small visual surprise rooted in the user's actual work: one recognizable repository
element, interpreted through a fresh artistic direction. A useful dream feels connected to
its source even without a caption. It is an editorial artwork, not a fabricated research result.

## Set up a dream

Read [configuration.md](references/configuration.md) when setting up or changing a series.
Resolve the repository, selected element, and personal library from the user's request or
existing configuration. A library may contain images, style notes, prior covers, scientific
material, or reusable visual skills; establish which role each source plays. Do not assume
that a code repository or a folder of papers is an image library.
For a ChatGPT Library source, read [chatgpt-library.md](references/chatgpt-library.md).

Save a private series configuration outside the shared skill package. Confirm missing paths
and the intended element, but carry forward information and authorization already supplied.
Default creative choices are one image, landscape 16:9, no visible text, moderate artistic
freedom, and a different suitable style from recent runs. A supplied preference wins.

Separate making the reusable skill from activating a real schedule. For a scheduled series,
read [scheduling.md](references/scheduling.md); obtain its cadence/timezone and verify the
chosen host can access the source, library, and image generator unattended. Once configured
and authorized, routine runs do not need another style-selection question.

## Run a dream

1. **Recover the series.** Read the private configuration and recent run records. For a
   scheduled run use its stable occurrence key, not the current second. Use the run helper
   below to reserve the occurrence before any image call. A duplicate reservation means
   inspect the existing result and stop; do not generate another image for that occurrence.
2. **Ground one element.** Read the configured source file/section or inspect the chosen
   object. With a topic selector, search only the configured scope and pick one concrete
   element. Write its source path and location, a content fingerprint or Git revision, and
   the short idea the artwork should express. Missing source/library: record blocked and
   notify only when this is a new or changed blocker. Do not substitute an unrelated topic.
3. **Use the library deliberately.** Inspect a small relevant selection (normally 1–3
   references), including the images themselves. Separate subject/anatomy references from
   style/mood references. Read relevant style notes. Preserve the subject's defining
   structure; borrow medium, palette, texture, lighting, or composition from style references.
4. **Choose a fresh direction.** Consult [art-direction.md](references/art-direction.md) when
   choosing or changing style. Prefer a direction not used in the last few successful runs.
   Keep the conceptual connection clear; do not rotate styles mechanically when they obscure
   the element. For a fixed source, explore a new visual interpretation even if Git is unchanged.
5. **Save the brief and complete prompt before rendering.** Include source identity, selected
   references and their roles, what must stay true, chosen artistic treatment, composition,
   aspect ratio, and excluded visual inventions. Use the actual source rather than generic
   decorative imagery. Do not add headings, branding, or captions inside the image by default.
6. **Render through an available image backend.** Read the host image-generation skill and
   use its current tool schema. Native image generation is the default; the installed
   `image-generation` skill is an alternative when the user has selected/configured its API
   workflow. Baoyu style references may inform art direction if available; Image Dream does
   not require Baoyu's article insertion workflow. Do not substitute an HTML/SVG mockup for a
   requested generated artwork. Missing backend: record blocked, not successful.
7. **Inspect and deliver.** Check the actual image for a recognizable source element, artistic
   intent, distracting defects, unintended text, and any scientific misrepresentation.
   Save it in this run's directory and finish the run record. Return the image, a brief title,
   and one sentence explaining the source connection and style experiment. Append a linked
   entry to the series gallery, preserving earlier entries. Record explicit user feedback
   about favorites or disliked styles in the private series preferences.

For scientific elements, preserve the invariants that carry meaning (for example, branching,
compartments, cell identities, or flow direction). Freely interpret color, texture, light, and
medium where permitted. An abstract metaphor must be described as such; it must not silently
present a hypothetical mechanism as established anatomy or data.

## Run records and bounded execution

The standard-library helper [dream_runs.py](scripts/dream_runs.py) manages an exclusive run
reservation and verified local artifact paths; it does not generate images or schedule jobs.
Resolve it from this skill's real directory before invoking it.

```bash
python3 scripts/dream_runs.py reserve --output OUTPUT_DIR --key OCCURRENCE_KEY
python3 scripts/dream_runs.py finish --output OUTPUT_DIR --key OCCURRENCE_KEY --status complete --image IMAGE_PATH --prompt PROMPT_PATH --brief BRIEF_PATH --note "Visual inspection passed"
python3 scripts/dream_runs.py finish --output OUTPUT_DIR --key OCCURRENCE_KEY --status blocked --note "Configured library is unavailable"
```

Use a distinct output directory per series. `reserve` returns `claimed: true` only for a new
occurrence. Existing or interrupted occurrences return `claimed: false`; inspect before
resuming. An uncertain backend response must not trigger a blind repeat call. Reconcile any
returned assets first. Do not retry a failed/blocked occurrence automatically. A user-requested
retry gets a new, linked key. Ignore unrelated ongoing runs or tasks.

Default total generation calls per occurrence: one. If the series explicitly allows a second
attempt, preserve the first candidate, save the revised prompt, and stay within that limit.
Never describe a failed visual check as complete to satisfy the schedule. Track failed attempts
and their reason without deleting their artifacts. Do not accumulate missed runs by default.

## Outputs and completion

Each run contains `run.json`, `brief.md`, `prompt.md`, and the actual generated image when
successful. The private output root contains `gallery.md`, linking completed runs and their
source/style notes. Exact backend/model metadata should be recorded when exposed; use
`unavailable` when the backend does not report it.

A successful run has a source-grounded brief, inspected references, a saved generation prompt,
a real image visibly reviewed by the agent, and a matching gallery entry. Setup reports
whether scheduling is active, its next run if known, and any missing operational input.
Installing or validating this skill does not itself establish live generation or scheduler
reliability. Never commit private source material or generated dreams into this skill library.
