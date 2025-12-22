
import os

BASE = os.path.dirname(os.path.dirname(__file__))
ORDER_FILE = os.path.join(BASE, "build", "BOOK_ORDER.txt")
CHAPTERS_DIR = os.path.join(BASE, "chapters")
OUT = os.path.join(BASE, "build", "MANUSCRIPT.md")

def main():
    if not os.path.exists(ORDER_FILE):
        raise SystemExit("Missing build/BOOK_ORDER.txt")

    with open(ORDER_FILE, "r", encoding="utf-8") as f:
        files = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    parts = []
    for fn in files:
        path = os.path.join(CHAPTERS_DIR, fn)
        if not os.path.exists(path):
            raise SystemExit(f"Missing chapter file listed in BOOK_ORDER.txt: {fn}")
        parts.append(open(path, "r", encoding="utf-8").read().rstrip())

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n\n".join(parts) + "\n")

    print(f"Wrote: {OUT}")

if __name__ == "__main__":
    main()
