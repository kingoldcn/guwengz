#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 articles/*/content.json 完整性与拼音对齐"""
import json, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
CJK = re.compile(r'[\u3400-\u9fff\uF900-\uFAFF]')
ROOT = r'D:\古文观止'
bad = []

articles = json.load(open(os.path.join(ROOT, 'data', 'articles.json'), encoding='utf-8'))
volumes = {}
for a in articles:
    volumes.setdefault(a['id'][:3], []).append(a)
for vkey in sorted(volumes):
    vs = volumes[vkey]
    print(f'{vkey} 目标 {len(vs)} 篇')
    for a in vs:
        aid = a['id']
        d = os.path.join(ROOT, 'articles', aid)
        if not os.path.exists(os.path.join(d, 'content.json')) or not os.path.exists(os.path.join(d, 'content.js')):
            bad.append(aid + ' 缺文件')
            continue
        c = json.load(open(os.path.join(d, 'content.json'), encoding='utf-8'))
        for p in c['paragraphs']:
            for s in p['sentences']:
                if 'py' not in s:
                    bad.append(aid + ' 缺拼音')
                    break
                n_cjk = sum(1 for ch in s['zh'] if CJK.match(ch))
                n_py = len(s['py'].split())
                if n_cjk != n_py:
                    bad.append(f'{aid} 音字不符 cjk={n_cjk} py={n_py}: {s["zh"][:20]}')
        if not c.get('notes'):
            bad.append(aid + ' 缺注释')
        if not c.get('appreciation'):
            bad.append(aid + ' 缺赏析')
        if not c.get('background'):
            bad.append(aid + ' 缺背景')

print('完成')
if bad:
    print('问题:')
    for b in bad:
        print(' -', b)
else:
    print('全部通过：所有篇目均有 content.json/js、拼音对齐、注释/赏析/背景齐全')