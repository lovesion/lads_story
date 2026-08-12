from datetime import datetime, timezone
import json
from pathlib import Path
from story_lib import parse_story, validate
root = Path(__file__).resolve().parents[1]; grouped = {}
for path in sorted((root / "content" / "stories").glob("*/*.md")):
    meta, body = parse_story(path); errors = validate(meta, body, path)
    if errors: raise SystemExit(f"Cannot index {path}: {'; '.join(errors)}")
    keys = ("id", "title", "fandom", "character", "world", "relationship_stage", "characters", "tags", "length", "word_count", "created_at", "generation_seed")
    item = {key: meta[key] for key in keys}; item["summary"] = meta.get("summary", ""); item["path"] = path.relative_to(root).as_posix()
    grouped.setdefault(meta["created_at"], []).append(item)
dates = [{"date": key, "count": len(value), "stories": sorted(value, key=lambda story: story["id"])} for key, value in sorted(grouped.items(), reverse=True)]
output = {"version": 1, "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"), "dates": dates}
(root / "metadata").mkdir(exist_ok=True)
(root / "metadata" / "index.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote metadata/index.json with {sum(day['count'] for day in dates)} stories.")
