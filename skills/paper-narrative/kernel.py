"""paper-narrative helpers.

`check_narrative_brief` is pure Python and runs anywhere; both modes (polish and
rewrite) use it. `derive_figure_brief` and `narrative_review_task` serve the optional
figure review; `derive_figure_brief` calls `host.llm` and needs a host that provides
that SDK. Elsewhere, use the prompt text and schemas with a sub-agent instead.
"""
STRENGTHS = ("unresolved", "consistent_with", "suggests", "shows")
ARC_ROLES = ("hook", "mechanism", "evidence", "boundary", "application", "supplement")


def pn_sdk():
    """Rebind-proof handle to the host SDK; import lazily so pure helpers work without it."""
    import host
    return host


# ---------------------------------------------------------------- narrative brief

def narrative_brief_schema():
    """Shared spine for both modes and the figure review (see SKILL.md, step 1)."""
    step = {"type": "object", "properties": {
        "key": {"type": "string"},
        "question": {"type": "string"},
        "answer": {"type": "string"},
        "evidence": {"type": "string"},
        "strength": {"type": "string", "enum": list(STRENGTHS)},
        "load_bearing": {"type": "boolean"},
        "requires": {"type": "array", "items": {"type": "string"}},
        "grounds": {"type": "array", "items": {"type": "string"}},
        "raises": {"type": "string"}},
        "required": ["key", "question", "answer", "evidence", "strength"]}
    return {"type": "object", "properties": {
        "reader": {"type": "string"},
        "prerequisites": {"type": "array", "items": {"type": "string"}},
        "question": {"type": "string"},
        "gap": {"type": "string"},
        "message": {"type": "string"},
        "message_strength": {"type": "string", "enum": list(STRENGTHS)},
        "steps": {"type": "array", "items": step},
        "limits": {"type": "array", "items": {"type": "string"}},
        "next": {"type": "string"}},
        "required": ["reader", "question", "message", "message_strength", "steps"]}


def _norm(concept):
    return " ".join(str(concept).lower().split())


def check_narrative_brief(brief):
    """Mechanical checks on a narrative brief. Returns {"ok": bool, <issue lists>}.

    Catches what can be checked without judgment: missing fields, unlinked steps,
    concepts used before they are grounded, steps without evidence, and a message
    stated more strongly than a load-bearing step supports. Whether a step's question
    really follows from the previous `raises`, and whether a strength label fits the
    evidence, remain the agent's and the reviewer's judgment.
    """
    issues = {"missing_fields": [], "unlinked_steps": [], "ungrounded": [],
              "no_evidence": [], "overclaims": []}
    for field in ("reader", "question", "message", "message_strength"):
        if not str(brief.get(field) or "").strip():
            issues["missing_fields"].append(field)
    steps = brief.get("steps") or []
    if not steps:
        issues["missing_fields"].append("steps")

    rank = {s: i for i, s in enumerate(STRENGTHS)}
    msg_strength = brief.get("message_strength")
    grounded = {_norm(c) for c in brief.get("prerequisites") or []}

    for i, step in enumerate(steps):
        key = step.get("key") or f"step{i + 1}"
        for field in ("question", "answer"):
            if not str(step.get(field) or "").strip():
                issues["missing_fields"].append(f"{key}.{field}")
        if i < len(steps) - 1 and not str(step.get("raises") or "").strip():
            issues["unlinked_steps"].append(
                {"step": key, "problem": "no `raises`; the reader is not told why the next step follows"})
        if not str(step.get("evidence") or "").strip():
            issues["no_evidence"].append(key)

        # A step may ground a concept and use it in the same step.
        available = grounded | {_norm(c) for c in step.get("grounds") or []}
        for concept in step.get("requires") or []:
            if _norm(concept) not in available:
                issues["ungrounded"].append(
                    {"concept": concept, "first_used_in": key,
                     "fix": "ground it in an earlier step, declare it a prerequisite, or cut it"})
        grounded = available

        strength = step.get("strength")
        if strength not in rank:
            issues["missing_fields"].append(f"{key}.strength")
        elif (step.get("load_bearing", True) and msg_strength in rank
              and rank[msg_strength] > rank[strength]):
            issues["overclaims"].append(
                {"step": key, "problem": f"message is `{msg_strength}` but this load-bearing step is `{strength}`"})

    issues["ok"] = not any(issues[k] for k in issues)
    return issues


