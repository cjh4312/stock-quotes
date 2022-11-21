# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtCore import Signal,QThread
import pyttsx3
#from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
#from PySide6.QtCore import QUrl
#from PySide6.QtGui import QColor,QTextCursor
#import akshare as ak
import json
import re
import requests
import datetime,time

class NewsReport(QThread):
    _signal = Signal()

    def __init__(self,parent):
        super(NewsReport, self).__init__()
        self.parent=parent
        self.recent_leng=0
        self.recent_time=str(datetime.datetime.now()+datetime.timedelta(minutes=-3))[0:19]
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        self.url='https://www.jin10.com/flash_newest.js?t=1667528593473'
#        self.file = QUrl.fromLocalFile('e:/cjh/Documents/pyqt/baoStock/key.wav') # 音频文件路径
#        self.player = QMediaPlayer()
#        self.player.setSource(self.file)
#        self.audioOutput = QAudioOutput() # 不能实例化为临时变量，否则被自动回收导致无法播放
#        self.player.setAudioOutput(self.audioOutput)
#        self.audioOutput.setVolume(50)

        self.engine = pyttsx3.init() #初始化语音引擎
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name[0:16]=='Microsoft Huihui':
                self.engine.setProperty('voice',voice.id)       #设置语音合成器
                break
        self.engine.setProperty('rate', 190)   #设置语速
        self.engine.setProperty('volume',0.5)  #设置音量

    def __del__(self):
        self.wait()

    def get_news_data(self):
        data=requests.get(url=self.url,headers=self.headers).text
        self.js_news_df=json.loads(re.findall('\[{.*}\]', data)[0])

    def deal_news_data(self):
        self.get_news_data()
        #self.js_news_df = ak.js_news(timestamp=datetime.datetime.now())
        #cur_time=str(datetime.datetime.now())[11:16]
        for i in [10,9,8,7,6,5,4,3,2,1,0]:
            t = self.js_news_df[i]['time'][0:19]
            utc_date2=datetime.datetime.strptime(t,"%Y-%m-%dT%H:%M:%S")
            local_date=utc_date2+datetime.timedelta(hours=8)
            local_date=datetime.datetime.strftime(local_date,"%Y-%m-%d %H:%M:%S")
            if local_date<self.recent_time:
                continue
            if 'content' in self.js_news_df[i]['data']:
                news_data=self.js_news_df[i]['data']['content']
            else:
                continue
            l=len(news_data)
            if news_data[1:5]=='金十图示' or news_data=='' or news_data[0:2]=='<a' or news_data=='-' or \
                 news_data[1:5]=='金十出品':
                continue
            if local_date==self.recent_time and l==self.recent_leng:
                continue
            self.recent_leng=l
            self.recent_time=local_date
            self.parent.text1=local_date
            self.parent.text=news_data
            self._signal.emit()
            time.sleep(0.1)
            self.text=news_data
            #self.player.play()
            if self.parent.isOpenNewsReport:
                self.parent.isNewsReportStop=False
                self.engine.say(self.text)
                self.engine.runAndWait()
                self.engine.stop()
                self.parent.isNewsReportStop=True

    def run(self):
        self.deal_news_data()
