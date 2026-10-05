# Private series configuration

Use a readable Markdown file in the requesting project's ignored local storage, or another
user-selected private directory. Keep its exact path available to the scheduler. Do not write
machine paths, personal library contents, or source excerpts into the public skill package.

## Minimum operational inputs

- Repository: an existing checkout accessible to the execution host.
- Element: a file and section/object, or a bounded topic selector within specified paths.
- Personal library: existing reference paths or a verified ChatGPT Library selection, with
  roles (subject, style, or inspiration).
- Output: a private directory for this series; separate from the library and source files.
- Backend: native image generation, or an explicitly configured available alternative.
- For scheduling: cadence, local time, timezone, and notification intent.

Ask only for unresolved inputs. A user request to build the capability does not supply a real
repository, library, or cadence. Do not invent them or activate a placeholder schedule.
A generator API key is never an input to store in the series file; use the host's configured
credential mechanism.

## Copyable series template

```markdown
# Image Dream series

Repository: <existing repository>
Element: <file and section/object, or bounded topic selector>
Library provider: local or ChatGPT Library
Library access: browser session or verified private local reference cache
Library:
- <reference path>: subject structure
- <reference path>: palette/texture inspiration
Output: <private output directory>

Intent: Make a surprising artistic cover connected to this element.
Must preserve: <defining structures or relationships>
May reinterpret: color, medium, texture, light, composition
Avoid: <unwanted styles or content>
Aspect ratio: 16:9
Visible text: none
Style policy: explore; avoid repeating the last three completed styles when possible
Preferred styles: <optional list; otherwise use Image Dream's art-direction guide>
Backend: native
Images per run: 1
Maximum generation calls per occurrence: 1

Schedule: <cadence, local time, timezone; inactive until configured>
Occurrence key: <stable scheduled slot in that timezone>
Catch-up: newest due slot only
Notify: each completed image; new or changed failure requiring action
Automation ID: <record after scheduler confirms creation>
```

Place this configuration and run output in already ignored storage, or add a narrowly scoped
ignore entry after checking project instructions. Do not change repository-wide settings.
Resolve relative input paths against the repository root; resolve the output directory to a
stable absolute path before scheduling. Read sources in place; leave repository content intact.

## Brief template

```markdown
# <Dream title>

Element: <specific subject>
Source: <file:section or other precise location>
Source version: <Git revision plus content hash for dirty/untracked input, or content hash>
Meaning: <one-sentence connection to the work>
References: <file and role for each inspected reference>
Invariants: <what remains recognizable and correct>
Art direction: <medium, palette, texture/light, composition>
Novelty: <how this differs from recent dreams>
Backend/model: <observed value, or unavailable>
Visual check: <actual findings after generation; pending before generation>
```

A failed visual check belongs in a failed run with its candidate retained. A completed gallery
entry links the image, brief, and prompt and records the style and source. Gallery maintenance
must preserve previous entries and avoid duplicate occurrence keys. User preference updates
belong here, not in the reusable skill or unrelated agent memory.
