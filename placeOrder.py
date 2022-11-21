# coding:utf-8
import pywinauto
from pywinauto.keyboard import send_keys

#app=pywinauto.application.Application(backend='uia').start('D:\\tc\/xiadan.exe')
app_connect=pywinauto.application.Application(backend='uia').connect(title='网上股票交易系统5.0')
#time.sleep(2)
obj=app_connect.window(title='网上股票交易系统5.0')
#turn to buy
obj.window(class_name='SysTreeView32')
obj.window(title='卖出[F2]')
obj.type_keys('600519')
send_keys('{TAB}')
send_keys('{TAB}')
obj.type_keys('500')
obj.window(title='卖出[S]').click()
#send_keys('{Y}')
