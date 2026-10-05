# ChatGPT Library as a reference source

Use the user's signed-in ChatGPT Library when requested. Being signed in to Codex does not
establish access to every ChatGPT asset. Discover a supported connector first; otherwise use
the host's browser/computer tools to inspect the actual signed-in Library interface. Follow
current visible navigation rather than assuming that the image gallery lives at a fixed URL.

## Select and inspect

Filter to images, then use the library's search or visible candidates relevant to the requested
subject. Inspect a few selected images at usable size. Titles alone do not establish style or
scientific correctness. Do not assume the newest image is a favorite; it might be a rejected
attempt. If the user has favorites or exclusions, preserve them in the private series config.

Record the selected title, a stable Library or conversation link when the UI supplies one,
and its intended reference role. Keep private links and source text out of the public skill.
Do not inventory unrelated account content, share images publicly, alter library items, or
submit new ChatGPT prompts merely to read the library.

## Make references usable

The preferred scheduled workflow uses a small private local cache of selected references,
obtained via the normal download UI or a supported browser asset export capability. Inspect
saved files and retain their source links and retrieval date. Do not extract session cookies,
credentials, hidden APIs, or access tokens, or persist temporary signed asset URLs as durable
references. Cache only the selected material needed for the user's requested series.

Use local image files as generator references when the backend supports them. A browser
screenshot or inspected style description can guide planning, but is not an original downloaded
reference. If only a textual style description can be used, state that limitation rather than
claiming direct image conditioning. Do not claim to have passed a reference to the generator
unless the actual call includes it.

## Scheduling modes

- **Cached references:** runs can use the verified local files without visiting ChatGPT each
  time. Record that the cache is a snapshot and refresh only within the configured scope.
- **Live library:** each run browses the signed-in library, checks accessibility, selects and
  inspects references. Requires browser access and a valid session on the scheduled host.
  A login page, unavailable browser, or missing reference is a blocker, not an empty library.

If cache export is unavailable and unattended browser access is unverified, build and install
the reusable skill but leave live scheduling inactive. Explain what works now (for example,
interactive browsing) and what still needs verification. Offer user-provided downloaded
references only after the available access/export paths have been tried.
