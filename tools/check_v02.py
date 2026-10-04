#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = open(r'C:\Users\royli\AppData\Local\Temp\opencode\v02016_dom.html', encoding='utf-8').read()
print('正文句子数:', d.count('class="sent"'))
print('标题渲染:', bool(re.search(r'吴许越成', d)))
print('逐句译文:', bool(re.search(r'译文', d)))
print('赏析导读tab:', bool(re.search(r'赏析导读', d)))
print('注解词条:', d.count('class="note-item"') if 'note-item' in d else 'check-tab')
print('封面img:', bool(re.search(r'assets/covers/v02-016\.png', d)))
print('页面标题:', re.search(r'<title>(.*?)</title>', d).group(1))