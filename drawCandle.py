# This Python file uses the following encoding: utf-8

import pyqtgraph as pg
from PySide6.QtWidgets import QWidget,QLabel
from PySide6.QtGui import QColor,QPicture,QPainter
from PySide6.QtCore import Signal,QPointF,QRectF
import pandas as pd
import datetime

class DrawChart(QWidget):
    _signal=Signal()
    def __init__(self, data):
        super(DrawChart, self).__init__()
        self.baseheight=745
        self.baseWidth=1465
        self.data=data
        self.idx_range=150
        self.idx_start=len(data)
        self.x_max=self.idx_start
        self.y_len=4
        if self.idx_start<self.idx_range:
            self.idx_range=self.idx_start

#        self.xdict = {self.idx_start-self.idx_range: str(data['date'][self.idx_start-self.idx_range])[0:10].replace('-', '/'),
#                    self.idx_start -self.idx_range//4 : str(data['date'][self.idx_start -self.idx_range//4])[0:10].replace('-', '/'),
#                    self.idx_start -self.idx_range//2 : str(data['date'][self.idx_start -self.idx_range//2])[0:10].replace('-', '/'),
#                    self.idx_start -3*self.idx_range//4 : str(data['date'][self.idx_start -3*self.idx_range//4])[0:10].replace('-', '/'),
#                    self.idx_start - 1: str(data['date'][self.idx_start - 1])[0:10].replace('-', '/')}
#        self.stringaxis = pg.AxisItem(orientation='bottom')
#        self.stringaxis.setTicks([self.xdict.items()])
        self.candle_widget=QWidget()
#        self.stringaxis2 = pg.AxisItem(orientation='bottom')
#        self.stringaxis2.setTicks([self.xdict.items()])

        self.candle_plot = pg.PlotWidget(parent=self.candle_widget)
        self.candle_plot.setGeometry(0,0,self.baseWidth,self.baseheight)
        self.volume_plot= pg.PlotWidget(parent=self.candle_widget)
        self.volume_plot.setGeometry(0,self.baseheight+1,self.baseWidth,200)

        #self.candle_plot = pg.PlotWidget(axisItems={'bottom': self.stringaxis},background=QColor(219,241,255),enableMenu=False)
        self.candle_plot.showAxis('bottom', False)
        self.candle_plot.showAxis('left', False)
        #self.volume_plot= pg.PlotWidget(axisItems={'bottom': self.stringaxis2},background=QColor(219,241,255),enableMenu=False)
        self.volume_plot.showAxis('bottom', False)
        self.volume_plot.showAxis('left', False)

#        self.label_widget=QWidget()
#        self.candle_layout=QVBoxLayout()
#        self.label_layout=QGridLayout()
#        self.candle_widget.setLayout(self.candle_layout)
#        self.label_widget.setLayout(self.label_layout)
#        self.candle_layout.addWidget(self.label_widget)
#        self.candle_layout.addWidget(self.candle_plot)
#        self.candle_layout.addWidget(self.volume_plot)

        self.ylabel=QLabel(parent=self.candle_widget)
        self.xlabel=QLabel(parent=self.candle_widget)
        self.ylabel.setGeometry(-100,0,85,25)
        self.xlabel.setGeometry(-100,self.baseheight,90,25)
        self.ylabel.setStyleSheet("color:yellow;font:bold")
        self.xlabel.setStyleSheet("color:yellow;font:bold;font-size:14px")
        self.max_label=QLabel(parent=self.candle_widget)
        self.max_label.setStyleSheet("color:red;font:bold")
        self.min_label=QLabel(parent=self.candle_widget)
        self.min_label.setStyleSheet("color:green;font:bold")
        self.max_label.setGeometry(-100,0,85,25)
        self.min_label.setGeometry(-100,0,85,25)

        self.candle_plot.showGrid(x=False, y=True)
        self.volume_plot.showGrid(x=False, y=True)
        self.candle_plot.setMouseEnabled(x=False, y=False)
        self.volume_plot.setMouseEnabled(x=False, y=False)
        self.candle_plot.setXRange(self.idx_start-self.idx_range-1, self.idx_start, padding=0)
        self.volume_plot.setXRange(self.idx_start-self.idx_range-1, self.idx_start, padding=0)

        self.candle_item = CandleItem(self.data,self.idx_range,self.idx_start)
        self.vol_item=VolItem(self.data,self.idx_range,self.idx_start)
        self.candle_plot.addItem(self.candle_item)
        self.volume_plot.addItem(self.vol_item)

        #pen = pg.mkPen('w', width=1)

        #self.line_plt=pg.PlotWidget(parent=self.candle_widget)
        #self.line_plt.setGeometry(-100,self.baseheight,self.baseWidth+100,2)
        #self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pen)  # 创建垂直线
