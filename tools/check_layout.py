#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = open(r'C:\Users\royli\AppData\Local\Temp\opencode\v02007_dom.html', encoding='utf-8').read()
i = d.find('reader-side')
print('reader-side 结构片段:')
print(d[i:i+150].replace('\n', ' '))
print()
side_start = d.find('class="reader-side"')
tabs_pos = d.find('id="gw-tabs"')
facts_pos = d.find('id="gw-facts"')
nav_pos = d.find('id="gw-nav"')
print('positions: side=%d facts=%d tabs=%d nav=%d' % (side_start, facts_pos, tabs_pos, nav_pos))
print('tabs在side内:', side_start < tabs_pos)
print('nav在tabs之后:', tabs_pos < nav_pos)
# 检查正文句子
print('正文句子数:', d.count('class="sent"'))