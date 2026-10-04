#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""核查封面：新算法检测到的水印像素形态，区分文字残留与真实内容"""
import sys, os, numpy as np, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r'C:\Users\royli\.agents\skills\sensenova-u1-image\scripts')
from remove_watermark import find_watermark, _label_components, _brightness
from PIL import Image

D = r'D:\古文观止\assets\covers'
NEUTRAL_TOL = 30
LUM_MIN = 150

def inspect(aid):
    arr = np.array(Image.open(os.path.join(D, aid + '.png')).convert('RGB')).astype(np.int32)
    mask, bbox = find_watermark(arr)
    h, w = arr.shape[:2]
    print(f'=== {aid} 检测bbox={bbox}')
    if mask is None:
        print('  干净')
        return
    n = int(mask.sum())
    print(f'  文字像素 {n} 个')
    if n < 400:
        print('  数量很少 → 轻微残留或噪点，可忽略')
    # 检查 bbox 内是否有大块中性亮区域（真实内容）
    if bbox:
        x0, y0, x1, y1 = bbox
        sub = arr[y0:y1, x0:x1]
        neutral = (np.abs(sub[...,0]-sub[...,1])<=NEUTRAL_TOL)&(np.abs(sub[...,1]-sub[...,2])<=NEUTRAL_TOL)
        bright = neutral & (_brightness(sub)>=LUM_MIN)
        comps = _label_components(bright)
        big = [c for c in comps if (c['x1']-c['x0']+1)>120 or (c['y1']-c['y0']+1)>90 or c['count']>5000]
        if big:
            print(f'  bbox内还有 {len(big)} 个大块(>120宽或>90高或>5000px): {[(c["count"],c["x1"]-c["x0"]+1,c["y1"]-c["y0"]+1) for c in big[:4]]}')
        else:
            print('  bbox内全部为文字量级簇（安全）')

for aid in ['v01-006','v01-009','v01-010','v01-013','v01-014']:
    inspect(aid)