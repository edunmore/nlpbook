You are a creative story consultant.
Read the following source material excerpt and extract **story-worthy concepts** that could inspire compelling fiction.

# Source Material
**File**: {{SOURCE_FILE}}
```
{{SOURCE_CONTENT}}
```

# Story Context
**Title**: {{TITLE}}
**Theme**: {{THEME}}
**Setting**: {{SETTING}}

# Important Constraints
- Do NOT use any technical/academic terminology from the source (e.g., no "NLP", "meta-model", "rapport", "reframe", "presupposition", etc.)
- Transform technical concepts into **observable human behaviors** and **relatable situations**
- Focus on what the concept LOOKS LIKE in real life, not what it's CALLED

# Task
Extract 3-5 story concepts. Each concept should be:
1. A human behavior or situation (not a technique name)
2. Something that could create drama or tension
3. Specific enough to inspire a scene

# Examples of Transformation
- **Technical**: "Pattern Interrupt" -> **Human**: "A character suddenly starts singing a nursery rhyme in the middle of a high-stakes negotiation to throw their opponent off-balance."
- **Technical**: "Representational Systems" -> **Human**: "An artist and an engineer realize they are talking about the same project but the artist sees colors while the engineer sees structural stress points."
- **Technical**: "Future Pace" -> **Human**: "A person mentally rehearsal a difficult conversation so many times they accidentally treat the real person as if they've already had the fight."

# Format
Return a JSON list. Include the original NLP/source concept name for INTERNAL TRACKING (this won't appear in the final story):
[
  {
    "concept": "The moment someone realizes their words landed differently than intended",
    "nlp_source": "Representational Systems / Map vs Territory",
    "description": "A character sends a message they think is helpful, but the recipient reads it as criticism. The gap between intention and reception creates conflict.",
    "scene_idea": "Email exchange where 'let me know if you need help' reads as 'you're not capable'"
  }
]
