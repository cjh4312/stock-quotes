# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
from PySide6.QtCore import Signal,QThread
#import pyttsx3
#from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
#from PySide6.QtCore import QUrl
#from PySide6.QtGui import QColor,QTextCursor
#import akshare as ak
import json
import requests
import datetime,time
import pyttsx3
#import win32com.client as win

class NewsReport(QThread):
    _signal = Signal()

    def __init__(self,parent):
        super(NewsReport, self).__init__()
        self.parent=parent
        recent_time=datetime.datetime.now()+datetime.timedelta(minutes=-3)
        self.id=datetime.datetime.strftime(recent_time,"%Y%m%d%H%M%S000000")
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
        self.url='https://www.jin10.com/flash_newest.js?t=1667528593473'
        self.is_str=['金十图示','金十出品','点击大图','点击查看','点击观看','立即查看','<a']
        self.count=0
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
        self.engine.setProperty('rate', 180)   #设置语速
        self.engine.setProperty('volume',0.6)  #设置音量
#        self.speak = win.Dispatch("SAPI.SpVoice")
#        for Voice in self.speak.GetVoices():
#            if 'Microsoft Huihui' in Voice.GetDescription():
#                self.speak.Voice = Voice
#                break
#        self.speak.Volume=60
#        self.speak.rate=2
#        self.speak.Speak("",0)

    def __del__(self):
        self.wait()

    def get_news_data(self):
        data=requests.get(url=self.url,headers=self.headers).text
        self.js_news_df=json.loads(data[data.find('[{'):-1])

    def deal_news_data(self):
        cur_time=str(datetime.datetime.now())[14:16]
        if cur_time<='01':
            if self.count<3 and self.parent.isOpenNewsReport:
                self.engine.say('休息时间,起来锻炼了！')
                self.count+=1
                self.engine.runAndWait()
                self.engine.stop()
        elif '20'<=cur_time<='21' or '40'<=cur_time<='41':
            if self.count<3 and self.parent.isOpenNewsReport:
                self.engine.say('转转头,伸个懒腰')
                self.count+=1
                self.engine.runAndWait()
                self.engine.stop()
        else:
            self.count=0
        self.get_news_data()
        #self.js_news_df = ak.js_news(timestamp=datetime.datetime.now())
        #cur_time=str(datetime.datetime.now())[11:16]
        for i in range(10,-1,-1):
            id=self.js_news_df[i]['id']
            if id<=self.id:
                continue
            if 'content' in self.js_news_df[i]['data']:
                news_data=self.js_news_df[i]['data']['content']
            else:
                continue
            if any(s in news_data for s in self.is_str) or news_data=='' or news_data=='-':
                continue
            t = self.js_news_df[i]['time'][0:19]
            utc_date2=datetime.datetime.strptime(t,"%Y-%m-%dT%H:%M:%S")
            local_date=utc_date2+datetime.timedelta(hours=8)
            self.parent.text1=datetime.datetime.strftime(local_date,"%Y-%m-%d %H:%M:%S")
            self.id=id
            self.parent.text=news_data
            self._signal.emit()
            time.sleep(0.1)
            if self.parent.isOpenNewsReport:
                self.engine.say(news_data)
                self.engine.runAndWait()
                self.engine.stop()
#                self.speak.Speak(news_data)

    def run(self):
        self.deal_news_data()
        self.parent.isNewsReportStop=True
