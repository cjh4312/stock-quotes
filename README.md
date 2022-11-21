# stock-quotes
股票行情软件

因为一般看盘软件都无法在linux下使用，所以自己干脆写了一个跨平台的。

python+pyqt。

查看全球主要指数，实盘美股和港股。

A股板块、指数、个股k线图均线资料查看、搜索，输入拼音查询。

F10资料，主要指标，经营分析，3大报表，板块资金流。

实时语音播报当前新闻

后续功能再慢慢加。。。。。。

需要解决的问题：

一、可以实时浏览所有股票（A股，美股，港股）

['代码','名称','最新价','涨跌幅','换手率','成交额','市盈率','成交量','总市值','流通市值','今年涨幅','60日涨幅','涨速','最高','最低','今开','昨收']
表格数据用QTableView组件，使用model/view模型控制显示的颜色，格式。

A股，美股，港股全部都使用同样的数据结构，这样可以很方便界面的切换。一个model模式就可以了。在做其它（比如资金流分析）时，再建一个model模式。

看盘的主界面上分了4大块区域（个人习惯），一个显示所有股票的实时数据，一个只显示涨速，一个自选股，最右边显示个股的详细信息，包括分时图，买卖一到五及其分笔成交细节。

点击表格任何一列实现顺序、倒序排列。比如按涨幅，成交额排序

![Snipaste_2022-11-06_19-20-46](https://user-images.githubusercontent.com/29307274/200167923-75be3496-439d-48f6-8e2b-42c7edffc02f.jpg)

二、实现鼠标和键盘操作

重载鼠标的单击和双击，单击显示个股详细信息，双击显示个股的k线图。鼠标滚轮，右键功能

重载键盘事件，回车也可显示个股的k线图。输入个股、指数、板块的代码，拼音都可查询。ESC键，翻页键。F10查看个股报表资讯

三、需要多线程，刷新数据的同时界面不能卡顿。

可能是数据原因或者python的原因，为了保证实时，同时开了6个线程

一个用于刷新全球实时指数

一个刷新所有股票的实时数据

一个刷新买卖一到五的数据

一个刷新分笔成交数据

一个实时语音播报

一个用于获取k线图数据，这个觉得有些多余，但是在开盘阶段如果想看k线图，偶尔会出现卡顿的情况，所以单独开了一个线程。

四、目前所遇到问题：

    在盘后操作基本还是很流畅的，反应速度也很快。主要在开盘阶段，因为每5秒刷新一次界面，如果正好在刷新的时刻单击或者双击某一行股票，就会出现卡顿现象。我感觉可能是ui刷新速度不够快，同一时刻子线程均发信号要求刷新界面导致。又或者是我代码有问题，或者python的速度问题。
    由于以前没有学过python，临时从c++转过来，基本是按照c++的编程思路来的。也不知道合适不，欢迎大家多提建议。

![Snipaste_2022-11-06_19-21-27](https://user-images.githubusercontent.com/29307274/200167939-b4401eac-f204-4335-bc96-82d1f71e4251.jpg)
![Snipaste_2022-11-06_19-22-01](https://user-images.githubusercontent.com/29307274/200167941-64237622-e2e6-46e1-a52c-1fd7183637cf.jpg)
![Snipaste_2022-11-06_19-22-36](https://user-images.githubusercontent.com/29307274/200167942-01991042-fa3d-43b6-8f2a-eec6aca27c92.jpg)
![Snipaste_2022-11-06_19-24-37](https://user-images.githubusercontent.com/29307274/200167943-a318c9cd-16b0-47c1-b1d6-02b601d595a0.jpg)
![Snipaste_2022-11-06_19-25-25](https://user-images.githubusercontent.com/29307274/200167945-a9750d43-b587-4a5e-81db-6fa194930a1f.jpg)
![Snipaste_2022-11-06_19-25-57](https://user-images.githubusercontent.com/29307274/200167946-8cfeccf3-7a48-4cde-98b8-2baf4644a9e2.jpg)
