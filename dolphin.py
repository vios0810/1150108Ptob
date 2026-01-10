#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2026/1/4
# @file    : dolphin_m3u_group.py

import sys
import requests
sys.path.append('..')
from base.spider import Spider as BaseSpider


class Spider(BaseSpider):
    def __init__(self):
        super(Spider, self).__init__()
        self.name = 'dolphin'
        self.url = ''
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        }
        self.ck = None

    def getName(self):
        return self.name

    def init(self, extend='{}'):
        pass

    def liveContent(self, url):
        tv_list = ['#EXTM3U']  # M3U 開頭
        try:
            # 取得 base URI
            response = requests.get(
                'https://raw.githubusercontent.com/FGBLH/FG/refs/heads/main/港台大陆频道',
                headers=self.headers
            )
            uri = None
            for line in response.text.strip().splitlines():
                if 'http://iptvpro.pw:35451' in line:
                    uri = line.split(',')[1].rsplit('/', 1)[0] + '/'
                    break

            if uri:
                response2 = requests.get('http://kenneth001.serv00.net/IPTVpro源.txt', headers=self.headers)
                response2.encoding = 'utf-8'

                current_genre = "其他"  # 預設分類
                for line in response2.text.strip().splitlines():
                    line = line.strip()
                    if not line:
                        continue

                    if '#genre#' in line:
                        # 解析分類名稱，例如 "#genre#港台" -> "港台"
                        current_genre = line.replace('#genre#', '').strip()
                    else:
                        info = line.split(',')
                        if len(info) < 2:
                            continue
                        name = info[0].strip()
                        pid = info[1].split('=')[-1].strip()
                        ts_url = f'{uri}{pid}.ts'
                        # 組裝 M3U 格式，帶 group-title
                        tv_list.append(f'#EXTINF:-1 tvg-name="{name}" group-title="{current_genre}",{name}')
                        tv_list.append(ts_url)

        except Exception as e:
            print("抓取出錯:", e)

        return '\n'.join(tv_list)

    def init_ck(self):
        try:
            response = requests.get(self.url, headers=self.headers, allow_redirects=False)
            ck = response.headers.get('Set-Cookie')
            if ck:
                self.ck = ck
        except Exception as e:
            print(e)
        return False


if __name__ == '__main__':
    sp = Spider()
    sp.init()
    m3u_content = sp.liveContent('')
    # 寫入檔案
    with open('dolphin_group.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_content)
    print("已生成 dolphin_group.m3u（自動分類版）")
