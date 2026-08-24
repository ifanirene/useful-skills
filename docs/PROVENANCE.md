# Provenance

`manifest.json` is the canonical source record. This page explains unresolved history that
cannot be reconstructed safely from the current files alone.

| Skill | Recorded provider | License | Upstream source |
| --- | --- | --- | --- |
| `figure-style` | Anthropic | Apache-2.0 | Owner confirmation required |
| `figure-composer` | Anthropic | Apache-2.0 | Owner confirmation required |
| `paper-narrative` | Anthropic | Apache-2.0 | Owner confirmation required |
| `literature-review` | Anthropic | Apache-2.0 | Owner confirmation required |
| `ai-session-export` | grapeot | MIT (README declaration) | `https://github.com/grapeot/ai_session_export` at `e52754d` |
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

`online-media` uses the same adapter pattern. The upstream project remains pinned as a
submodule, includes a standalone MIT license, and keeps its focused Markdown workflows
internal. Only the central `online-media` adapter is projected into Agent discovery.

`presentation` remains a pinned standalone project with a standalone MIT license. Its root
router and supporting presentation workflows stay inside the submodule; only the central
`presentation` adapter is projected into Agent discovery.
