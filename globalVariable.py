# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import os, pytz
import datetime
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt, QSettings, QDateTime

settings = QSettings("config.ini", QSettings.IniFormat)

def _init():
    global whatInterface
    whatInterface = 1
    global marketNum
    marketNum = 1
    global PreInterface
    PreInterface = 0
    global subCount
    subCount = 1
    global isBoardWidth
    isBoardWidth = False
    init_style()

def init_style():
    global pered
    pered = QPalette()
    global pegreen
    pegreen = QPalette()
    global peblack
    peblack = QPalette()
    global peblue
    peblue = QPalette()
    global redBackGround
    redBackGround = QPalette()
    global greenBackGround
    greenBackGround = QPalette()
    pered.setColor(QPalette.WindowText, Qt.red)
    pegreen.setColor(QPalette.WindowText, QColor(0, 191, 0))
    peblack.setColor(QPalette.WindowText, Qt.black)
    peblue.setColor(QPalette.WindowText, Qt.blue)
    global circle_green_SheetStyle
    circle_green_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:green"
    global circle_red_SheetStyle
    circle_red_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:red"

def getValue():
    return whatInterface

def setValue(value):
    global whatInterface
    whatInterface = value

def getIsNet():
    IsNet = os.system('ping 110.242.68.66 -n 1')
    return IsNet

# 是否交易日
def isWeekend():
    tz = pytz.timezone('Asia/shanghai')
    date_zh = datetime.datetime.now(tz)
    localweek = int(date_zh.strftime('%w'))
    if localweek in [1, 2, 3, 4, 5]:
        return False
    else:
        return True

def isHKMarketDay():
    tz = pytz.timezone('Asia/Hong_Kong')
    date_zh = datetime.datetime.now(tz)
    Vacation = eval(settings.value("General/Vacation_HK"))
    localdate = int(date_zh.strftime('%m%d'))
    localweek = int(date_zh.strftime('%w'))
    localtime = int(date_zh.strftime("%H%M%S"))
    if localdate not in Vacation and localweek in [1, 2, 3, 4, 5] and (
            (90000 <= localtime <= 121505) or (130000 <= localtime <= 161505)):
        return True
    else:
        return False

def isZhMarketDay():
    tz = pytz.timezone('Asia/shanghai')
    date_zh = datetime.datetime.now(tz)
    Vacation = eval(settings.value("General/Vacation_ZH"))
    localdate = int(date_zh.strftime('%m%d'))
    localweek = int(date_zh.strftime('%w'))
    localtime = int(date_zh.strftime("%H%M%S"))
    if localdate not in Vacation and localweek in [1, 2, 3, 4, 5] and (
            (91500 <= localtime <= 113010) or (130000 <= localtime <= 150010)):
        return True
    else:
        return False

def isUSMarketDay():
    tz = pytz.timezone('America/New_York')
    date_us = datetime.datetime.now(tz)
    Vacation = eval(settings.value("General/Vacation_US"))
    localdate = int(date_us.strftime('%m%d'))
    localweek = int(date_us.strftime('%w'))
    localtime = int(date_us.strftime("%H%M%S"))
    if localdate not in Vacation and localweek in [1, 2, 3, 4, 5] and (localtime >= 93000 and localtime <= 160005):
        return True
    else:
        return False

def curRecentMarketDay():
    date = datetime.datetime.now()
    for i in range(15):
        time = date + datetime.timedelta(days=-i)
        if isMarketDay(time):
            return time
    return 0

def time_to_QDateTime(time):
    str = time.strftime("%Y%m%d %H:%M:%S")
    date = QDateTime.fromString(str, "yyyyMMdd hh:mm:ss").date()
    return date

def isMarketDay(date_zh):
    Vacation = eval(settings.value("General/Vacation_ZH"))
    local = datetime.datetime.now()
    localdate = int(date_zh.strftime('%m%d'))
    localweek = int(date_zh.strftime('%w'))
    localtime = int(local.strftime("%H%M%S"))
    if localdate not in Vacation and localweek in [1, 2, 3, 4, 5]:
        if local == date_zh and localtime < 150000:
            return False
        return True
    return False

def format_conversion(grid):
    if isinstance(grid, float):
        if float(grid) >= 100000000:
            return str(round(float(grid) / 100000000, 4)) + '亿'
        elif float(grid) >= 10000:
            return str(round(float(grid) / 10000, 4)) + '万'
        elif float(grid) <= -100000000:
            return str(round(float(grid) / 100000000, 4)) + '亿'
        elif float(grid) <= -10000:
            return str(round(float(grid) / 10000, 4)) + '万'
        return str(round(float(grid), 2))
    elif isinstance(grid, int):
        if int(grid) >= 100000000:
            return str(round(int(grid) / 100000000, 4)) + '亿'
        elif int(grid) >= 10000:
            return str(round(int(grid) / 10000, 4)) + '万'
        elif int(grid) <= -100000000:
            return str(round(int(grid) / 100000000, 4)) + '亿'
        elif int(grid) <= -10000:
            return str(round(int(grid) / 10000, 4)) + '万'
    elif str(grid).isdigit():
        if int(grid) >= 100000000:
            return str(round(int(grid) / 100000000, 4)) + '亿'
        elif int(grid) >= 10000:
            return str(round(int(grid) / 10000, 4)) + '万'
        elif int(grid) <= -100000000:
            return str(round(int(grid) / 100000000, 4)) + '亿'
        elif int(grid) <= -10000:
            return str(round(int(grid) / 10000, 4)) + '万'
    return str(grid)

def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1]
        if 45217 <= asc <= 45252:
            return 'a'
        if 45253 <= asc <= 45760:
            return 'b'
        if 45761 <= asc <= 46317:
            return 'c'
        if 46318 <= asc <= 46825:
            return 'd'
        if 46826 <= asc <= 47009:
            return 'e'
        if 47010 <= asc <= 47296:
            return 'f'
        if 47297 <= asc <= 47613:
            return 'g'
        if 47614 <= asc <= 48118:
            return 'h'
        if 48119 <= asc <= 49061:
            return 'j'
        if 49062 <= asc <= 49323:
            return 'k'
        if 49324 <= asc <= 49895:
            return 'l'
        if 49896 <= asc <= 50370:
            return 'm'
        if 50371 <= asc <= 50613:
            return 'n'
        if 50614 <= asc <= 50621:
            return 'o'
        if 50622 <= asc <= 50905:
            return 'p'
        if 50906 <= asc <= 51386:
            return 'q'
        if 51387 <= asc <= 51445:
            return 'r'
        if 51446 <= asc <= 52217:
            return 's'
        if 52218 <= asc <= 52697:
            return 't'
        if 52698 <= asc <= 52979:
            return 'w'
        if 52980 <= asc <= 53688:
            return 'x'
        if 53689 <= asc <= 54480:
            return 'y'
        if 54481 <= asc <= 55289:
            return 'z'
        return ''

def getPinyin(string):
    if string == None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        if u'\u4e00' <= l <= u'\u9fa5':
            charLst.append(single_get_first(l))
        else:
            charLst.append(l)
    return ''.join(charLst)
