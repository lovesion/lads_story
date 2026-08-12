from pathlib import Path
import sys
from story_lib import parse_story, validate
root = Path(__file__).resolve().parents[1]; seen, failures = set(), []
for path in sorted((root / "content" / "stories").glob("*/*/*.md")):
    try:
        meta, body = parse_story(path); errors = validate(meta, body, path); story_id = str(meta.get("id", ""))
        if story_id in seen: errors.append("duplicate id")
        seen.add(story_id); failures.extend(f"{path.relative_to(root)}: {error}" for error in errors)
    except Exception as exc: failures.append(f"{path.relative_to(root)}: {exc}")
if failures: print("Validation failed:\n" + "\n".join(failures)); sys.exit(1)
print(f"Validated {len(seen)} story file(s).")
