#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交叉检查：页面 JS 引用的元素是否都存在"""
import re, io, sys, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\古文观止'
pages = {
    'index.html': ['js/common.js'],
    'volume.html': ['js/common.js', 'js/volume.js'],
    'article.html': ['js/common.js', 'js/article.js'],
    'authors.html': ['js/common.js', 'js/authors.js'],
    'quotes.html': ['js/common.js', 'js/quotes.js'],
    'progress.html': ['js/common.js', 'js/progress.js'],
}

ok = True
for page, scripts in pages.items():
    html = open(os.path.join(ROOT, page), encoding='utf-8').read()
    ids = set(re.findall(r'id="([\w-]+)"', html))
    for sc in scripts:
        p = os.path.join(ROOT, sc)
        if not os.path.exists(p):
            print(f'[{page}] 缺少脚本 {sc}')
            ok = False
            continue
        js = open(p, encoding='utf-8').read()
        refs = set(re.findall(r'getElementById\("([\w-]+)"\)', js))
        refs |= set(re.findall(r'querySelector\("#([\w-]+)', js))
        missing = refs - ids
        if missing:
            print(f'[{page} + {sc}] 引用了不存在的元素: {sorted(missing)}')
            ok = False
if ok:
    print('全部通过：所有 JS 引用的元素均存在于对应页面')