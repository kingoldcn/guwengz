#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析封面右下角残留像素形态：稀疏小簇=水印字迹残留；大片实心=真实内容"""
import sys, os, numpy as np, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r'C:\Users\royli\.agents\skills\sensenova-u1-image\scripts')
from remove_watermark import find_watermark_bbox
from PIL import Image

D = r'D:\古文观止\assets\covers'

def neutral_mask(arr):
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    lum = (r + g + b) / 3.0
    neutral = (np.abs(r - g) <= 30) & (np.abs(g - b) <= 30) & (np.abs(r - b) <= 30)
    return neutral & (lum >= 150)

def analyze(aid):
    arr = np.array(Image.open(os.path.join(D, aid + '.png')).convert('RGB')).astype(np.int32)
    b = find_watermark_bbox(arr)
    print(f'=== {aid} 检测bbox={b}')
    if not b:
        return
    x0, y0, x1, y1 = b
    sub = arr[y0:y1, x0:x1]
    mask = neutral_mask(sub)
    total = mask.sum()
    h, w = mask.shape
    print(f'  区域 {w}x{h}, 中性亮像素 {total} 个 ({total*100.0/(w*h):.1f}%)')
    # 分析簇结构
    visited = np.zeros_like(mask, dtype=bool)
    comps = []
    for y in range(h):
        for x in range(w):
            if mask[y, x] and not visited[y, x]:
                stack = [(y, x)]
                visited[y, x] = True
                px = []
                while stack:
                    cy, cx = stack.pop()
                    px.append((cx, cy))
                    for dy, dx in ((-1,0),(1,0),(0,-1),(0,1)):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))
                if len(px) > 3:
                    xs = [p[0] for p in px]; ys = [p[1] for p in px]
                    comps.append((len(px), max(xs)-min(xs)+1, max(ys)-min(ys)+1))
    comps.sort(reverse=True)
    print(f'  连通簇(>3px) {len(comps)} 个，前10: {comps[:10]}')
    big = [c for c in comps if c[1] > 30 and c[2] > 30]
    if big:
        print(f'  有 {len(big)} 个大块(>30x30)，可能为真实内容: {big[:5]}')
    else:
        print('  全部为小块，符合文字笔画特征（水印残留）')

for aid in ['v01-006', 'v01-009', 'v01-010', 'v01-013', 'v01-014']:
    analyze(aid)