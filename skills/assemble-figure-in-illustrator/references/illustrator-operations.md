# Illustrator operations and failure recovery

## Choose a control route

Use the available native scripting bridge or Illustrator's script-opening UI after
reading the host tool documentation. Generate task-specific JSX in the consuming
project. Probe a small operation on a copy before editing a complex document.
For computer interaction, inspect the current app state, activate the intended
document, observe selection and dialogs, and verify each consequential operation.
Do not use unverified screen coordinates or assume a menu action succeeded.

## Stable document and object mapping

Capture an explicit document reference; imports can change the active document.
Check the document identity and unsaved state. Inventory artboard rectangles,
layer/group names, bounds, locked/hidden state and text before mutation. Record
which objects belong to each target panel. Use names plus structural evidence;
duplicated names or spatial overlap alone are insufficient identification.

For JSX, use syntax supported by the installed ExtendScript runtime. Cache collection
lengths and snapshot direct-child references before adding, deleting or regrouping.
Container collections may expose descendants differently; define a single traversal
that counts each item once rather than summing overlapping collection lengths.
Distinguish a layer, a group and a clipping path. Inspect clipping recursively.

Keep stacking order and local transforms when regrouping. Unlock only intended
objects and restore their state where appropriate. A single panel group is often
enough; add data/axes/annotation subgroups only when they improve editing.

## Import, transform and replace

Open/import the local export into a temporary document or place it according to
whether editable native objects are required. A placed PDF alone does not prove its
labels are editable. Probe duplication and inspect the returned object before using
it; cross-document duplication must not be assumed to return a transformable group.
If needed, use copy/paste into a named destination layer, inspect the selected items,
and group only that import. Verify both documents and retain source artwork.

Derive translations from the actual artboard coordinate system and measured bounds.
Illustrator geometry commonly uses points; use 72 points per inch for unit conversion.
Do not assume the artboard origin or axis direction. Clipped visible extent may differ
from geometric or stroke bounds: inspect the actual crop before alignment or sizing.
Preserve aspect ratio unless the requested plot redraw requires a different shape.
After resizing, measure text and line widths rather than assuming scaling preferences.

Replace the identified panel objects, including verified obsolete covered content;
then check adjacent and unaffected regions. Never replace every occurrence of a
single panel letter globally. Keep an explicit panel-label mapping.

## Bounded recovery and saved-file proof

Wait for the current script to finish before another mutation or export. Use a clear
completion/error receipt written only after the save/export finishes. A newly created
AI file can exist before the editing script has completed. On failure, inspect the
partial document and completed operations before retrying; do not blindly rerun a
script that might duplicate panels or repeat translations.

Use explicit destination filenames and a fresh preview. Restore any application
preferences a task-specific script changes. Keep external-script security settings
unchanged. Do not execute an upstream script unreviewed merely because it is popular.

Reopen the saved output when safe, or otherwise establish that the export represents
the completed save. Compare panel dimensions and recursive counts, inspect a few text
and panel selections, and view the entire figure. Object counts are diagnostic; no
universal count threshold establishes usability. If scripting succeeds but visual
inspection is unavailable, report that limitation instead of declaring the AI verified.
