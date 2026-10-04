#!/usr/bin/env python3
"""
古文观止 · 内容生产流水线
读一篇"作者稿"(source/*.json, 不含拼音) -> 自动注音 -> 校验 -> 生成 articles/<id>/content.json + content.js

作者稿格式见 tools/source/sample.json
"""
import json, os, re, sys
from pypinyin import pinyin, Style

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT, "tools", "source")
ART_DIR = os.path.join(ROOT, "articles")

CJK = re.compile(r"[\u3400-\u9fff\uF900-\uFAFF]")

# 全局文言多音字倾向（可按篇覆盖）
GLOBAL_OVERRIDES = {
    "恶": "wù",      # 厌恶/交恶
    "乘": "shèng",   # 战车/兵车
    "遗": "wèi",     # 赠送
    "辟": "bì",      # 躲避
    "参": "sān",     # 三
    "亟": "qì",      # 屡次
    "帅": "shuài",   # 率领
    "共叔段": "gòng shū duàn",
    "大叔": "dà shū",
}


def gen_syllables(zh, overrides):
    """按字符生成音节，跳过标点；overrides 为 phrase->"syllables" 字符串"""
    mapping = {}
    text = zh
    n = 0
    for phrase in sorted(overrides, key=len, reverse=True):
        while phrase in text:
            key = "\x01OVR%d\x01" % n
            mapping[key] = overrides[phrase].split()
            text = text.replace(phrase, key, 1)
            n += 1
    parts = re.split(r"(\x01OVR\d+\x01)", text)
    syllables = []
    for part in parts:
        if part.startswith("\x01") and part in mapping:
            syllables.extend(mapping[part])
            continue
        for ch in part:
            if CJK.match(ch):
                syllables.append(pinyin(ch, style=Style.TONE)[0][0])
    return syllables


def count_cjk(s):
    return sum(1 for ch in s if CJK.match(ch))


def build(article):
    aid = article["id"]
    overrides = dict(GLOBAL_OVERRIDES)
    overrides.update(article.get("py_overrides", {}))

    for p in article["paragraphs"]:
        for s in p["sentences"]:
            if "py" in s:
                # 已有手工拼音，校验字符数
                exp = count_cjk(s["zh"])
                got = len(s["py"].split())
                if exp != got:
                    print(f"WARN {aid}: 手工拼音字符数不符 zh={exp} py={got} :: {s['zh'][:20]}")
                continue
            syls = gen_syllables(s["zh"], overrides)
            exp = count_cjk(s["zh"])
            if len(syls) != exp:
                print(f"WARN {aid}: 音节数不符 cjk={exp} got={len(syls)} :: {s['zh'][:30]}")
            s["py"] = " ".join(syls)

    out_json = os.path.join(ART_DIR, aid, "content.json")
    out_js = os.path.join(ART_DIR, aid, "content.js")
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    raw = json.dumps(article, ensure_ascii=False, indent=2)
    with open(out_json, "w", encoding="utf-8") as f:
        f.write(raw)
    with open(out_js, "w", encoding="utf-8") as f:
        f.write("window.CONTENT = " + raw + ";\n")
    print(f"OK {aid}: {len(article['paragraphs'])}段 {sum(len(p['sentences']) for p in article['paragraphs'])}句 -> {out_json}")
    return out_json


def main():
    files = sys.argv[1:] or [f for f in os.listdir(SOURCE_DIR) if f.endswith(".json")]
    for fn in files:
        path = os.path.join(SOURCE_DIR, fn) if not os.path.isabs(fn) else fn
        with open(path, encoding="utf-8") as f:
            build(json.load(f))


if __name__ == "__main__":
    main()