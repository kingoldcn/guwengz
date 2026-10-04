#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = open(r'C:\Users\royli\AppData\Local\Temp\opencode\v01002_dom2.html', encoding='utf-8').read()
m = re.search(r'<div class="reader-cover" id="gw-cover" style="([^"]*)">', d)
print('gw-cover style:', m.group(1) if m else '未找到容器')
print('含封面img:', bool(re.search(r'assets/covers/v01-002\.png', d)))