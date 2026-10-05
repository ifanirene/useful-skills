# Provenance

`manifest.json` is the canonical source record. This page explains unresolved history that
cannot be reconstructed safely from the current files alone.

| Skill | Recorded provider | License | Upstream source |
| --- | --- | --- | --- |
| `figure-style` | Anthropic | Apache-2.0 | Owner confirmation required |
| `figure-composer` | Anthropic | Apache-2.0 | Owner confirmation required |
| `paper-narrative` | Anthropic | Apache-2.0 | Owner confirmation required |
| `literature-review` | Anthropic | Apache-2.0 | Owner confirmation required |
| `research-paper-analysis-writing` | grapeot | MIT (README declaration) | `context-infrastructure/rules/skills/workflow_research_paper_survey_writing.md` at `3f62b8b` |
| `ai-programming-mindset` | grapeot | MIT (README declaration) | `context-infrastructure/rules/skills/bestpractice_ai_programming_mindset.md` at `3f62b8b` |
| `skill-writing-principles` | grapeot | MIT (README declaration) | `context-infrastructure/rules/skills/bestpractice_skill_writing.md` at `3f62b8b` |
| `show-me` | HumanLayer | MIT | `humanlayer/skills/plugins/show-me/skills/show-me/SKILL.md` at `3c26291` |
| `writing-workflows` | grapeot | MIT | `https://github.com/grapeot/writing-skill` at `9f2f697` |
| `innovation-assistant` | grapeot | MIT | `https://github.com/grapeot/innovation-assistant-skill` at `e062b37` |
| `ai-session-export` | grapeot | MIT (README declaration) | `https://github.com/grapeot/ai_session_export` at `e52754d` |
| `ai-session-search-archive` | grapeot | MIT (README declaration) | `context-infrastructure/rules/skills/ai_session_search_archive.md` at `3f62b8b` |
| `image-generation` | grapeot | Not declared | `https://github.com/grapeot/image-generation-skill` at `5c1b259` |
| `online-media` | grapeot | MIT | `https://github.com/grapeot/online-media-skill` at `794ff6c` |
| `presentation` | grapeot | MIT | `https://github.com/grapeot/presentation_skill` at `f9881ad` |

These four Skills were already present before the registry conversion. Their files identify
an Apache-2.0 license, and the earlier manifest identified Anthropic as origin, but no precise
upstream URLs were retained. The registry records that gap explicitly instead of inventing
links.

Before publishing a release that claims traceable upstream provenance, the repository owner
should identify and verify those URLs or amend the provider record based on original export
history.

`ai-session-export` is not copied into the registry. Its standalone project is pinned as a
submodule and a small local adapter is the discoverable Skill. The upstream README declares
MIT, but the pinned commit has no standalone license file; human review should resolve or
accept that packaging gap before promotion.

`ai-session-search-archive` adapts one instruction-only Markdown workflow from
`grapeot/context-infrastructure` into the Agent Skills format. The source file has no Skill
frontmatter or executable code. The upstream README declares MIT, but the repository has no
standalone license file; that packaging limitation requires human review before promotion.

`research-paper-analysis-writing` adapts another instruction-only workflow from the same
upstream repository. The local name reflects its stated scope more accurately than the
upstream “survey” filename. The adaptation removes missing internal references and replaces
Tavily/Claude-specific execution assumptions with the local `literature-review` route and
provider-neutral private overlay. The same missing standalone license-file limitation applies.

`ai-programming-mindset` and `skill-writing-principles` adapt two instruction-only best
practices from the same upstream repository. The former narrows broad advice into a diagnostic
workflow and removes fixed orchestration prescriptions. The latter governs Skill content
quality while leaving host-specific packaging and validation to current creation tooling.
Neither source file contains code or private configuration. The upstream README declares MIT,
but the repository has no standalone license file.

