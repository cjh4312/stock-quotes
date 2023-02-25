# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1920, 1080)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(False)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u"logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.download_d = QAction(MainWindow)
        self.download_d.setObjectName(u"download_d")
        self.download_d.setEnabled(False)
        self.exit = QAction(MainWindow)
        self.exit.setObjectName(u"exit")
        self.download_info = QAction(MainWindow)
        self.download_info.setObjectName(u"download_info")
        self.us_market = QAction(MainWindow)
        self.us_market.setObjectName(u"us_market")
        self.us_market.setCheckable(True)
        self.us_market.setChecked(False)
        self.us_market.setEnabled(True)
        self.financial_flows = QAction(MainWindow)
        self.financial_flows.setObjectName(u"financial_flows")
        self.financial_flows.setCheckable(False)
        self.zh_market = QAction(MainWindow)
        self.zh_market.setObjectName(u"zh_market")
        self.zh_market.setCheckable(True)
        self.zh_market.setChecked(True)
        self.hk_market = QAction(MainWindow)
        self.hk_market.setObjectName(u"hk_market")
        self.hk_market.setCheckable(True)
        self.actF10 = QAction(MainWindow)
        self.actF10.setObjectName(u"actF10")
        self.actF3 = QAction(MainWindow)
        self.actF3.setObjectName(u"actF3")
        self.newsReport = QAction(MainWindow)
        self.newsReport.setObjectName(u"newsReport")
        self.newsReport.setCheckable(True)
        self.newsReport.setChecked(False)
        self.pick_stocks = QAction(MainWindow)
        self.pick_stocks.setObjectName(u"pick_stocks")
        self.us_zh_stock = QAction(MainWindow)
        self.us_zh_stock.setObjectName(u"us_zh_stock")
        self.us_zh_stock.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(-1, 0, 1920, 1030))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setBold(False)
        self.frame.setFont(font1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 25))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setFont(font1)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menu.addAction(self.download_d)
        self.menu.addAction(self.download_info)
        self.menu.addAction(self.newsReport)
        self.menu.addAction(self.exit)
        self.menu_2.addAction(self.zh_market)
        self.menu_2.addAction(self.us_market)
        self.menu_2.addAction(self.hk_market)
        self.menu_2.addAction(self.us_zh_stock)
        self.menu_3.addAction(self.financial_flows)
        self.menu_3.addAction(self.pick_stocks)
        self.menu_4.addAction(self.actF10)
        self.menu_4.addAction(self.actF3)

        self.retranslateUi(MainWindow)
        self.exit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.download_d.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7dk\u7ebf\u6570\u636e", None))
        self.exit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.download_info.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u80a1\u7968\u4fe1\u606f", None))
        self.us_market.setText(QCoreApplication.translate("MainWindow", u"\u7f8e\u80a1", None))
        self.financial_flows.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u91d1\u6d41", None))
        self.zh_market.setText(QCoreApplication.translate("MainWindow", u"A\u80a1", None))
        self.hk_market.setText(QCoreApplication.translate("MainWindow", u"\u6e2f\u80a1", None))
        self.actF10.setText(QCoreApplication.translate("MainWindow", u"F10---\u8d22\u52a1\u5206\u6790 \u7ecf\u8425\u5206\u6790", None))
        self.actF3.setText(QCoreApplication.translate("MainWindow", u"F3---\u70ed\u5ea6\u5173\u952e\u8bcd", None))
        self.newsReport.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u8bed\u97f3\u64ad\u62a5", None))
        self.pick_stocks.setText(QCoreApplication.translate("MainWindow", u"\u516c\u5f0f\u9009\u80a1", None))
        self.us_zh_stock.setText(QCoreApplication.translate("MainWindow", u"\u7f8e\u4e2d\u6982\u80a1", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5176\u5b83\u5e02\u573a", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u5206\u6790", None))
        self.menu_4.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

