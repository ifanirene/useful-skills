---
name: explain-ste100
description: Explain concepts or draft and revise English technical text using ASD-STE100 Simplified Technical English principles. Use when the user requests STE, ASD-STE100, or a concept explanation in controlled technical English; not for every general writing task.
license: NOASSERTION
---

# Explain with Simplified Technical English

Explain a concept so that the reader can understand how it works and why it matters.
Use ASD-STE100 to control the language. Keep the technical meaning, evidence, and limits.
This skill supports concept explanations, new technical text, and revisions of existing text.
It does not change code, identifiers, formulas, or direct quotations to make them look like STE.

## Choose the task and the level

Use the user's topic, source text, audience, and purpose. If the audience is unknown,
assume an adult who is new to the subject. State this assumption only when it affects the result.
Ask a focused question if the topic has materially different meanings or a missing input prevents useful work.
Do not require a questionnaire before a clear request.

- For an explanation, establish the meaning, the main process, and its practical consequence.
- For a draft, use the requested format and purpose.
- For a revision, preserve the source's claims, order, and useful structure. Change the language as needed.
- For a compliance review, identify the applicable issue and the available rules and dictionary before judging compliance.

Apply this skill to the requested text or explanation. Do not make it a permanent rule for unrelated conversations.
STE is English. If the user also requests a translation, apply STE to the English text;
do not call the translation ASD-STE100 compliant.

## Explain the concept

Start with a direct definition or answer. Introduce the necessary parts before describing their interactions.
Build the explanation from what the reader already knows. Explain each new technical term when it first appears.
Use the same term throughout. Expand unfamiliar abbreviations on first use.

Show the relevant chain: what changes, how the change occurs, and what result follows.
Give a small, concrete example when it helps the reader apply the concept.
Use an analogy only if it clarifies a difficult relation. State where the analogy stops being accurate.
Do not present an analogy as a mechanism or as evidence.

Answer the user's actual question. Add the key limit or common misunderstanding if it affects the answer.
Do not simplify by removing conditions, exceptions, units, uncertainty, or the distinction between association and cause.
For a scientific claim, keep observation, proposed mechanism, and inference distinct.
Research unfamiliar or changeable facts with the available tools; retain citations that support the claims.
This skill controls expression. It does not supply factual evidence.

## Control the language

These are working checks, not the complete standard:

- Classify passages as descriptions or instructions. Use at most 25 words per descriptive sentence and 20 per procedural sentence.
- Give each descriptive paragraph one topic and at most six sentences.
- Use commands for instructions. Normally give one instruction per sentence; simultaneous actions can require a combined instruction.
- Put a necessary condition before its instruction. Place an applicable warning before the affected step.
- Use active constructions. In descriptions, use passive constructions only when an active construction is unsuitable.
- Prefer simple verb forms. Replace ambiguous verb forms ending in “-ing”; do not reject permitted words or technical terms by suffix alone.
- Break up long noun groups. Use articles and connecting words to show the relation between terms.
- Remove idioms, figurative expressions, and unnecessary words. Use American spelling for ordinary English words.

Use the official dictionary to establish a general word's approved meaning, part of speech, and permitted forms.
A common or short word is not automatically an approved STE word. Do not invent word-approval claims.
Avoid synonyms used only for variety. Name each thing consistently, and use each term with a stable meaning.

Retain necessary technical nouns and technical verbs under the standard's applicable categories.
A project glossary can record these terms, their meanings, and their permitted use.
It does not make any chosen word a valid exception. Do not label ordinary difficult prose as technical terminology to bypass the dictionary.
In science, keep exact gene names, assay names, statistical terms, and measurement units when they carry necessary meaning.
Explain them instead of replacing them with inaccurate everyday words.

## Check and report the result

Review meaning first, then language:

1. Compare the result with the question or source. Preserve quantities, conditions, relationships, and the strength of each claim.
2. Read it as the intended audience. Resolve undefined terms, unclear pronouns, missing logical steps, and unexplained examples.
3. Check sentence lengths, paragraph lengths, instruction order, and consistent terminology.
4. If the official reference is available, check vocabulary and the remaining applicable rules against it.

Use the standard's word-count rules when making a compliance judgment. A simple whitespace count is only a screening aid.
Rephrase a difficult sentence rather than making mechanical word substitutions that change its meaning.

Return the requested explanation or text first. Match the user's requested length and format.
Use connected prose for explanations and numbered steps for procedures when useful.
Do not force a definition/example/glossary template onto every answer.
Show a change table, glossary, or audit only if requested or needed to resolve a material issue.

Without a complete rules and vocabulary review, call the result an **STE-style draft**, not verified compliant text.
Give one short qualification, such as: “STE-style draft. Full dictionary compliance has not been checked.”
For a compliance review, report the issue used, checks performed, unresolved terms, and any rules not checked.
Do not imply ASD certification or treat a checker result as proof of full compliance.
If the reference is missing, still produce a useful draft and identify the verification gap.

## Official references and provenance

Issue 9 was published on January 15, 2025. Use the issue specified by the user or project.
Confirm the applicable issue from the official source when a compliance review requires it.

- [About ASD-STE100](https://asd-ste100.org/about_STE.html): scope and terminology.
- [Official downloads](https://www.asd-ste100.org/STE_downloads.html): obtain the standard and its dictionary.
- [Issue 9 reference](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf): writing and vocabulary rules.
- [Official FAQ](https://asd-ste100.org/STE_faq.html): vocabulary, technical terms, and usage questions.

This is an original explanation workflow with a brief paraphrase of selected STE guidance.
It does not reproduce the full rules or dictionary. ASD owns the standard.
Keep a supplied standard, private glossary, and private examples in the consuming project or ignored local overlay.
Do not copy them into this public skill package.

## Example requests

- “Use $explain-ste100 to explain false discovery rate to a biologist who is new to statistics.”
- “Use $explain-ste100 to rewrite this technical paragraph. Keep its claims and citations.”
- “Use $explain-ste100 to draft these instructions, then list terms that need dictionary review.”
