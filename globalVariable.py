# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import os,pytz
import datetime
from PySide6.QtGui import QPalette,QColor
from PySide6.QtCore import Qt,QSettings

settings = QSettings("config.ini", QSettings.IniFormat)

def _init():
    global whatInterface
    whatInterface=1
    global marketNum
    marketNum=1
    global PreInterface
    PreInterface=0
    global subCount
    subCount=1
    global isBoardWidth
    isBoardWidth=False
    init_style()

def init_style():
    global pered
    pered = QPalette()
    global pegreen
    pegreen = QPalette()
    global peblack
    peblack= QPalette()
    global peblue
    peblue = QPalette()
    global redBackGround
    redBackGround=QPalette()
    global greenBackGround
    greenBackGround=QPalette()
    pered.setColor(QPalette.WindowText,Qt.red)
    pegreen.setColor(QPalette.WindowText,QColor(0,191,0))
    peblack.setColor(QPalette.WindowText,Qt.black)
    peblue.setColor(QPalette.WindowText,Qt.blue)
    global circle_green_SheetStyle
    circle_green_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:green"
    global circle_red_SheetStyle
    circle_red_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:red"

def getValue():
    return whatInterface

def setValue(value):
    global whatInterface
    whatInterface=value

def getIsNet():
    IsNet=os.system('ping 110.242.68.66 -n 1')
    return IsNet

#是否交易日
def isWeekend():
    tz = pytz.timezone('Asia/shanghai')
    date_zh = datetime.datetime.now(tz)
    localweek=int(date_zh.strftime('%w'))
    if localweek in [1,2,3,4,5]:
        return False
    else:
        return True

def isHKMarketDay():
    tz = pytz.timezone('Asia/Hong_Kong')
    date_zh = datetime.datetime.now(tz)
    Vacation=settings.value("General/Vacation_HK")
    localdate=int(date_zh.strftime('%m%d'))
    localweek=int(date_zh.strftime('%w'))
    localtime=int(date_zh.strftime("%H%M%S"))
    if localdate not in Vacation and localweek in [1,2,3,4,5] and ((localtime>=91500 and localtime<=121505) or (localtime>=130000 and localtime<=161505)):
        return True
    else:
        return False
def isZhMarketDay():
    tz = pytz.timezone('Asia/shanghai')
    date_zh = datetime.datetime.now(tz)
    Vacation=eval(settings.value("General/Vacation_ZH"))
    localdate=int(date_zh.strftime('%m%d'))
    localweek=int(date_zh.strftime('%w'))
    localtime=int(date_zh.strftime("%H%M%S"))
    if localdate not in Vacation and localweek in [1,2,3,4,5] and ((localtime>=91500 and localtime<=113010) or (localtime>=130000 and localtime<=150010)):
        return True
    else:
        return False

def isUSMarketDay():
    tz = pytz.timezone('America/New_York')
    date_us = datetime.datetime.now(tz)
    Vacation=eval(settings.value("General/Vacation_US"))
    localdate=int(date_us.strftime('%m%d'))
    localweek=int(date_us.strftime('%w'))
    localtime=int(date_us.strftime("%H%M%S"))
    if localdate not in Vacation and localweek in [1,2,3,4,5] and (localtime>=93000 and localtime<=160005):
        return True
    else:
        return False

def curRecentMarketDay():
    date=datetime.datetime.now()
    for i in range(15):
        time=date+datetime.timedelta(days=-i)
        if isMarketDay(time):
            break
    return str(time.date())

def isMarketDay(date_zh):
    Vacation=eval(settings.value("General/Vacation_ZH"))
    local=datetime.datetime.now()
    localdate=int(date_zh.strftime('%m%d'))
    localweek=int(date_zh.strftime('%w'))
    localtime=int(local.strftime("%H%M%S"))
    if localdate not in Vacation and localweek in [1,2,3,4,5]:
        if local==date_zh and localtime<150000:
            return False
        return True
    else:
        return False

def format_conversion(grid):
    if isinstance(grid,float):
        if float(grid)>=100000000:
            return str(round(float(grid)/100000000,4))+'亿'
        elif float(grid)>=10000:
            return str(round(float(grid)/10000,4))+'万'
        elif float(grid)<=-100000000:
            return str(round(float(grid)/100000000,4))+'亿'
        elif float(grid)<=-10000:
            return str(round(float(grid)/10000,4))+'万'
        return str(round(float(grid),2))
    elif isinstance(grid,int):
        if int(grid)>=100000000:
            return str(round(int(grid)/100000000,4))+'亿'
        elif int(grid)>=10000:
            return str(round(int(grid)/10000,4))+'万'
        elif int(grid)<=-100000000:
            return str(round(int(grid)/100000000,4))+'亿'
        elif int(grid)<=-10000:
            return str(round(int(grid)/10000,4))+'万'
    elif str(grid).isdigit():
        if int(grid)>=100000000:
            return str(round(int(grid)/100000000,4))+'亿'
        elif int(grid)>=10000:
            return str(round(int(grid)/10000,4))+'万'
        elif int(grid)<=-100000000:
            return str(round(int(grid)/100000000,4))+'亿'
        elif int(grid)<=-10000:
            return str(round(int(grid)/10000,4))+'万'
    return str(grid)

def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1]
        if asc >= 45217 and asc <= 45252:
            return 'a'
        if asc >= 45253 and asc <= 45760:
            return 'b'
        if asc >= 45761 and asc <= 46317:
            return 'c'
        if asc >= 46318 and asc <= 46825:
            return 'd'
        if asc >= 46826 and asc <= 47009:
            return 'e'
        if asc >= 47010 and asc <= 47296:
            return 'f'
        if asc >= 47297 and asc <= 47613:
            return 'g'
        if asc >= 47614 and asc <= 48118:
            return 'h'
        if asc >= 48119 and asc <= 49061:
            return 'j'
        if asc >= 49062 and asc <= 49323:
            return 'k'
        if asc >= 49324 and asc <= 49895:
            return 'l'
        if asc >= 49896 and asc <= 50370:
            return 'm'
        if asc >= 50371 and asc <= 50613:
            return 'n'
        if asc >= 50614 and asc <= 50621:
            return 'o'
        if asc >= 50622 and asc <= 50905:
            return 'p'
        if asc >= 50906 and asc <= 51386:
            return 'q'
        if asc >= 51387 and asc <= 51445:
            return 'r'
        if asc >= 51446 and asc <= 52217:
            return 's'
        if asc >= 52218 and asc <= 52697:
            return 't'
        if asc >= 52698 and asc <= 52979:
            return 'w'
        if asc >= 52980 and asc <= 53688:
            return 'x'
        if asc >= 53689 and asc <= 54480:
            return 'y'
        if asc >= 54481 and asc <= 55289:
            return 'z'
        return ''

def getPinyin(string):
    if string == None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        if l >= u'\u4e00' and l <= u'\u9fa5':
            charLst.append(single_get_first(l))
        else:
            charLst.append(l)
    return ''.join(charLst)
