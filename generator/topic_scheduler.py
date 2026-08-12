from datetime import date, timedelta
from pathlib import Path
import hashlib, random, sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
from story_lib import parse_story
TARGET = 40
PROFILES = {"qinche": ("秦彻", ["夜行车内", "任务归来", "雨夜门厅", "天台", "深夜便利店", "训练场边"]), "xiyi": ("夏以昼", ["旧街拐角", "厨房清晨", "雪后阳台", "返程航站楼", "医院走廊", "童年房间"])}
CONFLICTS = ["你想独自承担", "约定被临时打断", "误会让你沉默", "旧伤突然发作", "任务改变了返程时间", "你不愿说出真实心意"]
def main():
    today = date.today(); rng = random.Random(int(hashlib.sha256(today.isoformat().encode()).hexdigest(), 16)); used = set()
    for path in (ROOT / "content" / "stories").glob("*/*/*.md"):
        meta, _ = parse_story(path)
        if str(meta.get("created_at", "")) >= (today - timedelta(days=30)).isoformat():
            seed = meta.get("generation_seed", {}); used.add((meta.get("character"), seed.get("scene"), seed.get("conflict")))
    qinche = rng.randint(15, 25); choices = ["qinche"] * qinche + ["xiyi"] * (TARGET - qinche); rng.shuffle(choices)
    for number, character in enumerate(choices, 1):
        name, scenes = PROFILES[character]
        for _ in range(100):
            scene, conflict = rng.choice(scenes), rng.choice(CONFLICTS); signature = (character, scene, conflict)
            if signature not in used:
                used.add(signature); print(f"{number:02d} | {today:%Y%m%d}{number:03d} | {name} | {rng.choice(['canon','if','modern'])} | {rng.choice(['first_meet','close','dating','married'])} | {scene} | {conflict}"); break
        else: raise RuntimeError(f"No new seed for {character}")
if __name__ == "__main__": main()
