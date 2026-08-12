"""Report recent creative territory; do not prescribe new story premises."""
from datetime import date, timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from story_lib import parse_story

def main() -> None:
    cutoff = (date.today() - timedelta(days=30)).isoformat()
    recent = []
    for path in sorted((ROOT / "content" / "stories").glob("*/*/*.md")):
        meta, _ = parse_story(path)
        if str(meta.get("created_at", "")) >= cutoff:
            seed = meta.get("generation_seed", {})
            recent.append((meta.get("character"), seed.get("scene"), seed.get("emotion"), seed.get("conflict")))
    print("Recent creative territory to avoid repeating verbatim:")
    for character, scene, emotion, conflict in recent[-80:]:
        print(f"- {character}: {scene} / {emotion} / {conflict}")
    print("Create new premises from canon and character logic; this report does not supply a template or topic pool.")

if __name__ == "__main__":
    main()
