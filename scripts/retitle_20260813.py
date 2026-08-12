"""One-off safe migration from serial labels to standalone story titles."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-13"
TITLES = {
    "20260813001": "雨停之前别走", "20260813002": "天台的第二杯热饮",
    "20260813003": "延误广播响起之后", "20260813004": "训练场的最后一盏灯",
    "20260813005": "切到一半的水果", "20260813006": "夜路的副驾驶",
    "20260813007": "围巾落在雪后", "20260813008": "薄荷糖没有那么凉",
    "20260813009": "旧街只够一把伞", "20260813010": "你回来时带了花",
    "20260813011": "门厅里的潮湿气息", "20260813012": "风把话留在天台",
    "20260813013": "航站楼没有晚安", "20260813014": "别在灯灭后逞强",
    "20260813015": "清晨的水壶先响", "20260813016": "导航声调得很低",
    "20260813017": "阳台上那一点白", "20260813018": "收银台前的沉默",
    "20260813019": "石板路上的回头", "20260813020": "远路带回的冷意",
    "20260813021": "伞尖滴落的圆点", "20260813022": "霓虹在风里晃",
    "20260813023": "返程改到明天", "20260813024": "汗水还没散尽",
    "20260813025": "窗玻璃上的薄雾", "20260813026": "路灯一盏盏后退",
    "20260813027": "呼出的白气很快散了", "20260813028": "深夜的一颗薄荷糖",
    "20260813029": "招牌在风里摇", "20260813030": "门锁响得太晚",
    "20260813031": "雨把台阶洗亮", "20260813032": "不要把话留给改天",
    "20260813033": "行李箱轮子响了一声", "20260813034": "金属气味还在",
    "20260813035": "没切完的水果", "20260813036": "车窗外的长夜",
    "20260813037": "栏杆上的新雪", "20260813038": "冷柜嗡鸣的夜",
    "20260813039": "拐角处的脚步声", "20260813040": "夜色带回来的花",
}

for path in sorted((ROOT / "content" / "stories" / DATE).glob("*/*.md")):
    text = path.read_text(encoding="utf-8")
    match = re.search(r'^title: "(.+)"$', text, re.M)
    if not match:
        raise SystemExit(f"missing title: {path}")
    identifier = re.search(r'^id: "(\d{11})"$', text, re.M)
    if not identifier or identifier.group(1) not in TITLES:
        raise SystemExit(f"unknown story id: {path}")
    title = TITLES[identifier.group(1)]
    if match.group(1) == title and path.name == f"{title}.md":
        continue
    target = path.with_name(f"{title}.md")
    if target.exists():
        raise SystemExit(f"target exists: {target}")
    text = text[:match.start(1)] + title + text[match.end(1):]
    path.unlink()
    target.write_text(text, encoding="utf-8")
    print(target.relative_to(ROOT))
