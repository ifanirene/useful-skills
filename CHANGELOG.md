# Changelog

All notable registry changes are recorded here.

## Unreleased

### Changed

- Reorganized the four existing skills under the canonical `skills/` root.
- Converted the repository into a central personal Skill library with a root Agent router,
  machine-readable registry, profiles, project integration template, and local link tool.
- Made the shared/private boundary and human promotion gate explicit.

### Added

- Registry and public-content validation scripts with CI coverage.
- Architecture, project integration, contribution, provenance, and review documentation.
- Pinned `grapeot/ai_session_export` as a standalone project and added one discoverable
  `ai-session-export` adapter with an isolated discovery profile.
- Adapted `grapeot/context-infrastructure`'s instruction-only AI session search workflow into
  one discoverable `ai-session-search-archive` Skill with an isolated discovery profile.
- Adapted `grapeot/context-infrastructure`'s paper-analysis workflow into the discoverable
  `research-paper-analysis-writing` Skill, replacing stale host-specific references with the
  local `literature-review` route and private-overlay contract.
- Adapted `grapeot/context-infrastructure`'s AI programming and Skill-writing best practices
  into the focused `ai-programming-mindset` and `skill-writing-principles` Skills with isolated
  discovery profiles and provider-neutral private overlays.
- Adapted HumanLayer's instruction-only `show-me` Skill into a host-neutral visual-explanation
  workflow with its upstream MIT license and an isolated discovery profile.
- Pinned `grapeot/online-media-skill` as a standalone project and exposed exactly one
  `online-media` adapter with an isolated discovery profile.
- Pinned `grapeot/presentation_skill` as a standalone project and exposed exactly one
  `presentation` adapter with an isolated discovery profile.
- Pinned `grapeot/innovation-assistant-skill` as a standalone project and exposed exactly one
  `innovation-assistant` adapter with an isolated discovery profile.
- Pinned `grapeot/image-generation-skill` as a standalone project and exposed exactly one
  `image-generation` adapter with an isolated discovery profile and private credential
  overlay.
- Pinned `grapeot/writing-skill` as a standalone project and exposed exactly one
  language-aware `writing-workflows` adapter with an isolated discovery profile and offline
  Chinese prose lint CLI.
- Added an ignored `.local/<skill>/` overlay contract for private aliases, paths,
  credentials, and runtime artifacts.

### Review required

- Confirm the precise upstream URLs for the four Anthropic-imported skills. Their provider
  and licenses are recorded, but the earlier import did not preserve canonical source URLs.
- Review the upstream `ai_session_export` license packaging: its README declares MIT, but the
  pinned commit does not include a standalone license file.
- Review the `ai-session-search-archive` adaptation and upstream license packaging: the
  source README declares MIT, but the repository has no standalone license file.
- Review the `research-paper-analysis-writing` adaptation and upstream license packaging: the
  source README declares MIT, but the repository has no standalone license file.
- Review the `ai-programming-mindset` and `skill-writing-principles` adaptations and the same
  upstream license-packaging limitation before promotion.
- Confirm the `show-me` adaptation selects the smallest useful visual, preserves factual
  structure, and does not create unnecessary HTML artifacts before promotion.
- Confirm the `online-media` adapter routes the intended workflows and that no private local
  media configuration is present before promotion.
- Confirm the `presentation` adapter routes image and Reveal workflows correctly and that no
  private presentation configuration or generated deck content is present before promotion.
- Confirm the `innovation-assistant` adapter routes SIT and Think Bigger correctly, preserves
  its human judgment checkpoints, and exposes no private innovation context before promotion.
- Resolve or explicitly accept the missing upstream license declaration for
  `image-generation`, and confirm that its provider credentials and generated artifacts stay
  outside public registry content.
- Confirm the `writing-workflows` adapter selects the correct audience and language workflow,
  treats the Chinese lint CLI appropriately for English output, and keeps private drafts,
  voice examples, and publishing configuration outside public content.
- Obtain explicit functional and privacy approval before merging this branch.
