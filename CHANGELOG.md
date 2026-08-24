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
- Pinned `grapeot/online-media-skill` as a standalone project and exposed exactly one
  `online-media` adapter with an isolated discovery profile.
- Pinned `grapeot/presentation_skill` as a standalone project and exposed exactly one
  `presentation` adapter with an isolated discovery profile.
- Added an ignored `.local/<skill>/` overlay contract for private aliases, paths,
  credentials, and runtime artifacts.

### Review required

- Confirm the precise upstream URLs for the four Anthropic-imported skills. Their provider
  and licenses are recorded, but the earlier import did not preserve canonical source URLs.
- Review the upstream `ai_session_export` license packaging: its README declares MIT, but the
  pinned commit does not include a standalone license file.
- Confirm the `online-media` adapter routes the intended workflows and that no private local
  media configuration is present before promotion.
- Confirm the `presentation` adapter routes image and Reveal workflows correctly and that no
  private presentation configuration or generated deck content is present before promotion.
- Obtain explicit functional and privacy approval before merging this branch.