#        self.hline = pg.InfiniteLine(angle=0, movable=False, pen=pen)  # 创建水平线
#        #self.vline.setPos(0)
#        self.hline.setPos(0)
#        #self.line_plt.addItem(self.vline, ignoreBounds=True)
#        self.line_plt.addItem(self.hline, ignoreBounds=True)
        self.proxy = pg.SignalProxy(self.candle_plot.scene().sigMouseMoved, rateLimit=100,slot=self.mouseMoved)

    def init_idx(self,data):
        #self.idx_range=150
        self.idx_start=len(data)
        self.x_max=self.idx_start
        pre_range=120
        if self.idx_range>=pre_range:
            pre_range=self.idx_range
        if self.idx_start<pre_range:
            self.idx_range=self.idx_start
            #pre_range=150
            self.x_max=pre_range
        else:

            self.idx_range=pre_range
#            if self.idx_start<50:
#                self.x_max=50
        self.init(data)

    def init(self,data):
#        xdict={}

#        l=self.idx_start-self.idx_range
#        if self.idx_start!=self.idx_range:
#            for i in range(l,self.idx_start):
#                if i in [l,l+self.idx_range//6,l+self.idx_range*2//6,l+self.idx_range*3//6,\
#                        l+self.idx_range*4//6,l+self.idx_range*5//6,self.idx_range]:
#                    xdict[i]= data['date'][i]

#            stringaxis = pg.AxisItem(orientation='bottom')
#            stringaxis.setTicks([xdict.items()])
#            self.volume_plot.setAxisItems(axisItems={'bottom':stringaxis})
        self.data=data
        self.candle_plot.removeItem(self.candle_item)
        self.volume_plot.removeItem(self.vol_item)

#        self.xdict = {self.idx_start-self.idx_range: str(data['date'][self.idx_start-self.idx_range])[0:10].replace('-', '/'),
#                        self.idx_start -3*self.idx_range//4 : str(data['date'][self.idx_start -3*self.idx_range//4])[0:10].replace('-', '/'),
#                        self.idx_start -self.idx_range//2 : str(data['date'][self.idx_start -self.idx_range//2])[0:10].replace('-', '/'),
#                        self.idx_start -self.idx_range//4 : str(data['date'][self.idx_start -self.idx_range//4])[0:10].replace('-', '/'),
#                        self.idx_start - 1: str(data['date'][self.idx_start - 1])[0:10].replace('-', '/')}
#        self.stringaxis = self.candle_plot.getAxis('bottom')
#        self.stringaxis.setTicks([self.xdict.items()])
#        self.candle_plot.showAxis('bottom', False)
#        self.candle_plot.showAxis('left', False)
#        self.stringaxis2 = self.volume_plot.getAxis('bottom')
#        self.stringaxis2.setTicks([self.xdict.items()])
#        self.volume_plot.showAxis('bottom', False)
#        self.volume_plot.showAxis('left', False)

        self.candle_plot.setXRange(self.idx_start-self.idx_range-1, self.x_max, padding=0)
        self.volume_plot.setXRange(self.idx_start-self.idx_range-1, self.x_max, padding=0)

        self.candle_item = CandleItem(self.data,self.idx_range,self.idx_start)
        self.vol_item=VolItem(self.data,self.idx_range,self.idx_start)
        self.candle_plot.addItem(self.candle_item)
        self.volume_plot.addItem(self.vol_item)
        dd=(self.candle_item.max_high-self.candle_item.min_low)/20
        self.candle_plot.setYRange(self.candle_item.min_low-dd, self.candle_item.max_high+dd, padding=0)
        d=0
        if self.candle_item.max_i==self.idx_range-2 and self.idx_range>=120:
            d=20
        elif self.candle_item.max_i==self.idx_range-1 and self.idx_range>=120:
            d=35
        self.max_label.setText(str(self.candle_item.max_high))
        a=self.baseWidth/self.idx_range
        if self.idx_range<120 and self.idx_start<120:
            a=12.25
        self.max_label.move(self.candle_item.max_i*a-d,5)
        self.min_label.setText(str(self.candle_item.min_low))
        d=0
        if self.candle_item.min_i==self.idx_range-2 and self.idx_start>2:
            d=20
        elif self.candle_item.min_i==self.idx_range-1 and self.idx_start>1:
            d=35
        self.min_label.move(self.candle_item.min_i*a-d,self.baseheight-32)

    def deal_with_data(self,data):
        self.data=data
        self.data['MA5'] = self.data['close'].rolling(window=5).mean()
        self.data['MA10'] = self.data['close'].rolling(window=10).mean()
        self.data['MA20'] = self.data['close'].rolling(window=20).mean()
        self.data['MA60'] = self.data['close'].rolling(window=60).mean()

        self.data['VMA5'] = self.data['volume'].rolling(window=5).mean()/500
        self.data['VMA10'] = self.data['volume'].rolling(window=10).mean()/500

    def mouseMoved(self,ev):
        pos = ev[0]
        if pos.x()>=self.baseWidth-7 or pos.x()<=0 or pos.y()>=self.baseheight-1 or pos.y()<=0:
            self.ylabel.hide()
            self.xlabel.hide()
            return
        if self.candle_plot.sceneBoundingRect().contains(pos):
            mousePoint = self.candle_plot.plotItem.vb.mapSceneToView(pos)#转换坐标系

            self.index = int(mousePoint.x() + 0.5)  # 鼠标所处的x轴坐标
            if self.index<self.idx_start and self.index>=0:
                self._signal.emit()
            if self.idx_start-self.idx_range-1 < self.index < self.idx_start:
                trade_date = datetime.datetime.strptime(self.data['date'][self.index],'%Y-%m-%d').strftime("%m/%d/%Y")

                # 显示x, y坐标跟随鼠标移动
                if not self.ylabel is None:
                    self.ylabel.setText(str(round(mousePoint.y(), 2)))
                    self.ylabel.move(0,pos.y()-self.ylabel.geometry().height()/2)
                    if self.ylabel.isHidden():
                        self.ylabel.show()
                if not self.xlabel is None:
                    self.xlabel.setText(trade_date)
                    self.xlabel.move(pos.x() - self.xlabel.geometry().width()/2,self.xlabel.geometry().y())
                    if self.xlabel.isHidden():
                        self.xlabel.show()

    def leaveEvent(self, a0):
        if not self.ylabel is None:
            self.ylabel.hide()
        if not self.xlabel is None:
            self.xlabel.hide()

