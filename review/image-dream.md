# Image Dream review packet

## Result

Original skill for recurring artistic covers rooted in a selected repository element and a
personal reference library. Supports ChatGPT Library through verified browser access or a
private cache, optional existing generation backends, fresh art direction, source invariants,
saved prompts, visual review, gallery history, and host-native automation configuration.

## Scope and provenance

One new skill and discovery profile; synchronized manifest, README, routing, changelog, and
provenance. Original instructions and standard-library Python helper. Optional Baoyu and
image-generation skills are referenced, not copied. Redistribution license is unassigned.
Prior Baoyu integration changes on this review branch remain intact.

Private library selections, account details, repository targets, reference caches, generated
images, and actual schedules stay outside public files. The helper performs no network calls,
generation, scheduling, credential reads, or repository source edits.

## Verification

Run helper tests, skill validation, reference-path audit, registry/privacy/whitespace checks,
and Codex/Claude discovery checks. Run tests use synthetic temporary artifacts; a passing test
does not imply aesthetic quality, scientific accuracy, or unattended backend availability.
Validation results are appended after execution.

## Functional cases for review

- A scheduled slot is delivered twice: only the first caller can reserve it for generation.
- An initialized run is interrupted: a later wake must not silently generate a duplicate.
- A library or generator is unavailable: record blocked; do not invent references or output.
- Source is unchanged: a fresh artistic interpretation is still valid when a new slot is due.
- ChatGPT image titles are accessible but no asset is inspected: do not claim visual review.
- A saved library image was rejected: do not infer a favorite merely from presence or recency.
- No cadence or repository element is configured: finish the reusable skill, not a fake schedule.

## Review state

Local review branch, not published or merged. Functional reviewer: pending. Privacy reviewer:
pending. No human approval or review time has been recorded. No active schedule created and
no generated image produced during installation.

Validation completed: six offline run-state tests passed; CLI reserve/replay/blocked
round-trip passed; skill frontmatter validation passed; all local references resolve;
registry passed (17 skills, 16 profiles); public-content scan passed (85 text files);
working and staged whitespace checks passed. Codex and Claude discovery links resolve.
Interactive ChatGPT Library access and rendering of a selected image were verified;
no export, image generation, or unattended scheduling was tested.
