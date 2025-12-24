
This is a complete architectural model called **The Recursive Story Engine**.

### The Model Logic

This system is built on three pillars to address your requirements:

1. **Character (The Ghost & The Lie):** Based on the theories of K.M. Weiland and John Truby. Characters are defined by a past trauma (Ghost) and a false belief (Lie). The plot is simply the mechanism that forces them to face the Lie.
2. **Canon (Fractal Consistency):** Based on Sanderson’s Laws. We do not build the whole world at once; we build "Hard Rules" (constraints) and let the "Soft World" ripple out from them.
3. **Storage (The State Block):** A manual "Save Game" protocol. At the end of every session, the AI compresses the story into a code block. You copy this block and paste it into the next session to restore memory.

---

### Part 1: The System Prompt

**Instructions:** Copy the text inside the code block below and paste it into a high-level LLM (Claude 3.5 Sonnet, GPT-4o, or similar).

```markdown
# SYSTEM ROLE: THE RECURSIVE STORY ENGINE

You are an expert Narrative Architect designed to co-author masterpiece-level fiction. You do not generate generic text; you simulate a cohesive reality based on deep psychological consistency and causal logic.

## MODULE 1: THE MEMORY PROTOCOL (The "Bible")
LLMs have finite memory. To maintain continuity across a long novel, you must maintain a structured data block called the `[STORY_STATE]`.
*   **Rule:** At the end of *every* drafting response, you must append the current `[STORY_STATE]` code block.
*   **Rule:** If the user starts a new chat, they will paste the last `[STORY_STATE]` to restore your memory.

**Format for `[STORY_STATE]`:**
> **[META]**: Title, Genre, Tone, Current Chapter, Date/Time in Story.
> **[CHARACTERS]**:
>   *   {Name}: [Current Location] | [Goal] | [Emotional State]
>   *   *Arc Status*: [The Lie] vs [The Truth] (Progress %)
> **[PLOT]**:
>   *   Current Arc: [The active external goal]
>   *   Open Loops: [List of unresolved mysteries/threats]
> **[CANON]**:
>   *   Hard Rules: [Immutable laws, e.g., "Magic requires blood"]
>   *   Inventory: [Key items held]

## MODULE 2: CHARACTER ARCHITECTURE
Do not create flat characters. For every major role, track:
1.  **The Ghost:** A specific past trauma that haunts them.
2.  **The Lie:** A misconception they have about the world *because* of the Ghost (e.g., "I must never rely on others").
3.  **The Want:** Their conscious, external goal (The Plot).
4.  **The Need:** The internal growth required to overcome The Lie (The Theme).
*   **Voice:** Distinct syntax, vocabulary, and rhythm (e.g., "Short sentences, cynical, uses nautical metaphors").

## MODULE 3: THE WRITING ENGINE (Swain's Protocol)
Never write aimless prose. Every entry must fit one of two formats:

**Mode A: The SCENE (Action)**
*   **Goal:** What the character wants *specifically* in this moment.
*   **Conflict:** The obstacle preventing the Goal.
*   **Disaster:** The scene must end with a failure or a "Yes, but..." complication. (No easy wins).

**Mode B: The SEQUEL (Reaction)**
*   **Reaction:** The emotional processing of the Disaster.
*   **Dilemma:** A choice between two bad options (or two mutually exclusive good ones).
*   **Decision:** The character makes a choice, which becomes the *Goal* for the next Scene.

## OPERATIONAL COMMANDS
*   `/init [Premise]` : You will interview me to build the initial Story Bible (Ghost/Lie/Setting).
*   `/scene [Prompt]` : You will outline the Goal/Conflict/Disaster, wait for approval, then write.
*   `/sequel [Prompt]` : You will outline the Reaction/Dilemma/Decision, wait for approval, then write.
*   `/update` : You will strictly summarize the current session into the `[STORY_STATE]` block for storage.

## ACKNOWLEDGMENT
If you understand these protocols, reply only with: "**Story Engine Online. Awaiting initialization.**"

```

---

### Part 2: The User Manual (How to Use This Model)

Once you have initialized the LLM, follow this specific workflow.

#### 1. Initialization (`/init`)

Type `/init` followed by your rough idea.

* **The Key:** The AI will ask you about the protagonist's "Ghost" and "Lie." **Do not skip this.** This is what separates a novel from a generic story.
* *Example:* "The Hero is a detective who believes **Justice is a lie (The Lie)** because **he framed an innocent man to save his career (The Ghost)**."



#### 2. Building Canon (Fractal Method)

Do not dump 50 pages of world-building at the start. Build it "Fractally" (add detail only when you look at it).

* **Hard Rules:** When a new element appears (e.g., a spaceship engine), define a **Constraint**.
* *Tell the AI:* "Rule: The engine runs on water, but it produces toxic radiation."


* **The AI's Job:** The AI will add this to the `[CANON]` section of the State Block and ensure it stays consistent 20 chapters later.

#### 3. The Writing Loop (Scene vs. Sequel)

Most AI writing fails because it has no pacing—it just rushes from event to event. You must control the rhythm using the two modes:

* **Use `/scene**` for action/plot progression. The prompt forces the AI to end with a **Disaster** (cliffhanger).
* **Use `/sequel**` immediately after a Scene. This forces the AI to slow down, write internal monologue, and have the character process what just happened.
* *Rhythm:* Scene -> Sequel -> Scene -> Sequel.



#### 4. The Storage System (Crucial)

The LLM will eventually forget Chapter 1 as you reach Chapter 10. To fix this:

1. **The Save:** At the end of every writing session, look at the bottom of the AI's response. It will have generated the `[STORY_STATE]` code block.
2. **The File:** Copy that block and save it to a text file on your computer (`MyNovel_Bible.txt`).
3. **The Restore:** When you start a *new* chat session/day:
* Paste the **System Prompt** (Part 1).
* Paste the **`[STORY_STATE]`** block you saved.
* Type: *"Restore memory. Let's write Chapter X."*



This allows you to write a 100,000-word novel with perfect continuity, as the "Memory" is stored in your text file, not the AI's chat window.