#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量生成《古文观止》文章封面插图（sensenova 绘本风 + 自动去水印）"""
import json, os, sys, time, urllib.request, urllib.error

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\royli\.agents\skills\sensenova-u1-image\scripts')

API_KEY = os.environ.get('SENSENOVA_API_KEY', '')
BASE_URL = 'https://token.sensenova.cn/v1'
COVER_DIR = r'D:\古文观止\assets\covers'

STYLE = ('Colorful flat children\'s picture book illustration, ancient Chinese story scene, '
         'warm inviting colors, soft rounded shapes, cute hand-drawn style, no photo, no 3D, '
         'no realistic rendering. No text, no words, no letters, no numbers, no labels, no watermark. '
         'Full-bleed composition, fill the entire canvas from top to bottom, no empty areas.')

PROMPTS = {
  "v01-002": "A young prince of the Zhou royal family and a young prince of the Zheng state exchanging tokens of trust at a grand ancient hall, two cute boys in royal robes bowing politely to each other, scrolls and bronze goblets on the table, soft golden light.",
  "v01-003": "A wise old minister with a white beard earnestly advising a young duke on a palace terrace, beside them a spoiled little prince playing with a toy sword, worried royal consort standing behind a pillar, warm palace setting.",
  "v01-004": "A young duke watching fishermen catch fish at a river shore, elegant ancient Chinese robes, an old court minister with a worried face bowing to stop him, clear river water, willow trees, spring day.",
  "v01-005": "A confident king in royal robes assigning two loyal officers to guard the two sides of a small conquered city, maps and banners, warm morning light on ancient walls, respectful courtiers.",
  "v01-006": "An old minister in ceremonial court robes raising his hand to advise before a great bronze tripod being carried into a grand ancestral temple, solemn ancient hall, the king looking hesitant.",
  "v01-007": "A wise counselor holding his arm out to stop an eager duke from charging into battle, soldiers waiting behind, rolling green hills and banners, tense but hopeful morning scene.",
  "v01-008": "A wise strategist and a duke riding a war chariot into a great ancient battlefield, flags waving, brave soldiers marching, dramatic but friendly picture-book scene, green fields under blue sky.",
  "v01-009": "A brave diplomat and a powerful duke riding side by side viewing a grand army formation on a plain, rows of banners and shields, mountains in the distance, confident yet peaceful atmosphere.",
  "v01-010": "A wise old minister pleading with a greedy duke at a castle gate, two small kingdoms shown as two cute houses side by side, one house collapsing making the other shake, moral fable style.",
  "v01-011": "A great duke in royal robes kneeling respectfully to receive a sacred roasted meat offering on a golden plate, a royal messenger standing before him, grand ceremonial hall, respectful mood.",
  "v01-012": "A clever diplomat in scholar robes talking calmly with a powerful king across a low table, ancient maps and tea, two states' flags behind them, diplomatic warm light.",
  "v01-013": "A kind but stubborn king in armor on a riverbank watching the enemy soldiers crossing a wide river, his general pointing forward urgently wanting to attack, the king refusing, dramatic river scene.",
  "v01-014": "A court eunuch kneeling before a newly enthroned duke in a palace garden, the duke listening seriously, hidden guards in the background, morning light through ancient trees.",
  "v01-015": "A kind mother and her virtuous son walking together into misty green mountains, carrying simple bundles, leaving the palace far behind, peaceful spring scenery, path winding into the hills.",
  "v01-016": "A brave official in scholar robes presenting gifts to a huge visiting army at the border, the enemy commander looking surprised and thoughtful, ancient city walls and banners, tense standoff.",
  "v01-017": "An old wise man lowered by rope from high city walls at night, landing to speak with a surprised king beside a war camp fire, moonlight, ancient towers, dramatic night scene.",
  "v01-018": "An old white-bearded minister crying as he sees an army marching away through a mountain pass, his son looking back sadly, the king watching sternly, misty mountain pass at dawn.",
  "v02-001": "A court official of a small state handing a long letter scroll with both hands to the chief minister of a powerful state in a grand hall, the minister reading it carefully, candlelight, solemn diplomatic scene.",
  "v02-002": "A wise young minister of the Zhou court calmly pointing at three huge bronze tripods, a powerful king in armor standing before them looking curious, grand ancient hall, the tripods glowing warmly.",
  "v02-003": "A dignified diplomat standing tall speaking firmly before the war camp of a victorious army, pointing back toward his homeland, the enemy general listening uneasily, banners and tents at dusk.",
  "v02-004": "A captive officer being released at a border gate between two kingdoms, the king of the other state politely seeing him off, the officer bowing respectfully but proudly, ancient border gate, morning light.",
  "v02-005": "An eloquent minister reciting a long list of grievances to a king across a table, maps and old treaty scrolls scattered about, the king's face turning embarrassed, ancient hall.",
  "v02-006": "A proud leader of a mountain tribe standing calmly answering before a gathering of dukes, sheep and tents behind him, green mountains, the duke of Jin looking impressed and ashamed.",
  "v02-007": "An old white-haired retired minister riding a fast chariot toward the palace, eagerly pleading before the prime minister to pardon a wrongly imprisoned officer, palace gates, sunrise.",
  "v02-008": "A wise minister of Zheng handing a letter to the powerful minister of Jin, treasure chests of gold on the table beside them, the Jin minister thinking deeply, warm diplomatic hall.",
  "v02-009": "A dignified minister standing outside a grand mansion gate after a king's death, bowing respectfully, royal guards watching, a tragic but noble morning scene, neither fleeing nor kneeling to please.",
  "v02-010": "A refined young prince sitting in a grand hall listening to musicians playing ancient instruments, drums, bells and flutes around, dancers in flowing robes, warm ceremonial light.",
  "v02-011": "Workers carefully taking apart the wall of a guest house while a small delegation stores horses and carts inside, the host minister arriving surprised, ancient courtyard, bright day.",
  "v02-012": "An old wise minister explaining to a younger duke with a pair of scissors and a roll of beautiful silk on the table, a young boy practicing archery in the background, teaching scene.",
  "v02-013": "A diplomat politely refusing a grand procession of soldiers at a city gate, wedding banners and bridal gifts, the soldier general looking hesitant, the gate firmly held.",
  "v02-014": "A king in a fur hat and cloak talking with a wise advisor inside a grand tent, snow falling outside, a map and a bronze tripod model on the table, warm lantern light.",
  "v02-015": "A wise old minister lying sick in bed giving final advice to a younger officer, a bright fire burning in the fireplace, a gentle river visible through the window, calm but meaningful scene.",
  "v02-016": "A defeated king kneeling to offer peace terms before a proud victorious king, a wise old general standing behind frowning and shaking his head, ancient battlefield with banners.",
}