# ---------------------------------------------------------------- figure review

def figure_brief_schema():
    """Figure-review brief: the narrative brief plus editor-facing fields; steps are figures."""
    schema = narrative_brief_schema()
    schema["properties"].update({
        "vision": {"type": "string"},
        "most_arresting_asset": {"type": "string"}})
    return schema


def derive_figure_brief(summary_text, figure_claims, reader="broad scientist in the field", model=None):
    """summary_text: the document's abstract or opening.
    figure_claims: list[{"key", "claim"|"caption", "composite_vid"?}].
    Returns a figure brief (figure_brief_schema) with one step per figure. Needs `host.llm`.

    The document text is untrusted input and every returned string is LLM-derived
    from it. Review the whole brief, then run `check_narrative_brief`, before dispatching
    `narrative_review_task`. Raises RuntimeError if the host returns no structured output."""
    fc = "\n".join(f"  {f.get('key', '?')}: {f.get('claim') or f.get('caption', '')}"
                   for f in figure_claims)
    prompt = (
        "You are the corresponding author. From the summary and per-figure captions below, "
        "write the narrative brief a reader would judge the figures against.\n\n"
        f"Reader: {reader}. List the concepts this reader already brings as prerequisites.\n"
        "Question = the central question, in the reader's terms. Gap (for a manuscript or "
        "proposal) = complete 'It remains unclear whether, why, or under what conditions ___' "
        "(not 'nobody has used our method'). "
        "Message = the most specific one-sentence answer the evidence supports; do not inflate it. "
        "Message_strength and each step's strength: shows (direct test with a control or "
        "perturbation), suggests, consistent_with, or unresolved.\n"
        "Steps = one per figure, in order: the question the reader holds when the figure starts, "
        "its answer, evidence (figure key), strength, requires (concepts it leans on), grounds "
        "(concepts it introduces), raises (the question it leaves for the next figure).\n"
        "Vision = what a reader can now do. Most_arresting_asset = the single panel you would "
        "put on a poster.\n\n"
        f"## Summary\n{summary_text}\n\n## Figures\n{fc}\n")
    r = pn_sdk().llm(prompt, tools=[{"name": "figure_brief", "input_schema": figure_brief_schema()}],
                     tool_choice={"type": "tool", "name": "figure_brief"},
                     model=model or pn_sdk().reasoning_model(), max_tokens=3000)
    calls = r.get("tool_use") or []
    if not calls or not calls[0].get("input"):
        raise RuntimeError("derive_figure_brief: host returned no structured brief; build it by hand")
    brief = calls[0]["input"]
    brief.setdefault("reader", reader)
    return brief


