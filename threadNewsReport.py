# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtCore import Signal, QThread
# import pyttsx3
# from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
# from PySide6.QtCore import QUrl
# from PySide6.QtGui import QColor,QTextCursor
# import akshare as ak
from memory_profiler import profile

import json
import requests
import datetime, time
# import pyttsx3
import re
import win32com.client as win
from lxml import etree
import operator

class NewsReport(QThread):
    _signal = Signal()

    def __init__(self, parent):
        super(NewsReport, self).__init__()
        self.parent = parent
        recent_time = datetime.datetime.now() + datetime.timedelta(hours=-1)
        self.id = datetime.datetime.strftime(recent_time, "%Y%m%d%H%M%S000000")
        self.time = self.parent.eastNewsReportCurTime
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        self.url = 'https://www.jin10.com/flash_newest.js?t=1667528593473'
        self.url2 = 'https://finance.eastmoney.com/yaowen.html'
        self.is_str = ['金十图示', '金十出品', '点击大图', '点击查看', '点击观看', '点击马上观看', '立即查看',\
                       '马上观看', '立即开通', '点击阅读全文', '马上参与', '金十期货图示', '点击报名', '<a']
        self.count = 0
        self.num = 3
        self.east_data = {'time': ''}
        #        self.file = QUrl.fromLocalFile('e:/cjh/Documents/pyqt/baoStock/key.wav') # 音频文件路径
        #        self.player = QMediaPlayer()
        #        self.player.setSource(self.file)
        #        self.audioOutput = QAudioOutput() # 不能实例化为临时变量，否则被自动回收导致无法播放
        #        self.player.setAudioOutput(self.audioOutput)
        #        self.audioOutput.setVolume(50)

        #        self.engine = pyttsx3.init() #初始化语音引擎
        #        voices = self.engine.getProperty('voices')
        #        for voice in voices:
        #            if voice.name[0:16]=='Microsoft Huihui':
        #                self.engine.setProperty('voice',voice.id)       #设置语音合成器
        #                break
        #        self.engine.setProperty('rate', 180)   #设置语速
        #        self.engine.setProperty('volume',0.6)  #设置音量
        self.speak = win.Dispatch("SAPI.SpVoice")
        for Voice in self.speak.GetVoices():
            if 'Microsoft Huihui' in Voice.GetDescription():
                self.speak.Voice = Voice
                break
        self.speak.Volume = 60
        self.speak.rate = 2
        self.speak.Speak("", 0)

    def __del__(self):
        self.wait()
    #@profile
    def get_news_data(self):
        data = requests.get(url=self.url, headers=self.headers).text
        self.js_news_df = json.loads(data[data.find('[{'):-1])
        if self.num == 3:
            dd = requests.get(url=self.url2, headers=self.headers).content.decode()
            html = etree.HTML(dd)
            titles = html.xpath('//*[@class="artitleList2"]/ul/li/div[2]/p/a')
            times = html.xpath('//*[@class="time"]//text()')
            df = []
            day = str(datetime.date.today().day)
            for n, i in enumerate(titles):
                s = str(times[n])
                s_ = re.findall(r'[\u4e00-\u9fa5](.*?)[\u4e00-\u9fa5]', s)[0]
                if day == s_:
                    dd = {'time': s, 'title': str(i.xpath('.//text()')[0]), 'href': str(i.xpath('./@href')[0])}
                    df.append(dd)
            self.east_data = sorted(df, key=operator.itemgetter('time'), reverse=True)
            self.num = 0
        self.num += 1

    def is_report_js_news(self):
        if self.new_id <= self.id:
            return
        if 'content' in self.js_news_df[self.js_count]['data']:
            news_data = self.js_news_df[self.js_count]['data']['content']
        else:
            return
        if any(s in news_data for s in self.is_str) or news_data == '' or news_data == '-':
            return
        t = self.js_news_df[self.js_count]['time'][0:19]
        utc_date2 = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S")
        local_date = utc_date2 + datetime.timedelta(hours=8)
        self.parent.text1 = datetime.datetime.strftime(local_date, "%Y-%m-%d %H:%M:%S")
        if self.parent.text1 <= self.parent.jinShiNewsReportCurTime:
            return
        self.parent.text = f'<span> {news_data} </span>'
        self._signal.emit()
        news_data = re.sub(r'<(.*?)>', '', news_data)
        time.sleep(0.1)
        if self.parent.isOpenNewsReport:
            #                self.engine.say(news_data)
            #                self.engine.runAndWait()
            #                self.engine.stop()
            self.speak.Speak(news_data)
        self.id = self.new_id
        self.parent.jinShiNewsReportCurTime = self.parent.text1
        self.parent.settings.setValue("General/jinShiNewsReportCurTime", self.parent.jinShiNewsReportCurTime)

    def is_report_east_news(self):
        if int(self.time) >= int(self.new_time):
            return
        news_data = self.east_data[self.east_count]['title']
        self.parent.text1 = self.east_data[self.east_count]['time']
        self.parent.text = f'''<span> <a href="{self.east_data[self.east_count]['href']}">{news_data}</a> </span>'''
        self._signal.emit()
        time.sleep(0.1)
        if self.parent.isOpenNewsReport:
            #                self.engine.say(news_data)
            #                self.engine.runAndWait()
            #                self.engine.stop()
            self.speak.Speak(f"东方财经:{news_data}")
        self.time = self.new_time
        self.parent.settings.setValue("General/eastNewsReportCurTime", self.new_time)

    def deal_news_data(self):
        cur_time = str(datetime.datetime.now())[14:16]
        if cur_time <= '01':
            if self.count < 3:
                self.speak.Speak('休息时间,起来锻炼了！')
                # self.engine.say('休息时间,起来锻炼了！')
                self.count += 1
        #                self.engine.runAndWait()
        #                self.engine.stop()
        elif '20' <= cur_time <= '21' or '40' <= cur_time <= '41':
            if self.count < 3:
                self.speak.Speak('转转头,伸个懒腰')
                # self.engine.say('转转头,伸个懒腰')
                self.count += 1
        #                self.engine.runAndWait()
        #                self.engine.stop()
        else:
            self.count = 0
        self.get_news_data()
        # self.js_news_df = ak.js_news(timestamp=datetime.datetime.now())
        # cur_time=str(datetime.datetime.now())[11:16]
        self.js_count = len(self.js_news_df) - 1
        self.east_count = len(self.east_data) - 1
        while self.js_count != -1 or self.east_count != -1:
            if self.js_count != -1:
                self.new_id = self.js_news_df[self.js_count]['id']
                self.time1 = int(self.new_id[4:12])
            else:
                self.time1 = 123456789
            if self.east_count != -1:
                a=re.findall(r'\d+',self.east_data[self.east_count]['time'])
                self.time2 = self.new_time =''.join(i for i in a)
            else:
                self.time2 = 123456789
            if self.time1 <= int(self.time2):
                if self.js_count != -1:
                    self.is_report_js_news()
                    self.js_count -= 1
            else:
                if self.east_count != -1:
                    self.is_report_east_news()
                    self.east_count -= 1

    def run(self):
        self.deal_news_data()
        self.parent.isNewsReportStop = True