from remove_watermark import remove_watermark


def gen_one(prompt, output_path):
    for attempt in range(4):
        try:
            body = {
                "model": "sensenova-u1-fast",
                "prompt": prompt,
                "size": "2752x1536",
                "n": 1,
            }
            req = urllib.request.Request(
                f"{BASE_URL}/images/generations",
                data=json.dumps(body).encode('utf-8'),
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            url = data['data'][0]['url']
            with urllib.request.urlopen(urllib.request.Request(url), timeout=120) as r2:
                img_data = r2.read()
            with open(output_path, 'wb') as f:
                f.write(img_data)
            from PIL import Image
            img = Image.open(output_path)
            clean, bbox = remove_watermark(img)
            if bbox is not None:
                clean.save(output_path)
                return f'OK 去水印{bbox}'
            return 'OK 无水印'
        except Exception as e:
            print(f'  尝试{attempt+1}失败: {e}')
            time.sleep(8)
    return 'FAIL'


def main():
    prompts_file = None
    ids = []
    for a in sys.argv[1:]:
        if a.startswith('--prompts='):
            prompts_file = a.split('=', 1)[1]
        else:
            ids.append(a)
    if prompts_file:
        extra = json.load(open(prompts_file, encoding='utf-8'))
        PROMPTS.update(extra)
    ids = ids or list(PROMPTS.keys())
    for aid in ids:
        out = os.path.join(COVER_DIR, aid + '.png')
        if os.path.exists(out) and len(open(out, 'rb').read()) > 50000:
            print(f'{aid}: 已存在，跳过')
            continue
        if aid not in PROMPTS:
            print(f'{aid}: 缺 prompt，跳过')
            continue
        print(f'{aid}: 生成中...')
        t0 = time.time()
        result = gen_one(STYLE + ' Scene: ' + PROMPTS[aid], out)
        print(f'{aid}: {result} ({time.time()-t0:.0f}s)')
    print('全部完成')


if __name__ == '__main__':
    main()