
import os, re, sys

BASE = os.path.dirname(os.path.dirname(__file__))
BANNED = os.path.join(BASE, "canon", "BANNED_TERMS.txt")
CHAPTERS = os.path.join(BASE, "chapters")

def load_banned():
    with open(BANNED, "r", encoding="utf-8") as f:
        terms = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    return terms

def scan_file(path, terms):
    text = open(path, "r", encoding="utf-8").read()
    hits = []
    low = text.lower()
    for t in terms:
        if t.lower() in low:
            hits.append(t)
    return hits

def main():
    terms = load_banned()
    if not os.path.isdir(CHAPTERS):
        print("No chapters/ directory found.")
        return 0

    failed = False
    for fn in sorted(os.listdir(CHAPTERS)):
        if not fn.lower().endswith(".md"):
            continue
        path = os.path.join(CHAPTERS, fn)
        hits = scan_file(path, terms)
        if hits:
            failed = True
            print(f"[FAIL] {fn}: banned terms found: {', '.join(sorted(set(hits)))}")

    if failed:
        return 1
    print("[PASS] No banned terms found in chapters/*.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