`show-me` adapts HumanLayer's instruction-only Agent Skill at the pinned commit. It preserves
the upstream visual formats and examples while replacing the macOS-specific `Bash(open ...)`
instruction with the current host's preview or file-link mechanism. Explicit boundaries and
acceptance checks were added for factual accuracy and restraint. The upstream repository's MIT
license is included with the Skill.

`online-media` uses the same adapter pattern. The upstream project remains pinned as a
submodule, includes a standalone MIT license, and keeps its focused Markdown workflows
internal. Only the central `online-media` adapter is projected into Agent discovery.

`presentation` remains a pinned standalone project with a standalone MIT license. Its root
router and supporting presentation workflows stay inside the submodule; only the central
`presentation` adapter is projected into Agent discovery.

`innovation-assistant` remains a pinned, pure-Markdown standalone project with a standalone
MIT license. Its root router, focused SIT and Think Bigger pipelines, axioms, and experiment
evidence stay in the submodule; only the central `innovation-assistant` adapter is projected
into Agent discovery.

`image-generation` remains a pinned standalone Python project with one root router and an
offline test suite. The inspected commit contains no license file and declares no package
license, so the registry records `NOASSERTION` instead of inferring reuse terms. Only the
central `image-generation` adapter is projected into Agent discovery; provider credentials
and generated images remain in ignored local storage.

`writing-workflows` remains a pinned standalone project with an MIT license, one Chinese
canonical root router, synchronized focused English mirrors, and a Chinese-primary lint CLI.
The central English adapter performs language-aware routing and is the only root projected
into Agent discovery; focused workflows, private voice material, drafts, and publishing
configuration are not separately exposed.

`baoyu-article-illustrator` is an adapter to JimLiu/baoyu-skills at
`8ae8c33a8d7c8c7c6de291b2c91ba1debe1d2766`. The upstream root LICENSE declares
MIT, copyright 2026 Jim Liu. Its full repository remains pinned as a submodule; only the
Article Illustrator entrypoint is exposed. Supporting styles and preferences remain upstream.
The adapter adds scientific fidelity checks and respects actual host tool contracts.

`image-dream` is an original workflow authored in this repository. It optionally routes to
existing image-generation capabilities and Baoyu references without vendoring their content.
Its art-direction recipes and run-state helper are original. No redistribution license is
assigned yet (`NOASSERTION`); human functional and privacy review remains pending.

`intake-skill` routes to `grapeot/intake-skill` at
`830956d107cc0e9fc4849809827d8841b8426837`, under the upstream MIT LICENSE
(copyright 2026 intake_skill contributors). The upstream implementation is unchanged
and pinned as a submodule. Only the central adapter is exposed. The adapter requires
private runtime storage and explicit authorization for optional nightly automation.

`explain-ste100` is an original concept-explanation and technical-writing workflow.
Its selected STE guidance is paraphrased from official ASD sources linked in the Skill.
The ASD-owned standard and dictionary are not bundled. No redistribution license has
been assigned to the original Skill; functional and privacy review is pending.

`visual-explainer` adapts `nicobailon/visual-explainer` at `5846f5aef34a23c8fea389d2f23ce56224cbf840`.
The upstream MIT license is copyright 2025 Nico Bailon. The pinned implementation,
references, templates, and optional tools stay intact in the submodule; only the adapter
is projected globally. Functional and privacy review remains required before merge.

`graphify` is a package adapter to `Graphify-Labs/graphify`, using the official
PyPI distribution `graphifyy==0.9.77`. The runtime declares Apache-2.0 and includes
Apache LICENSE, MIT attribution, and NOTICE files. The adapter reads the installed
package's host workflow and progressive references, rather than copying them.
Local installation was requested on 2026-10-05; publication and merge review is pending.

`compute-scg` is an owner-requested SCG variant derived from the owner-authored
`remote-compute-ssh` helper and supplied Claude Science compute notes. Exact
bundled code hashes are retained in its provenance sidecar. No upstream repository
URL or redistribution license has been established; recorded as `NOASSERTION`.
Personal paths and actual lab accounts are retained only in an ignored overlay.