def narrative_review_schema():
    framing = {"type": "object", "properties": {
        "question": {"type": "string"}, "message": {"type": "string"},
        "fig1_claim": {"type": "string"}, "what_it_costs": {"type": "string"}},
        "required": ["question", "message", "fig1_claim"]}
    return {"type": "object", "properties": {
        "hook_verdict": {"type": "object", "properties": {
            "would_send_for_review": {"type": "string", "enum": ["yes", "weak", "no"]},
            "why": {"type": "string"}, "fig1_is": {"type": "string"}},
            "required": ["would_send_for_review", "why"]},
        "reader_summary": {"type": "string"},
        "lost_at": {"type": "array", "items": {"type": "object", "properties": {
            "where": {"type": "string"}, "why": {"type": "string"}, "fix": {"type": "string"}},
            "required": ["where", "why", "fix"]}},
        "question_chain_breaks": {"type": "array", "items": {"type": "object", "properties": {
            "between": {"type": "string"}, "problem": {"type": "string"}, "fix": {"type": "string"}},
            "required": ["between", "problem", "fix"]}},
        "ungrounded_concepts": {"type": "array", "items": {"type": "object", "properties": {
            "concept": {"type": "string"}, "first_used_in": {"type": "string"},
            "fix": {"type": "string", "enum": ["ground_earlier", "make_prerequisite", "cut"]}},
            "required": ["concept", "first_used_in", "fix"]}},
        "overclaims": {"type": "array", "items": {"type": "object", "properties": {
            "where": {"type": "string"}, "claim": {"type": "string"},
            "evidence_supports": {"type": "string"}, "calibrated_claim": {"type": "string"}},
            "required": ["where", "claim", "calibrated_claim"]}},
        "figure_moves": {"type": "array", "items": {"type": "object", "properties": {
            "what": {"type": "string"}, "from_fig": {"type": "string"},
            "to_fig": {"type": "string"}, "why": {"type": "string"}},
            "required": ["what", "from_fig", "to_fig", "why"]}},
        "missing_panels": {"type": "array", "items": {"type": "object", "properties": {
            "target_fig": {"type": "string"}, "what_to_show": {"type": "string"},
            "analysis_needed": {"type": "string"}, "data_hint": {"type": "string"}},
            "required": ["target_fig", "what_to_show", "analysis_needed"]}},
        "kill_list": {"type": "array", "items": {"type": "object", "properties": {
            "what": {"type": "string"}, "why": {"type": "string"},
            "demote_to": {"type": "string", "enum": ["supplement", "caption", "delete"]}},
            "required": ["what", "why", "demote_to"]}},
        "arc": {"type": "array", "items": {"type": "object", "properties": {
            "fig": {"type": "string"}, "role": {"type": "string", "enum": list(ARC_ROLES)},
            "answers": {"type": "string"}, "raises": {"type": "string"}},
            "required": ["fig", "role", "answers"]}},
        "candidate_framings": {"type": "array", "items": framing, "minItems": 2, "maxItems": 3}},
        "required": ["question_chain_breaks", "ungrounded_concepts", "overclaims", "arc"]}


_LENSES = {
    "editor": (
        "You are the HANDLING EDITOR. Decide whether Fig 1 and the arc would make you send this "
        "paper for review. Judge story and significance, not figure craft. Fill hook_verdict, "
        "figure_moves, missing_panels (the concrete analysis to run), kill_list, arc, and 2-3 "
        "candidate_framings, each a different question/message pair with the Fig 1 claim it implies "
        "and what it costs. Never kill counterevidence or a limit that changes how the message "
        "reads; demote robustness checks instead."),
    "reader": (
        "You are a BROAD SCIENTIST in the field who does not know this project's datasets, metrics, "
        "labels, or local terms. Read the figures in order. Fill reader_summary (in one sentence: "
        "what question does this answer and what is the answer?), lost_at (where you first could "
        "not follow, and why), question_chain_breaks (where a figure does not answer the question "
        "the previous one left), ungrounded_concepts (a concept used before it was explained), "
        "overclaims (a verb stronger than the evidence: association stated as mechanism, a trend "
        "stated as significant, one dataset stated as general), and arc."),
}


def narrative_review_task(brief, deck_vid, rules_vid=None, lens="editor"):
    """Prompt for one independent reviewer. Run lens='editor' and lens='reader' in parallel;
    neither reviewer sees the other's output. `rules_vid` is an optional design-rules artifact
    shown for reference only."""
    if lens not in _LENSES:
        raise ValueError(f"lens must be one of {sorted(_LENSES)}")
    steps = "\n".join(
        f"  {s.get('key', '?')}: Q: {s.get('question', '—')} -> A: {s.get('answer') or s.get('claim', '—')} "
        f"[{s.get('strength', '?')}]"
        for s in brief.get("steps") or brief.get("figures") or [])
    rules = (f"\n## Design rules (reference only; do NOT grade craft)\n`{{{{artifact:{rules_vid}}}}}`\n"
             if rules_vid else "")
    prereq = ", ".join(brief.get("prerequisites") or []) or "—"
    return f"""{_LENSES[lens]}

## Narrative brief (the author's intent; test it, do not trust it)
**Reader:** {brief.get('reader', 'broad scientist in the field')}  |  **Prerequisites:** {prereq}
**Question:** {brief.get('question', '—')}
**Gap:** {brief.get('gap', '—')}
**Message ({brief.get('message_strength', '?')}):** {brief.get('message', '—')}

## All figures (one PDF)
`{{{{artifact:{deck_vid}}}}}`

## Per-figure steps
{steps}
{rules}
Be specific and opinionated; the author wants a partner, not a grader. Return ONLY structured output."""
