# Maintain the wiki

Read when adding or revising a source, or when closing out work that changed what the project
knows.

## Ingest or revise a source

1. **Place it.** Read the owning branch index and the current answer. Decide whether the
   material updates an existing question or warrants a child page. Keep the file in the
   repository with its original filename, or identify its library item for a formal
   publication. Run the audit to see what is new, changed or missing.
2. **Read all of it.** For a PDF, keep page-marked text and inspect the figures and tables that
   interpretation depends on. For HTML, include embedded data. For an image, look at the image.
   State unreadable portions. Files with identical hashes share one note that lists every path.
3. **Write or revise the source note** from `templates/source-note.md`. Give the source's own
   claims, the evidence type, exact locators, useful findings, limitations and what it changes
   for the project. Classify a source by the use it serves now, not by its file type or origin.
   A correction to an earlier reading is made explicitly; a later disagreement is linked, never
   overwritten.
4. **Integrate.** Revise every affected current answer in place, saying what the source
   strengthens, changes, challenges or leaves unchanged. Follow the implications across
   branches by meaning, not by folder. Reconcile superseded statements wherever they remain.
   Record disagreements in `questions.md` and investigator choices in `decisions.md`.
5. **Register** the manifest entry after integration: path, sha256, bytes, source ID, note,
   status `ingested` and coverage. The audit never accepts new files automatically.
6. **Close.** Update the immediate index if a page was added, moved or changed scope. Append one
   log entry naming the intake, the pages changed and what remains unresolved. Run the audit and
   review the scientific meaning yourself.

## Close out project work

- **Analysis:** when a result changes an answer, cite the owning analysis note and report or
  figure with its run or variant. State the estimand and its limits. Leave numbers and
  provenance in the analysis record.
- **Literature research:** cite papers you actually read, with the version and the reading
  depth. Add formal publications to the bibliography workflow, or to the reconciliation list
  when unresolved. Revise the answer, not just its reference list.
- **Writing:** when a draft changes the project's claims, scope or framing, record the accepted
  change in the answer and in decisions. A draft is not an accepted decision until the
  investigator says so.
- **Conversation:** record an investigator decision with a verbatim quote, the date and the
  place it was made. Keep agent recommendations listed separately as recommendations.

Keep updates at the level of scientific questions, not tickets or sessions. If no wiki update
was needed, say why in the closing report.

## Structure and health

- Before creating a page, ask what question it answers and where that question already lives.
  Choose the smallest existing branch that covers it. A new source, person or date is not a
  reason for a new branch. Change the main branches only for a real change in scope, and
  record the reason.
- For a page move, update inbound and outbound links, manifest note paths and the branch
  indexes, then confirm that every original hash still matches.
- Occasionally, with the investigator's guidance, consolidate pages that grew source by source
  into coherent current answers. Keep each source's own account and any unresolved
  disagreement.
- Images (optional): keep originals in place and register retained images in the image
  manifest. Default to `supporting`; reserve `reference` for gallery selections that carry a
  selection reason. Regenerate the gallery with `wiki_images.py render` and inspect it, because
  an automated check cannot judge visual quality.
