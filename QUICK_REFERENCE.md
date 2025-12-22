# Quick Reference Card - BookAgent GUI

## 🚀 Essential GUI Commands

### Start the System
1. **Backend**: `source gui/backend/venv/bin/activate && python gui/backend/main.py`
2. **Frontend**: `cd gui/client && npm run dev`
3. **Visit**: `http://localhost:5173`

### World Management
- **New World**: Click dropdown -> `+ New World`.
- **Auto-Generate**: Use `AI: [instruction]` in Theme/Glitch fields and click **Auto-Generate (AI)**.

### Planning Pipeline
- **Brainstorm**: In the Planning tab, click **Generate from Source**.
- **Rate**: Approving concepts requires a **3+ star** rating.
- **Refresh**: The GUI auto-updates once Agent tasks finish (via log polling).

---

## 📂 File Structure

| Folder | Contents |
|--------|----------|
| `worlds/` | All projects (worlds) |
| `worlds/[name]/canon/` | World configuration and Bibles |
| `worlds/[name]/chapters/` | Drafted chapter prose |
| `worlds/[name]/planning/` | Brainstorms, Maps, and Cards |
| `prompts/` | AI system instructions |
| `gui/` | Backend and Frontend code |

---

## 🛠️ Advanced (CLI)

> [!NOTE]
> The GUI is the preferred interface. Use these CLI tools only for debugging.

```bash
# Refine a specific chapter manually
python scripts/refine_chapters.py --world [name] --chapter [num] --type writer

# Generate a storyline/timeline
python scripts/generate_storyline.py --world [name]
```

## 📄 Documentation
- `README.md` - Setup and feature overview.
- `GUI_WORKFLOW.md` - Step-by-step visual guide.
- `archive/` - Legacy CLI documentation.
