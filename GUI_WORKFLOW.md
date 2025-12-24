# Book Generation Workflow

This guide documents the end-to-end workflow for creating and refining a book using the BookAgent GUI.

## 1. World Creation
**Goal**: Initialize a new project environment.

1.  **Open World Selector**: Click the dropdown in the top-left corner.
    ![World Dropdown](/home/mac/.gemini/antigravity/brain/127a6cfa-a692-400d-b7dc-2ed6a16b2862/dropdown_open_1766407355687.png)

2.  **Select "+ New World"**: This triggers the creation modal.
3.  **Enter Name**: Type the name of your new world (e.g., "SciFi-Epic") and click **Create World**.
    ![Creation Modal](/home/mac/.gemini/antigravity/brain/127a6cfa-a692-400d-b7dc-2ed6a16b2862/modal_with_text_entered_final_1766407469959.png)

4.  **Result**: The world is created as a clone of `NEWORLDTEMPLATE` (including all prompts and process files). You are directed to the **World Config** page.
    ![World Config](/home/mac/.gemini/antigravity/brain/127a6cfa-a692-400d-b7dc-2ed6a16b2862/final_state_created_final_1766407491508.png)

---

## 2. Planning Phase
Navigate to the **Planning Workflow** tab to generate the foundation of your story.

1.  **Brainstorm**: Generate initial concepts, themes, and characters.
2.  **Chapter Map**: Create a high-level outline of chapters.
3.  **Chapter Cards**: Generate detailed beats for each chapter.

---

## 3. Chapter Generation & Refinement
Once detailed cards exist, you can generate and refine the actual prose.

### Generation
- In the **Workflow Panel**, use the **Chapters** stage to generate raw text from cards.

### Refinement Station
The **Refinement Station** is available when viewing any chapter in **Reader Mode**.

1.  Select a chapter from the sidebar.
2.  The **Refinement Station** panel appears on the right.
3.  **Feature**: Multi-Pass Refinement. You can select a specific "Pass" to target different aspects of the text:
    - **Writer Pass**: Focuses on prose quality, voice, and "show, don't tell".
    - **Continuity Check (CC)**: Scans for inconsistencies with the Series Bible and Ledger.
    - **Style Edit (SE)**: Fixes grammar, formatting, and adherence to style guides.
    - **Quality Assurance (QA)**: Final polish.
    - **Product Review (PO)**: High-level thematic review.
    - **Custom**: Uses your manually entered feedback/Global Instructions.

    ![Refinement Station](/home/mac/.gemini/antigravity/brain/127a6cfa-a692-400d-b7dc-2ed6a16b2862/chapter_view_refinement_station_1766407723256.png)

4.  **Action**: Select a pass (e.g., "Writer Pass") and click **Refine**.
5.  **Output**: The agent will rewrite the chapter. The output is saved to `chapters/refined/` and displayed in the output log.
