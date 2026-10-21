# Bootstrap a wiki

Read when a repository has no wiki yet. The result is a small wiki that answers the project's
durable questions from a confirmed set of sources. Breadth can come later.

1. **Learn the project.** Read the README, the repository `AGENTS.md`, and any analysis index
   and notes. Identify three to six durable questions the project keeps returning to. These
   become topic pages, grouped under at most four stable branches. If another system already
   owns analysis records, note which pages it owns so the wiki can link to them.
2. **Agree on the initial sources and questions.** Use the investigator's selection where one
   was given. Otherwise propose candidates, giving each one the question or decision it informs.
   Ask the investigator once to confirm the sources and the durable questions. Read nothing
   beyond the authorized set. A file that git does not track is invisible to automation reading
   the pushed repository, so ask whether such files should be tracked or left out.
3. **Scaffold.** Copy the templates: `living-wiki.toml` to the repository root, and the rest
   into the wiki folder (`AGENTS.md`, `index.md`, `decisions.md`, `questions.md`, `log.md`,
   `NOTES.md`, and `sources/` for notes). Register raw files where they already are. Set
   `raw_roots` only for curated folders whose every file must be registered, never for results
   or data trees.
4. **Read and note each source.** Read the whole relevant content. For a PDF, keep page
   locators and inspect the figures and tables the interpretation needs. For DOCX or HTML,
   include embedded comments, tables and images. Subagents may read sources in parallel; give
   each one the source note template and the questions. Record what was not read.
5. **Write the current answers.** One page per durable question, from the topic template:
   question, current answer, key evidence, strongest alternative, what would change the answer,
   and limits. Link analysis notes for numbers rather than copying them.
6. **Seed decisions and questions** from records that already exist: meeting notes, reviewer
   responses, attributed notes. Quote and attribute. Never turn an agent suggestion into a
   decision.
7. **Register and check.** Use `wiki_audit.py --stub` for hashes, complete each manifest entry
   with its source ID, note and coverage, then run the audit until it shows no errors. Baseline
   only errors that cannot be fixed now, and list them in `NOTES.md`.
8. **Route and connect.** Add a short wiki section to the repository `AGENTS.md`, following
   that file's own editing rules. With the investigator's authorization, register `decisions.md`
   as a decision source in any attributed decision memory, and add the wiki to the Ouroboros
   journal configuration.
9. **Log and report.** Write the first log entry. Report the sources read and their coverage
   gaps, the pages created, and the open questions.

Done when every selected source is registered with its coverage, each durable question has a
page with a current answer, every page is reachable from the index, the audit shows no new
errors, and the log records the bootstrap.
