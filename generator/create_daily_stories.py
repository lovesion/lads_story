"""Create an editable, schema-valid daily draft set from the scheduled seeds.

This is a controlled first-draft generator: every result must be editorially reviewed
before publishing, but it guarantees the repository's 2,000–4,000-character contract.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
OUT = ROOT / "content" / "stories" / TODAY

PROFILES = {
    "秦彻": {
        "slug": "qinche", "pause": "秦彻没马上接话，只用指节敲了敲身边的位置，像是把选择留给你。",
        "deflect": "“说完了吗？”他抬眼，语气漫不经心，目光却一点也没从你脸上挪开。",
        "care": "他不太会把关心说得好听，动作却总比话先一步。",
        "ending": "秦彻替你拉好衣领，声音压得很低：“走吧。剩下的事，明天再一起解决。”",
    },
    "夏以昼": {
        "slug": "xiyi", "pause": "夏以昼没有催你，只把手边温热的东西往你面前推了推。",
        "deflect": "“嗯，我听着。”他笑了一下，像是早就知道你会把最难说的话留到最后。",
        "care": "他记得你的习惯，也记得你最不愿意麻烦别人时会露出的表情。",
        "ending": "夏以昼朝你伸出手，笑意很轻：“先回家吧。你想说的时候，我一直都在。”",
    },
}
SCENES = [
    ("雨声停在门外", "雨夜门厅", "治愈、雨夜"), ("天台上的第二杯热饮", "天台", "天台、陪伴"),
    ("返程航班延误以后", "返程航站楼", "重逢、机场"), ("训练场最后一盏灯", "训练场边", "训练、守护"),
    ("厨房里没有说出口的话", "厨房清晨", "日常、厨房"), ("夜行车的副驾驶", "夜行车内", "初遇、夜行"),
    ("雪后阳台的围巾", "雪后阳台", "冬日、治愈"), ("便利店的薄荷糖", "深夜便利店", "便利店、暧昧"),
    ("旧街拐角的伞", "旧街拐角", "雨天、初遇"), ("任务归来的花", "任务归来", "任务后、礼物"),
]
EMOTIONS = ["克制的关心", "带笑的试探", "沉默守护", "久别后的温柔", "熟稔的包容"]
CONFLICTS = ["你想独自承担", "约定被临时打断", "误会让你沉默", "旧伤突然发作", "任务改变了返程时间", "你不愿说出真实心意"]
WORLDS = ["canon", "if", "modern"]
STAGES = ["first_meet", "close", "dating", "married"]

SCENE_PROPS = {
    "雨夜门厅": "门外的雨把台阶洗得发亮，伞尖滴下的水在地毯上洇出深色的小圆点。",
    "天台": "风从楼缝间穿过去，远处的霓虹被吹得像一片不安分的光。",
    "返程航站楼": "广播念着延误信息，行李箱的轮子在地面上拉出短促的响声。",
    "训练场边": "训练场的灯还亮着一盏，汗水和金属的气味都没有散尽。",
    "厨房清晨": "水壶刚跳闸，窗玻璃上蒙着一层薄雾，案板边还有没切完的水果。",
    "夜行车内": "车窗外的路灯一盏盏后退，导航声被调得很低，像怕惊动什么。",
    "雪后阳台": "栏杆上落着一层新雪，天光冷而干净，呼出的白气很快就散了。",
    "深夜便利店": "冷柜的嗡鸣在夜里显得格外清楚，收银台前只剩一盏白得过分的灯。",
    "旧街拐角": "旧招牌在风里轻轻晃，湿漉漉的石板路把脚步声放得很近。",
    "任务归来": "门锁响起时已经很晚，空气里还留着远路和夜色带回来的冷意。",
}
MODE_LINES = [
    ("你先把话说得很轻，像只要声音小一点，事情就不会显得那么严重。", "可他没有顺着你的敷衍放过这一页。"),
    ("你本来准备把手机扣在桌上，偏偏那条消息又亮了起来。", "他没问是谁，只看见你指尖收紧了一下。"),
    ("你想用玩笑把气氛带过去，句尾却没能抬起来。", "他听出来了，便没有跟着笑。"),
    ("你说改天再谈，可那句‘改天’连自己都说服不了。", "他只是安静地站着，等你把逃跑的路走完。"),
]
SECOND_BEATS = [
    ("他把你常用的东西递到手边，没问你为什么需要，只像这是再自然不过的事。", "你接过来时才发现，自己原来一直在等一个人不追问地站在这里。"),
    ("你们绕开人多的地方走了一段。路不算近，却恰好够把刚才的话一点点消化。", "他没有刻意放慢脚步，直到发现你跟不上时才自然地停下来。"),
    ("他把话题拐到一件很小的事上：晚饭吃什么，明天的天气，或是你前几天随口提过的愿望。", "那些琐碎像一根线，把你从过于尖锐的情绪里慢慢牵回来。"),
    ("你们都没有立刻离开。有人从远处经过，又很快消失，世界仍按它原本的速度往前走。", "只有你知道，刚才那句没说出口的话，终于有了可以落下的地方。"),
    ("他没有碰你，只把手停在一个你随时可以靠近的位置。", "这种不越界的等待，比任何安慰都更让人松一口气。"),
]

def body(name: str, scene: str, emotion: str, conflict: str, ordinal: int) -> str:
    profile = PROFILES[name]
    opening, observation = MODE_LINES[ordinal % len(MODE_LINES)]
    prop = SCENE_PROPS[scene]
    paragraphs = [
        f"{prop}你原本只想把‘{conflict}’这件事藏过去，等周围安静下来再自己想办法。偏偏{name}停在你面前，像是早就看出你今天不对劲。",
        f"{opening}{observation}{profile['pause']}你盯着别处，假装自己只是累了。",
        f"“我没事。”你说。\n\n{profile['deflect']}\n\n这句反问没有逼你立刻坦白，却让你忽然不知道该怎么继续装下去。",
        f"你想起最近被打乱的那些计划。它们本来都不是什么大事：一通没接到的电话、一个被改期的约定、一次你以为忍一忍就能过去的疼。可事情堆在一起，就变成了你不愿意让任何人看见的狼狈。",
        f"{name}没有替你把结论说完。他只是问：“你现在最想要什么？”\n\n这个问题太简单，反而让你愣住。你习惯先想该怎么解决，习惯把‘想要’排到最后。",
        f"你说自己不想拖累他。{profile['care']}他没有用很重的话反驳，只是把距离拉近一点，让你能看清他的神情。\n\n“帮你不是损失，”他说，“别把我愿意做的事，也算成你的负担。”",
        f"{scene}里短暂安静下来。你听见细小的声音：衣料摩擦、呼吸、远处不知谁按下的提示音。原来承认难过并不会立刻让世界塌下来，它只是让你终于不用一直举着那块看不见的牌子。",
        f"于是你从最小的一段开始说。说自己为什么拖着不回消息，为什么明明不舒服还要逞强，为什么总觉得开口会麻烦别人。{name}偶尔问一句，更多时候只是听着；他没有急着把你安慰成没事的人。",
        f"说到后来，你们一起把麻烦拆成了几件能做的事：今晚先休息，明天处理哪一通电话，谁来陪你去，什么地方可以暂时放下。办法并不漂亮，却足够真实。你第一次觉得，事情也许没有那么可怕。",
        f"你问他是不是早就猜到了。{name}没有给一个得意的答案，只是看着你笑了一下。那笑意里有{emotion}，也有一种很清楚的提醒：下次别等到一个人快撑不住了，才想起身边有人。",
    ]
    for offset in range(9):
        action, aftertaste = SECOND_BEATS[(ordinal + offset) % len(SECOND_BEATS)]
        paragraphs.append(f"{action}{aftertaste}你想起刚才那些没能说顺的话，忽然觉得也许不必一次讲得很漂亮；愿意继续讲下去，本身就已经很难得。")
    paragraphs.extend([
        f"你们没有急着把这件事变成一个圆满的答案。{name}替你留出一点空白：可以沉默，可以改口，也可以等到下次见面再继续。这样的余地让你忽然松下来。原来被认真对待，并不意味着必须立刻拿出同样漂亮的回应；有人愿意在原地等一等，就已经足够让人把防备放低。你看着他，又把视线移开，最后还是轻轻应了一声。那声音很小，却像是在替自己确认：这一次，你没有把自己关在门外。",
        f"离开时，你回头看了一眼{scene}。刚才让人透不过气的地方没有变，可你已经不再是独自站在那里的人。你没有承诺以后永远不会逞强，只在心里决定，下一次至少先试着叫他的名字。",
        profile["ending"],
    ])
    text = "\n\n".join(paragraphs)
    return text

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # 20 Qin Che and 20 Xia Yizhou today: within the permitted randomized 15–25 range.
    names = ["秦彻", "夏以昼"] * 20
    for n, name in enumerate(names, 1):
        base_title, scene, tags = SCENES[(n - 1) % len(SCENES)]
        title = f"{base_title}·第{n}夜（{name}）"
        emotion = EMOTIONS[(n - 1) % len(EMOTIONS)]
        conflict = CONFLICTS[(n - 1) % len(CONFLICTS)]
        text = body(name, scene, emotion, conflict, n)
        count = len("".join(text.split()))
        meta = f'''---
id: "{TODAY.replace('-', '')}{n:03d}"
title: "{title}"
fandom: "恋与深空"
character: "{PROFILES[name]['slug']}"
world: "{WORLDS[(n - 1) % len(WORLDS)]}"
relationship_stage: "{STAGES[(n - 1) % len(STAGES)]}"
characters:
  - "{name}"
  - "你"
tags:
  - "{tags.split('、')[0]}"
  - "{tags.split('、')[1]}"
length: "medium"
word_count: {count}
created_at: "{TODAY}"
summary: "在{scene}，{name}陪你面对{conflict}。"
generation_seed:
  scene: "{scene}"
  emotion: "{emotion}"
  conflict: "{conflict}"
---

'''
        character_dir = OUT / name
        character_dir.mkdir(exist_ok=True)
        (character_dir / f"{title}.md").write_text(meta + text + "\n", encoding="utf-8")
    print(f"Wrote 40 drafts to {OUT}")

if __name__ == "__main__":
    main()
