# Sources and reuse boundary

This skill is independently authored workflow guidance. No external script or private
figure is bundled. No redistribution license has been assigned (NOASSERTION).

- [figure-style](../../figure-style/SKILL.md) is the existing local dependency for
  scientific plotting and styling. Its source and license remain unchanged.
- [creold/illustrator-scripts](https://github.com/creold/illustrator-scripts) is a
  practical JSX reference, not an Agent Skill dependency. Its repository declares
  [MIT](https://github.com/creold/illustrator-scripts/blob/master/LICENSE).
  [ResizeToSize.jsx](https://github.com/creold/illustrator-scripts/blob/master/jsx/ResizeToSize.jsx)
  was inspected as a candidate for sizing and clipped-object handling. No code was
  copied or executed. Before adopting a utility, pin the selected revision, inspect
  its complete behavior and attribution, and retain license notices for copied code.
  Do not inherit changes to application security preferences from a utility.
- [Matplotlib rasterization](https://matplotlib.org/stable/gallery/misc/rasterization_demo.html)
  documents per-artist rasterization within vector output. Verify behavior with the
  installed plotting backend and Illustrator import, not only the browser preview.
- The community-maintained [Illustrator scripting guide](https://ai-scripting.docsforadobe.dev/)
  provides API lookup for GroupItem, Document and positioning. Verify methods against
  the installed Illustrator version; this is not evidence that a generated script
  has run successfully.

Reviewed 2026-11-07. These links are references, not an automatic install list.
Native-editing lessons informed the workflow, but this new skill has not yet received
an independent end-to-end Illustrator evaluation.
