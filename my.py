#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import requests
import re

sys.path.append('..')
from base.spider import Spider as BaseSpider


# ========= 基礎 Spider =========
class BaseLiveSpider(BaseSpider):
    def __init__(self, name, base_source=None, channel_source=None):
        super().__init__()
        self.name = name
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
        }
        self.base_source = base_source
        self.channel_source = channel_source

    def getName(self):
        return self.name

    def init(self, extend='{}'):
        pass

    def liveContent(self, url):
        tv_list = []
        try:
            if self.channel_source and self.channel_source.endswith('.txt'):
                tv_list = self._live_from_txt()
            elif self.channel_source and self.channel_source.endswith('.php'):
                tv_list = self._live_from_m3u()
            else:
                tv_list = self._live_from_txt()  # 默認處理 TXT
        except Exception as e:
            print(f"[{self.name} Spider Error]", e)

        return '\n'.join(tv_list)

    # ====== TXT 源方法 ======
    def _live_from_txt(self):
        tv_list = []

        base_uri = self._get_base_uri()
        channel_text = self._get_channel_list()

        if not channel_text:
            return []

        for line in channel_text.splitlines():
            line = line.strip()
            if not line:
                continue
            if '#genre#' in line:
                tv_list.append(line)
                continue
            try:
                name, play_url = line.split(',', 1)
                if base_uri:
                    pid = play_url.split('=')[-1]
                    real_url = f'{base_uri}{pid}.ts'
                else:
                    real_url = play_url
                tv_list.append(f'{name},{real_url}')
            except Exception:
                continue

        return tv_list

    # ====== M3U 源方法 ======
    def _live_from_m3u(self):
        tv_list = []
        r = requests.get(self.channel_source, headers=self.headers, timeout=10)
        r.encoding = 'utf-8'
        r.raise_for_status()
        content = r.text

        # 匹配 #EXTINF:-1 tvg-id="..." tvg-name="频道名",频道名\nURL
        matches = re.findall(r'#EXTINF:-1.*?,(.*?)\n(.*)', content)
        for name, url in matches:
            url = url.strip()
            tv_list.append(f'{name},{url}')

        return tv_list

    # ====== 內部方法 ======
    def _get_base_uri(self):
        if not self.base_source:
            return None
        try:
            r = requests.get(self.base_source, headers=self.headers, timeout=10)
            r.raise_for_status()
            for line in r.text.splitlines():
                if 'http' in line:  # 只抓有網址的行
                    url = line.split(',')[1]
                    return url.rsplit('/', 1)[0] + '/'
        except Exception as e:
            print(f"[{self.name} base_uri Error]", e)
        return None

    def _get_channel_list(self):
        if not self.channel_source:
            return None
        try:
            r = requests.get(self.channel_source, headers=self.headers, timeout=10)
            r.encoding = 'utf-8'
            r.raise_for_status()
            return r.text
        except Exception as e:
            print(f"[{self.name} channel_list Error]", e)
            return None


# ========= 海豚源 =========
class DolphinSpider(BaseLiveSpider):
    def __init__(self):
        super().__init__(
            name='海豚',
            base_source='https://raw.githubusercontent.com/FGBLH/FG/refs/heads/main/港台大陆频道',
            channel_source='http://kenneth001.serv00.net/IPTVpro源.txt'
        )


# ========= 企鵝源 (M3U Plus) =========
class PenguinSpider(BaseLiveSpider):
    def __init__(self):
        super().__init__(
            name='企鵝',
            channel_source='https://iptv.mydiver.eu.org/get.php?username=tg_ueiw02xw&password=wcytxrwpblzi&type=m3u_plus'
        )


# ========= 小鯨魚源 =========
class WhaleSpider(BaseLiveSpider):
    def __init__(self):
        super().__init__(
            name='小鯨魚',
            base_source='https://raw.githubusercontent.com/FGBLH/FG/refs/heads/main/%E5%88%AB%E4%BA%BA%E6%94%B6%E8%B4%B9%E6%BA%90',
            channel_source='https://raw.githubusercontent.com/FGBLH/FG/refs/heads/main/%E5%88%AB%E4%BA%BA%E6%94%B6%E8%B4%B9%E6%BA%90'
        )


# ========= 測試 =========
if __name__ == '__main__':
    spiders = [DolphinSpider(), PenguinSpider(), WhaleSpider()]
    for sp in spiders:
        print(f"--- {sp.getName()} ---")
        print(sp.liveContent(''))
        print("\n")
