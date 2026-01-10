#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
依照 海豚 Spider 的輸出規則：
#genre#分類
頻道名,播放URL

轉成 IPTV 標準 M3U(list.txt)
"""

from 海豚 import Spider


class M3UBuilder:

    def __init__(self):
        self.spider = Spider()

    def build(self):
        raw = self.spider.liveContent('')
        lines = raw.splitlines()

        m3u_lines = []
        m3u_lines.append('#EXTM3U')

        group = '未分類'

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 分類行
            if line.startswith('#genre#'):
                group = line.replace('#genre#', '').strip()
                continue

            # 頻道行
            if ',' not in line:
                continue

            name, url = line.split(',', 1)

            m3u_lines.append(
                f'#EXTINF:-1 tvg-name="{name}" group-title="{group}",{name}'
            )
            m3u_lines.append(url)

        return '\n'.join(m3u_lines)

    def save(self, filename='list.txt'):
        content = self.build()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ {filename} 產生完成')


if __name__ == '__main__':
    M3UBuilder().save()
