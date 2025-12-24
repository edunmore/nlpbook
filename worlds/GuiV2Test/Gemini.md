# Gemini Agent Context

You are an AI assistant collaborating on a book project. The current directory is the root of a specific **World** where the story takes place.

## File Structure
- `canon/`: Contains the immutable truths of this world.
  - `world_config.json`: Technical configuration (title, theme, settings).
  - `SERIES_BIBLE.md`: The core literary guide (premise, characters, theme).
  - `TIMELINE.md`: The chronological sequence of events.
  - `CONTINUITY_LEDGER.md`: Tracks facts and state to prevent plot holes.
- `chapters/`: The actual book content.
  - `CH{N}.md`: Individual chapters.
- `planning/`: Brainstorming and structural documents.
  - `BRAINSTORM_RAW.json`: Raw ideas extracted from source material.
  - `CHAPTER_MAP.md`: High-level outline of chapters.
  - `chapter-cards/`: Detailed plans for each chapter.
- `prompts/`: Instructions for your specific tasks.
- `history/`: Logs of previous interactions.

## Your Goal
Your primary goal is to help write a cohesive, high-quality story that adheres to the constraints and style defined in the `canon/` directory. Always respect the existing lore and character voices.
