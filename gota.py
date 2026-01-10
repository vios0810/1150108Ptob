#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
gota.py
用途：
- 修正 GitHub Actions / Linux 環境下的 import 路徑問題
- 呼叫 海豚 Spider
- 產生 IPTV 所需資料（例如 list.txt）
"""

import os
import sys

# === 關鍵：把專案根目錄加入 Python 搜尋路徑 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# === 現在這些 import 在 GitHub Actions 會 100% 成功 ===
from 海豚 import Spider


def main():
    sp = Spider()

    # 取得 Spider 原始輸出（#genre# + name,url）
    raw = sp.liveContent('')

    # 轉成 M3U(list.txt)
    lines = raw.splitlines()
    m3u = []
    m3u.append('#EXTM3U')

    group = '未分類'

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('#genre#'):
            group = line.replace('#genre#', '').strip()
            continue

        if ',' not in line:
            continue

        name, url = line.split(',', 1)

        m3u.append(
            f'#EXTINF:-1 tvg-name="{name}" group-title="{group}",{name}'
        )
        m3u.append(url)

    # 輸出 list.txt（給 IPTV / TVBox 用）
    out_file = os.path.join(BASE_DIR, 'list.txt')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(m3u))

    print('✅ list.txt generated')


if __name__ == '__main__':
    main()
