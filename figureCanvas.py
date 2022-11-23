# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
#matplotlib.use('QtAgg')  #指定渲染后端。QtAgg后端指用Agg二维图形库在Qt控件上绘图。
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
#使用matplotlib中的FigureCanvas(继承自QtWidgets.QWidget)绘制图形可以嵌入QT GUI
import mplfinance as mpf
import pandas as pd
import time

title_font = {'fontname': 'SimHei',
              'size':     '16',
              'color':    'black',
              'weight':   'bold',
              'va':       'bottom',
              'ha':       'center'}
large_red_font = {'fontname': 'Arial',
          'size':     '24',
          'color':    'red',
          'weight':   'bold',
          'va':       'bottom'}
# 绿色数字格式（显示开盘收盘价）粗体绿色24号字
large_green_font = {'fontname': 'Arial',
            'size':     '24',
            'color':    'green',
            'weight':   'bold',
            'va':       'bottom'}
# 小数字格式（显示其他价格信息）粗体红色12号字
small_red_font = {'fontname': 'Arial',
          'size':     '12',
          'color':    'red',
          'weight':   'bold',
          'va':       'bottom'}
# 小数字格式（显示其他价格信息）粗体绿色12号字
small_green_font = {'fontname': 'Arial',
            'size':     '12',
            'color':    'green',
            'weight':   'bold',
            'va':       'bottom'}
# 标签格式，可以显示中文，普通黑色12号字
normal_label_font = {'fontname': 'SimHei',
             'size':     '12',
             'color':    'black',
             'va':       'bottom',
             'ha':       'right'}
# 普通文本格式，普通黑色12号字
normal_font = {'fontname': 'Arial',
       'size':     '12',
       'color':    'black',
       'va':       'bottom',
       'ha':       'left'}

