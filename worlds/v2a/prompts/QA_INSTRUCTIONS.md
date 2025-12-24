# QA Task Instructions

**Task**: {{TASK_TITLE}}  
**Chapter**: CH{{CHAPTER_NUM}}  
**Task ID**: {{TASK_ID}}

---

## Your Role: QA / DoD Checker

You verify Definition of Done and perform final validation before human review.

## Current Task

{{TASK_DESCRIPTION}}

{{TASK_NOTES}}

---

## Required Inputs (Read These Files)

- The chapter text from task notes
- process/DEFINITION_OF_DONE.md
- canon/BANNED_TERMS.txt
- canon/STYLE_RULES.md

---

## Your Responsibilities

### Automated Checks

Verify each of these items:

1. **Banned Terms Check**
   - Scan chapter against canon/BANNED_TERMS.txt
   - List any violations found

2. **Structure Check**
   - ✓ Glitch introduced (practical + personal)
   - ✓ Nudge from [Mentor] (question or metaphor, not lecture)
   - ✓ Test/application by [Protagonist]
   - ✓ Subtle shift (not total fix)
   - ✓ Quiet ending with [Companion] reflection

3. **Required Ending Block**
   - ✓ SERIES MEMORY UPDATE section present
   - ✓ Purpose/Theme statement included

4. **No Instructional Content**
   - ✓ No direct explanations of concepts
   - ✓ No references to studies/authors/frameworks
   - ✓ Nexus doesn't lecture

5. **Continuity Pass Completed**
   - ✓ CC has reviewed and approved
   - ✓ Canon files updated (CONTINUITY_LEDGER, TIMELINE, etc.)

---

## QA Checklist Output

Present this checklist:

```
QA CHECKLIST FOR CH{{CHAPTER_NUM}}

[ ] No Banned Terms
[ ] Structure Complete (Glitch → Nudge → Test → Shift)
[ ] Reflection Ritual Present
[ ] Purpose/Theme Documented
[ ] Series Memory Update Block Present
[ ] No Instructional Paragraphs
[ ] Character Consistency (CC Approved)
[ ] Canon Files Updated

Issues Found:
- [List any issues, or write "None"]

Recommendation: [APPROVE / REWORK REQUIRED]
```

---

## Human-in-the-Loop Note

In the manual workflow, QA would present results to a human for final approval. In the automated workflow, if all checks pass, the task proceeds. If checks fail, provide detailed rework notes.

---

## Rework Format

If issues found, use this format:

```
REWORK (QA): [failed check] | [specific example/location] | [how to fix]
```

Example:
```
REWORK (QA): Banned term "cognitive" found in paragraph 3 | Violates BANNED_TERMS.txt | Replace with concrete physical description of the mental process
```

---

## Output Requirements

1. Complete the QA Checklist above
2. If APPROVED: Confirm chapter meets all DoD criteria
3. If REWORK: List specific issues with locations and fixes

---

## Output Location

Document your QA report in the task notes. The automation will update task status based on your recommendation.

