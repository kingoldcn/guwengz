#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = open(r'C:\Users\royli\AppData\Local\Temp\opencode\v01002_dom.html', encoding='utf-8').read()
print('封面图引用:', bool(re.search(r'assets/covers/v01-002\.png', d)))
m = re.search(r'<title>(.*?)</title>', d)
print('页面标题:', m.group(1) if m else '?')
print('正文句子数:', d.count('class="sent"'))
print('工具按钮btn-py:', bool(re.search(r'id="btn-py"', d)))