class Figure_Canvas(FigureCanvas):
    def __init__(self,code,freq,data,name,industry,parent=None,width=17,height=9.7,dpi=100):
        my_color=mpf.make_marketcolors(up='r',
                                       down='g',
                                       edge='inherit',
                                       wick='inherit',
                                       volume='inherit'
                                       )
        my_style=mpf.make_mpf_style(base_mpf_style='blueskies',
                                    #marketcolors=my_color,
                                    figcolor='(0.82, 0.83, 0.85)',
                                  gridcolor='(0.82, 0.83, 0.85)')
        self.style=my_style
        self.fig=mpf.figure(style=my_style,figsize=(width,height),facecolor=(0.82, 0.83, 0.85))
        fig=self.fig

        #显示鼠标位置信息

        # 添加三个图表，四个数字分别代表图表左下角在figure中的坐标，以及图表的宽（0.88）、高（0.60）
        self.ax1 = fig.add_axes([0.06, 0.25, 0.88, 0.60])
        #添加第二、三张图表时，使用sharex关键字指明与ax1在x轴上对齐，且共用x轴
        self.ax2 = fig.add_axes([0.06, 0.15, 0.88, 0.10], sharex=self.ax1)
        self.ax3 = fig.add_axes([0.06, 0.05, 0.88, 0.10], sharex=self.ax1)
        # 设置三张图表的Y轴标签
        #self.ax1.set_ylabel('Price')
        #self.ax2.set_ylabel('Volume')

        FigureCanvas.__init__(self,fig)
        self.setParent(parent)
        self.Title=self.fig.text(0.50, 0.94, code,title_font)

        self.init(code,freq,data,name,industry)
        self.detailed_data()
        fig.text(0.12, 0.90, '开/收: ', normal_label_font)
        fig.text(0.40, 0.90, '涨幅: ', normal_label_font)
        fig.text(0.40, 0.86, '换手: ', normal_label_font)
        fig.text(0.55, 0.90, '高: ', normal_label_font)
        fig.text(0.55, 0.86, '低：', normal_label_font)
        fig.text(0.70, 0.90, '量(万股): ', normal_label_font)
        fig.text(0.70, 0.86, '额(千万元): ', normal_label_font)
        fig.text(0.85, 0.90, 'PE(滚): ', normal_label_font)
        fig.text(0.85, 0.86, '前收: ', normal_label_font)
        self.Title.set_text(self.stock_code+' '+self.name+'('+self.interval+')'+self.industry)

        #fig.canvas.mpl_connect('button_press_event',self.on_press)
        #fig.canvas.mpl_connect('button_release_event',self.on_release)
        fig.canvas.mpl_connect('motion_notify_event',self.on_motion)
        #fig.canvas.mpl_connect('scroll_event',self.on_scroll)
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def init(self,code,freq,data,name,industry):
        self.freq=freq
        self.stock_code=code

        self.data=data
        self.deal_with_data_candle()
        self.name=name
        self.industry=industry
        self.idx_start=len(self.data_candle)
        self.curInformation=len(self.data_candle)-1
        self.idx_range=120
        if self.idx_start<self.idx_range:
            self.idx_range=self.idx_start

        self.pressed = False
        # 鼠标按下时的x坐标
        self.xpress = None

        if self.freq in ['5', '15', '30','60']:
            self.interval=self.freq+'分钟均线'
        else:

            if self.freq=='daily':
                self.interval='日线'
            if self.freq=='weekly':
                self.interval='周线'
            if self.freq=='monthly':
                self.interval='月线'
        self.Title.set_text(self.stock_code+' '+self.name+'('+self.interval+')'+self.industry)

    def deal_with_data_candle(self):
        self.data_candle=self.data[['date','open','high','low','close','volume']]
        self.data_candle.set_index('date',inplace=True)
        self.data_candle = self.data_candle.rename(index=pd.Timestamp)
        #data_price['date']=data_price['date'].apply(lambda x:mdates.date2num(datetime.datetime.strptime(x,'%Y-%m-%d')))
        #self.data_candle = self.data_candle.astype(float)
        self.data_candle['open']=pd.to_numeric(self.data_candle['open'],errors='ignore')
        self.data_candle['high']=pd.to_numeric(self.data_candle['high'],errors='ignore')
        self.data_candle['low']=pd.to_numeric(self.data_candle['low'],errors='ignore')
        self.data_candle['close']=pd.to_numeric(self.data_candle['close'],errors='ignore')
        self.data_candle['volume']=pd.to_numeric(self.data_candle['volume'],errors='ignore')

    def detailed_data(self):
        a=self.data.loc[self.curInformation]
        a=a.apply(pd.to_numeric,errors='ignore')
        if self.freq in ['5','15','30','60']:
            a['date'] = pd.to_datetime(a['date'])

        if a[1]<=a[2]:
            self.tOpen=self.fig.text(0.14,0.89,f'{a[1]}/{a[2]}',large_red_font)
        else:
            self.tOpen=self.fig.text(0.14,0.89,f'{a[1]}/{a[2]}',large_green_font)
        self.tTime=self.fig.text(0.14, 0.86,a[0],**normal_label_font)
        if a[8]>=0:
            self.tGain=self.fig.text(0.40,0.90,'%s%%'%(a[8]),small_red_font)
        else:
            self.tGain=self.fig.text(0.40,0.90,'%s%%'%(a[8]),small_green_font)
        self.tHigh=self.fig.text(0.55,0.90,a[3],small_red_font)
        self.tLow=self.fig.text(0.55,0.86,a[4],small_green_font)
        self.tVolume=self.fig.text(0.70,0.90,a[5]/10000,normal_font)
        self.tPreclose=self.fig.text(0.85,0.86,(a[2]/(1+a[8]/100)).round(2),normal_font)
        self.tAmount=self.fig.text(0.70,0.86,(a[6]/10000000).round(4),normal_font)

        self.tTurn=self.fig.text(0.40,0.86,'%s%%'%(a[10]),normal_font)

    def refrash_detailed_data(self,curInformation):
        a=self.data.loc[curInformation]
        a=a.apply(pd.to_numeric,errors='ignore')

        if self.freq in ['5','15','30','60']:
            a['date'] = pd.to_datetime(a['date'])
        self.Title.set_text(self.stock_code+' '+self.name+'('+self.interval+')'+self.industry)
        self.tOpen.set_text(f'{a[1]}/{a[2]}')
        if a[1]<=a[2]:
            self.tOpen.set_color('r')
        else:
            self.tOpen.set_color('g')
        self.tGain.set_text('%s%%'%(a[8]))
        if a[8]>=0:
            self.tGain.set_color('r')
        else:
            self.tGain.set_color('g')

        self.tTime.set_text(a[0])
        self.tHigh.set_text(a[3].round(2))
        self.tLow.set_text(a[4].round(2))
        self.tVolume.set_text(a[5]/10000)
        self.tAmount.set_text((a[6]/10000000).round(4))
        self.tPreclose.set_text((a[2]/(1+a[8]/100)).round(2))
        self.tTurn.set_text('%s%%'%(a[10]))

    def on_key_press(self,event):
        scale_factor=1.0
        if event.key == 'up':
            scale_factor=0.8
        if event.key=='down':
            scale_factor=1.2
        if event.key=='left':
            new_start=self.idx_start-self.idx_range//4
            if new_start <= self.idx_range:
               new_start = self.idx_range
            self.idx_start=new_start
        if event.key=='right':
            new_start=self.idx_start+self.idx_range//4
            if new_start >= len(self.data_candle):
               new_start = len(self.data_candle)
            self.idx_start=new_start
        self.idx_range=int(self.idx_range*scale_factor)
        if self.idx_range>=self.idx_start:
            self.idx_range=self.idx_start
        if self.idx_range<=100:
            self.idx_range=100
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.refrash_plot()
        self.fig.canvas.draw()

    def on_scroll(self,event):
        if event.inaxes!=self.ax1:
            return

    def on_press(self,event):
        if not event.inaxes==self.ax1:
            return
        if event.button!=1:
            return
        self.pressed=True
        self.xpress=event.xdata

    def on_release(self,event):
        self.pressed=False
        #dx=int(event.xdata-self.xpress)
        #self.idx_start-=dx
        if self.idx_start <= self.idx_range:
            self.idx_start = self.idx_range
        if self.idx_start >= len(self.data_candle):
            self.idx_start = len(self.data_candle)

    def on_motion(self,event):
        if event.inaxes!=self.ax1:
            #if(event.inaxes!=self.ax2):
                #if(event.inaxes!=self.ax3):
                    return
        if not self.pressed:
            x=event.xdata
            time.sleep(0.2)
            if event.xdata==x:
                self.curInformation=self.idx_start-(self.idx_range-int(event.xdata+0.5))
                self.refrash_detailed_data(self.curInformation)
                self.fig.canvas.draw_idle()
            return

    def refrash_plot(self):
        all_data=self.data_candle
        all_data['MA5'] = all_data['close'].rolling(window=5).mean()
        all_data['MA10'] = all_data['close'].rolling(window=10).mean()
        all_data['MA20'] = all_data['close'].rolling(window=20).mean()
        all_data['MA60'] = all_data['close'].rolling(window=60).mean()

        plot_data=all_data.iloc[self.idx_start-self.idx_range:self.idx_start]
        #计算移动平均线
        #talib计算macd
        #import talib
        #plot_data['MACD'],plot_data['MACDsignal'],plot_data['MACDhist'] = talib.MACD(plot_data.Close, fastperiod=12, slowperiod=26, signalperiod=9)
        #计算macd的方式
        exp12 = plot_data['close'].ewm(span=12, adjust=False).mean()
        exp26 = plot_data['close'].ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        histogram[histogram < 0] = None
        histogram_positive = histogram
        histogram = macd - signal
        histogram[histogram >= 0] = None
        histogram_negative = histogram

        # 添加子图
        add_plot = [
            mpf.make_addplot(plot_data[['MA5','MA10','MA20','MA60']], ax=self.ax1),

            mpf.make_addplot(histogram_positive, type='bar', color='red',ax=self.ax3),
            mpf.make_addplot(histogram_negative, type='bar', color='green',ax=self.ax3),
            mpf.make_addplot(macd, ax=self.ax3),
            mpf.make_addplot(signal, ax=self.ax3)
            ]
        self.ax3.set_ylabel('Macd')
        mpf.plot(plot_data,
                 ax=self.ax1,
                 type='candle',
                 addplot=add_plot,
                 ylabel='Price', ylabel_lower='Volume',
                 volume=self.ax2,
                 style=self.style,
                 datetime_format='%Y-%m-%d',
                 tight_layout=True,
                 #mav=(5,10,20,60)
                 )
