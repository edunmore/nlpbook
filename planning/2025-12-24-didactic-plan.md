# Refine Didactic Output Plan

## Goal Description
We aim to test and refine the "Didactic Fiction" generation logic (also known as "Phoenix Logic") using real transcript data. The goal is to ensure the `AGENT_DIDACTIC_ARCHITECT` prompt produces high-quality "business fables" that translate abstract concepts into engaging, human-centric narratives without purely expository interaction.

## User Review Required
> [!IMPORTANT]
> Success relies on the quality of the `AGENT_DIDACTIC_ARCHITECT` prompt. I will need to iterate on this prompt based on the output from real transcripts.

## Proposed Changes

### 1. Verification & Testing
- Run `generate_didactic_story.py` (or the recursive engine equivalent) against a sample NLP transcript.
- Analyze the output for:
    - **Narrative Arc**: Does it have conflict, rising action, and resolution?
    - **Concept Encoding**: Are specific business/NLP concepts encoded into events rather than dialogue dumps?
    - **Tone**: Is it consistent with valid business fable genre norms?

### 2. Prompt Tuning
- **[MODIFY] [didactic_architect.yaml](file:///home/mac/projects/nlpbook/agents/didactic_architect.yaml)** (or equivalent prompt file)
    - Adjust instructions to force "Show, Don't Tell".
    - Refine structural requirements (Act 1/2/3).

### 3. Frontend Check
- Verify the "Generate Fable" button in the Brainstorm Review page correctly triggers this flow.

## Verification Plan
### Automated Tests
- None specific (mostly qualitative).

### Manual Verification
- Generate a story from `NLP/transcripts/sample.txt` (or similar).
- Review generated markdown in `worlds/[WorldName]/chapters/`.