class CandleItem(pg.GraphicsObject):
    def __init__(self,data,idx_range,idx_start):
        pg.GraphicsObject.__init__(self)
        self.generatePicture(data,idx_range,idx_start)

    def generatePicture(self,data,idx_range,idx_start):
        self.picture = QPicture()
        p = QPainter(self.picture)
        pg.setConfigOptions(leftButtonPan=False, antialias=True)
        w = 0.25
        self.max_high=0
        self.min_low=100000
        self.max_i=0
        self.min_i=0
        for i in range((idx_start-idx_range),idx_start):
            open, close, high, low = data['open'][i], data['close'][i], data['high'][i], data['low'][i]
            if self.max_high<high:
                self.max_high=high
                self.max_i=i-(idx_start-idx_range)
            if self.min_low>low:
                self.min_low=low
                self.min_i=i-(idx_start-idx_range)
            if i-1>=0:
                if not pd.isna(data['MA5'][i-1]):
                    p.setPen(pg.mkPen(QColor(255, 255, 255)))
                    p.drawLine(QPointF(i-1, data['MA5'][i-1]), QPointF(i, data['MA5'][i]))
                if not pd.isna(data['MA10'][i-1]):
                    p.setPen(pg.mkPen(QColor(255, 255, 0)))
                    p.drawLine(QPointF(i-1, data['MA10'][i-1]), QPointF(i, data['MA10'][i]))
                if not pd.isna(data['MA20'][i-1]):
                    p.setPen(pg.mkPen(QColor(0, 255, 0)))
                    p.drawLine(QPointF(i-1, data['MA20'][i-1]), QPointF(i, data['MA20'][i]))
                if not pd.isna(data['MA60'][i-1]):
                    p.setPen(pg.mkPen(QColor(205,0,0)))
                    p.drawLine(QPointF(i-1, data['MA60'][i-1]), QPointF(i, data['MA60'][i]))
            if open > close:
                p.setPen(pg.mkPen(QColor(2,148,255)))
                p.setBrush(pg.mkBrush(QColor(2,148,255)))
            else:
                p.setPen(pg.mkPen('w'))
                p.setBrush(pg.mkBrush('w'))
            if high!=low:
                p.drawLine(QPointF(i, low), QPointF(i, high))
            p.drawRect(QRectF(i - w, open, w * 2, close - open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

class VolItem(pg.GraphicsObject):
    def __init__(self, data,idx_range,idx_start):
        pg.GraphicsObject.__init__(self)
        self.generatePicture(data,idx_range,idx_start)

    def generatePicture(self,data,idx_range,idx_start):
        self.picture = QPicture()
        p = QPainter(self.picture)
        pg.setConfigOptions(leftButtonPan=False, antialias=False)
        w=0.25
        for i in range((idx_start-idx_range),idx_start):
            open, close, vol = data['open'][i], data['close'][i], data['volume'][i]/500
            if i-1>=0:
                if not pd.isna(data['VMA5'][i-1]):
                    p.setPen(pg.mkPen(QColor(255, 255, 0)))
                    p.drawLine(QPointF(i-1, data['VMA5'][i-1]), QPointF(i, data['VMA5'][i]))
                if not pd.isna(data['VMA10'][i-1]):
                    p.setPen(pg.mkPen(QColor(0, 255, 0)))
                    p.drawLine(QPointF(i-1, data['VMA10'][i-1]), QPointF(i, data['VMA10'][i]))
            if open > close:
                p.setPen(pg.mkPen(QColor(2,148,255)))
                p.setBrush(pg.mkBrush(QColor(2,148,255)))
            else:
                p.setPen(pg.mkPen('w'))
                p.setBrush(pg.mkBrush('w'))
            p.drawRect(QRectF(i - w, 0, w * 2, vol))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())
