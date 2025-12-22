
import os, sys

BASE = os.path.dirname(os.path.dirname(__file__))
CHAPTERS = os.path.join(BASE, "chapters")

REQUIRED_ENDING_MARKER = "SERIES MEMORY UPDATE"

def main():
    if not os.path.isdir(CHAPTERS):
        print("No chapters/ directory found.")
        return 0

    failed = False
    for fn in sorted(os.listdir(CHAPTERS)):
        if not fn.lower().endswith(".md"):
            continue
        path = os.path.join(CHAPTERS, fn)
        text = open(path, "r", encoding="utf-8").read()
        if "---\n" not in text or REQUIRED_ENDING_MARKER not in text:
            failed = True
            print(f"[FAIL] {fn}: missing required ending block ('---' + {REQUIRED_ENDING_MARKER})")

    if failed:
        return 1
    print("[PASS] Structure checks OK for chapters/*.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
