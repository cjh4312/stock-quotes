# This Python file uses the following encoding: utf-8

import pyqtgraph as pg
from PySide6.QtWidgets import QWidget,QVBoxLayout
from PySide6.QtGui import QColor,QPainter,QPicture
from PySide6.QtCore import Signal,QPointF,QRectF

class DrawChart(QWidget):
    _signal=Signal()
    def __init__(self,high_low_point, data):
        super(DrawChart, self).__init__()
        self.pre_len=len(data)
        self.deal_with_data(high_low_point,data)
        self.baseheight=300
        self.baseWidth=420
        self.time_share_widget=QWidget()
        self.time_share_widget.setMaximumHeight(self.baseheight)
        self.time_share_widget.setMinimumWidth(self.baseWidth)
        self.time_share_layout=QVBoxLayout()
        self.time_share_layout.setContentsMargins(0,2,0,0)
        self.time_share_layout.setSpacing(1)
        self.time_share_widget.setLayout(self.time_share_layout)
        self.time_share_plot = pg.PlotWidget()
        #self.time_share_plot.setMinimumHeight(200)

        xdict = {0:'09:30',60:'10:30',120:'13:00',180:'14:00',240:'15:00'}
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        #self.time_share_plot.setGeometry(0,0,self.baseWidth,self.baseheight)
        self.volume_plot= pg.PlotWidget(axisItems={'bottom':stringaxis},enableMenu=False)
        self.volume_plot.setMaximumHeight(60)
        #self.volume_plot.setGeometry(0,self.baseheight,self.baseWidth,100)
        self.time_share_layout.addWidget(self.time_share_plot)
        self.time_share_layout.addWidget(self.volume_plot)

        #self.candle_plot = pg.PlotWidget(axisItems={'bottom': self.stringaxis},background=QColor(219,241,255),enableMenu=False)
        self.time_share_plot.showAxis('bottom', False)
        self.time_share_plot.showAxis('left', False)
        #self.volume_plot= pg.PlotWidget(axisItems={'bottom': self.stringaxis2},background=QColor(219,241,255),enableMenu=False)
        #self.volume_plot.showAxis('bottom', False)
        self.volume_plot.showAxis('left', False)

        self.time_share_plot.showGrid(x=False, y=True)
        self.volume_plot.showGrid(x=False, y=True)
        self.time_share_plot.setMouseEnabled(x=False, y=False)
        self.volume_plot.setMouseEnabled(x=False, y=False)
        self.time_share_plot.setXRange(-1, 241, padding=0)

        self.time_share_plot.setYRange(self.low_point, self.high_point, padding=0)
        self.volume_plot.setXRange(-1, 241, padding=0)
        self.volume_plot.setYRange(0, self.high_vol, padding=0)

        self.time_share_item = TimeShareItem(data,self.low_point ,self.high_point,self.high_stop,self.low_stop)
        self.vol_item=VolItem(data,self.high_vol)
        self.time_share_plot.addItem(self.time_share_item)
        self.volume_plot.addItem(self.vol_item)

    def init(self,high_low_point,data):
        self.time_share_plot.removeItem(self.time_share_item)
        self.volume_plot.removeItem(self.vol_item)
        self.deal_with_data(high_low_point,data)
        l=len(data)

        d=60
        if l<240:
            l=240
        elif l>1000:
            d=180
        elif l>500:
            d=120
#        if self.pre_len!=len(data):
#            self.pre_len=len(data)
#        xdict={}
        x=[]
        strs=[]
        for i in range(0,len(data),d):
            x.append(i)
            strs.append(data['Time'][i][11:16])
#            xdict[i]= data['Time'][i][11:16]
#        stringaxis = pg.AxisItem(orientation='bottom')
#        stringaxis.setTicks([xdict.items()])
        #self.volume_plot.setAxisItems(axisItems={'bottom':stringaxis})
        xAxis = self.volume_plot.getAxis('bottom')
        ticks = [(i, j) for i, j in zip(x,strs)]
        xAxis.setTicks([ticks])

        self.time_share_plot.setXRange(0, l, padding=0)
        self.volume_plot.setXRange(0, l, padding=0)
        self.time_share_plot.setYRange(self.low_point, self.high_point, padding=0)
        self.volume_plot.setYRange(0, self.high_vol, padding=0)
        self.time_share_plot.removeItem(self.time_share_item)
        self.volume_plot.removeItem(self.vol_item)

        self.time_share_item = TimeShareItem(data,self.high_point,self.low_point,self.high_stop,self.low_stop)
        self.vol_item=VolItem(data,self.high_vol)
        self.time_share_plot.addItem(self.time_share_item)
        self.volume_plot.addItem(self.vol_item)

    def deal_with_data(self,high_low_point,data):

        self.high_vol=high_low_point[2]
        self.high_point=high_low_point[0]+0.5
        self.low_point=high_low_point[1]-0.5
        self.high_stop=high_low_point[3]
        self.low_stop=high_low_point[4]

class TimeShareItem(pg.GraphicsObject):
    def __init__(self,data,low_point,high_ponit,high_stop,low_stop):
        pg.GraphicsObject.__init__(self)
        self.generatePicture(data,low_point,high_ponit,high_stop,low_stop)

    def generatePicture(self,data,high_point,low_point,high_stop,low_stop):
        self.picture = QPicture()
        p = QPainter(self.picture)
        pg.setConfigOptions(leftButtonPan=False, antialias=True)
        p.setPen(pg.mkPen('blue'))
        l=len(data)
        d=30
        if l<240:
            l=240
        elif l>1000:
            d=180
        elif l>600:
            d=120
        elif l>400:
            d=60
        p.drawLine(QPointF(0, 0), QPointF(l, 0))

        p.setPen(pg.mkPen('gray'))
        for i in range(1,l//d):
            p.drawLine(QPointF(i*d,high_point), QPointF(i*d, low_point))

        p.drawLine(QPointF(0, 2.5), QPointF(l, 2.5))
        p.drawLine(QPointF(0, 7.5), QPointF(l, 7.5))
        p.drawLine(QPointF(0, 15), QPointF(l, 15))
        p.drawLine(QPointF(0, 20), QPointF(l, 20))
        p.drawLine(QPointF(0, -2.5), QPointF(l, -2.5))
        p.drawLine(QPointF(0, -7.5), QPointF(l, -7.5))
        p.drawLine(QPointF(0, -15), QPointF(l, -15))
        p.drawLine(QPointF(0, -20), QPointF(l, -20))
        if high_point-0.5>=5:
            p.setPen(pg.mkPen('r'))
            p.drawLine(QPointF(0, 5), QPointF(l, 5))
        if high_point-0.5>=high_stop:
            p.setPen(pg.mkPen(QColor(255, 0, 255)))
            p.drawLine(QPointF(0, high_stop), QPointF(l, high_stop))
        if low_point+0.5<=-5:
            p.setPen(pg.mkPen(QColor(60,179,113)))
            p.drawLine(QPointF(0, -5), QPointF(l, -5))
        if low_point+0.5<=low_stop:
            p.setPen(pg.mkPen(QColor(0, 255, 0)))
            p.drawLine(QPointF(0, low_stop), QPointF(l, low_stop))

        for i in range(len(data)):
            if i-1>=0:
                price1 ,price2= data['price'][i-1],data['price'][i]
                ave_price1,ave_price2=data['ave_price'][i-1],data['ave_price'][i]
                p.setPen(pg.mkPen('yellow'))
                p.drawLine(QPointF((i-1), price1), QPointF(i, price2))
                p.setPen(pg.mkPen('white'))
                p.drawLine(QPointF((i-1), ave_price1), QPointF(i, ave_price2))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())

class VolItem(pg.GraphicsObject):
    def __init__(self, data,high_vol):
        pg.GraphicsObject.__init__(self)
        self.generatePicture(data,high_vol)

    def generatePicture(self,data,high_vol):
        self.picture = QPicture()
        p = QPainter(self.picture)
        pg.setConfigOptions(leftButtonPan=False, antialias=False)
        p.setPen(pg.mkPen('gray'))
        l=len(data)
        d=30
        if l<240:
            l=240
        elif l>1000:
            d=180
        elif l>600:
            d=120
        elif l>400:
            d=60
        for i in range(1,l//d):
            if high_vol>=1000000000:
                break
            p.drawLine(QPointF(i*d,0), QPointF(i*d,high_vol))

        for i in range(len(data)):
            vol,direct= data['vol'][i], data['direct'][i]
            if vol>=1000000000:
                break
            if direct==2:
                p.setPen(pg.mkPen('r'))
            elif direct==1:
                p.setPen(pg.mkPen(QColor(0, 255, 0)))
            else:
                p.setPen(pg.mkPen('w'))
            p.drawLine(QPointF(i, 0), QPointF(i, vol))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())
