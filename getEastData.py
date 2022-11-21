# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import requests
import pandas as pd
import py_mini_racer
from importlib import resources
from bs4 import BeautifulSoup
from tqdm import tqdm

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'}
def getStockHot():
    url = "https://emappdata.eastmoney.com/stockrank/getAllCurrentList"
    payload = {
        "appId": "appId01",
        "globalId": "786e4c21-70dc-435a-93bb-38",
        "marketType": "",
        "pageNo": 1,
        "pageSize": 100,
    }
    r = requests.post(url, json=payload,headers=headers)
    data_json = r.json()
    temp_rank_df = pd.DataFrame(data_json["data"])

    temp_rank_df["mark"] = [
        "0" + "." + item[2:] if "SZ" in item else "1" + "." + item[2:]
        for item in temp_rank_df["sc"]
    ]
    ",".join(temp_rank_df["mark"]) + "?v=08926209912590994"
    params = {
        "ut": "f057cbcbce2a86e2866ab8877db1d059",
        "fltt": "2",
        "invt": "2",
        "fields": "f14,f3,f12,f2",
        "secids": ",".join(temp_rank_df["mark"]) + ",?v=08926209912590994",
    }
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.columns = ["最新价", "涨跌幅", "代码", "股票名称"]
    temp_df["当前排名"] = temp_rank_df["rk"]
    temp_df["代码"] = temp_rank_df["sc"]
    temp_df = temp_df[
        [
            "当前排名",
            "代码",
            "股票名称",
            "最新价",
            "涨跌幅",
        ]
    ]
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors="coerce")
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors="coerce")
    return temp_df

def stock_hot_tgb():
    """
    淘股吧-热门股票
    https://www.taoguba.com.cn/stock/moreHotStock
    """
    url = "https://www.taoguba.com.cn/stock/moreHotStock"
    r = requests.get(url)
    temp_df = pd.concat([pd.read_html(r.text, header=0)[0], pd.read_html(r.text, header=0)[1]])
    temp_df = temp_df[[
        "个股代码",
        "个股名称",
    ]]
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df

def get_stock_pool_strong(date):
    """
    东方财富网-行情中心-涨停板行情-强势股池
    http://quote.eastmoney.com/ztb/detail#type=qsgc
    """
    url = "http://push2ex.eastmoney.com/getTopicQSPool"
    params = {
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wz.ztzt",
        "Pageindex": "0",
        "pagesize": "170",
        "sort": "zdp:desc",
        "date": date,
        "_": "1621590489736",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json["data"] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"]["pool"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.columns = [
        "序号",
        "代码",
        "_",
        "名称",
        "最新价",
        "涨停价",
        "_",
        "涨跌幅",
        "成交额",
        "流通市值",
        "总市值",
        "换手率",
        "是否新高",
        "入选理由",
        "量比",
        "涨速",
        "涨停统计",
        "所属行业",
    ]
    temp_df["涨停统计"] = (
        temp_df["涨停统计"].apply(lambda x: dict(x)["days"]).astype(str)
        + "/"
        + temp_df["涨停统计"].apply(lambda x: dict(x)["ct"]).astype(str)
    )
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "涨跌幅",
            "最新价",
            "涨停价",
            "成交额",
            "流通市值",
            "总市值",
            "换手率",
            "涨速",
            "是否新高",
            "量比",
            "涨停统计",
            "入选理由",
            "所属行业",
        ]
    ]
    temp_df["最新价"] = temp_df["最新价"] / 1000
    temp_df["涨停价"] = temp_df["涨停价"] / 1000
    return temp_df

def get_stock_hot_keyword(symbol):
    """
    东方财富-个股人气榜-关键词
    http://guba.eastmoney.com/rank/stock?code=000665
    """
    url = "https://emappdata.eastmoney.com/stockrank/getHotStockRankList"
    payload = {
        "appId": "appId01",
        "globalId": "786e4c21-70dc-435a-93bb-38",
        "srcSecurityCode": symbol,
    }
    r = requests.post(url, json=payload)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data'])
    del temp_df['flag']
    temp_df.columns = ['时间', '股票代码', '概念名称', '概念代码', '热度']
    return temp_df

def get_ths_js(file: str = "ths.js"):
    """Get path to data "ths.js" text file.

    Returns
    -------
    pathlib.PosixPath
        Path to file.

    References
    ----------
    .. [1] E.A.Abbott, ”Flatland”, Seeley & Co., 1884.
    """
    with resources.path("akshare.data", file) as f:
        data_file_path = f
        return data_file_path

def _get_file_content_ths(file: str = "ths.js") -> str:
    """
    获取 JS 文件的内容
    :param file:  JS 文件名
    :type file: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_path = get_ths_js(file)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data

def stock_fund_flow_concept(symbol):
    """
    同花顺-数据中心-资金流向-概念资金流
    http://data.10jqka.com.cn/funds/gnzjl/#refCountId=data_55f13c2c_254
    """
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "hexin-v": v_code,
        "Host": "data.10jqka.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://data.10jqka.com.cn/funds/gnzjl/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    url = (
        "http://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/ajax/1/free/1/"
    )
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    raw_page = soup.find("span", attrs={"class": "page_info"}).text
    page_num = raw_page.split("/")[1]
    if symbol == "3日排行":
        url = "http://data.10jqka.com.cn/funds/gnzjl/board/3/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "5日排行":
        url = "http://data.10jqka.com.cn/funds/gnzjl/board/5/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "10日排行":
        url = "http://data.10jqka.com.cn/funds/gnzjl/board/10/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "20日排行":
        url = "http://data.10jqka.com.cn/funds/gnzjl/board/20/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    else:
        url = "http://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(page_num) + 1)):
        js_code = py_mini_racer.MiniRacer()
        js_content = _get_file_content_ths("ths.js")
        js_code.eval(js_content)
        v_code = js_code.call("v")
        headers = {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "hexin-v": v_code,
            "Host": "data.10jqka.com.cn",
            "Pragma": "no-cache",
            "Referer": "http://data.10jqka.com.cn/funds/gnzjl/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        r = requests.get(url.format(page), headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    del big_df["序号"]
    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    if symbol == "即时":
        big_df.columns = [
            "序号",
            "行业",
            "行业指数",
            "行业-涨跌幅",
            "流入资金",
            "流出资金",
            "净额",
            "公司家数",
            "领涨股",
            "领涨股-涨跌幅",
            "当前价",
        ]
        big_df["行业-涨跌幅"] = big_df["行业-涨跌幅"].str.strip("%")
        big_df["领涨股-涨跌幅"] = big_df["领涨股-涨跌幅"].str.strip("%")
        big_df["行业-涨跌幅"] = pd.to_numeric(big_df["行业-涨跌幅"], errors="coerce")
        big_df["领涨股-涨跌幅"] = pd.to_numeric(big_df["领涨股-涨跌幅"], errors="coerce")
    else:
        big_df.columns = [
            "序号",
            "行业",
            "公司家数",
            "行业指数",
            "阶段涨跌幅",
            "流入资金",
            "流出资金",
            "净额",
        ]
    return big_df

def stock_fund_flow_industry(symbol):
    """
    同花顺-数据中心-资金流向-行业资金流
    http://data.10jqka.com.cn/funds/hyzjl/#refCountId=data_55f13c2c_254
    :param symbol: choice of {“即时”, "3日排行", "5日排行", "10日排行", "20日排行"}
    """
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "hexin-v": v_code,
        "Host": "data.10jqka.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://data.10jqka.com.cn/funds/hyzjl/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    url = (
        "http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/ajax/1/free/1/"
    )
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    raw_page = soup.find("span", attrs={"class": "page_info"}).text
    page_num = raw_page.split("/")[1]
    if symbol == "3日排行":
        url = "http://data.10jqka.com.cn/funds/hyzjl/board/3/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "5日排行":
        url = "http://data.10jqka.com.cn/funds/hyzjl/board/5/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "10日排行":
        url = "http://data.10jqka.com.cn/funds/hyzjl/board/10/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    elif symbol == "20日排行":
        url = "http://data.10jqka.com.cn/funds/hyzjl/board/20/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    else:
        url = "http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/page/{}/ajax/1/free/1/"
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(page_num) + 1)):
        js_code = py_mini_racer.MiniRacer()
        js_content = _get_file_content_ths("ths.js")
        js_code.eval(js_content)
        v_code = js_code.call("v")
        headers = {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "hexin-v": v_code,
            "Host": "data.10jqka.com.cn",
            "Pragma": "no-cache",
            "Referer": "http://data.10jqka.com.cn/funds/hyzjl/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        r = requests.get(url.format(page), headers=headers)
        temp_df = pd.read_html(r.text)[0]
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    del big_df["序号"]
    big_df.reset_index(inplace=True)
    big_df["index"] = range(1, len(big_df) + 1)
    if symbol == "即时":
        big_df.columns = [
            "序号",
            "行业",
            "行业指数",
            "行业-涨跌幅",
            "流入资金",
            "流出资金",
            "净额",
            "公司家数",
            "领涨股",
            "领涨股-涨跌幅",
            "当前价",
        ]
        big_df["行业-涨跌幅"] = big_df["行业-涨跌幅"].str.strip("%")
        big_df["领涨股-涨跌幅"] = big_df["领涨股-涨跌幅"].str.strip("%")
        big_df["行业-涨跌幅"] = pd.to_numeric(big_df["行业-涨跌幅"], errors="coerce")
        big_df["领涨股-涨跌幅"] = pd.to_numeric(big_df["领涨股-涨跌幅"], errors="coerce")
    else:
        big_df.columns = [
            "序号",
            "行业",
            "公司家数",
            "行业指数",
            "阶段涨跌幅",
            "流入资金",
            "流出资金",
            "净额",
        ]
    return big_df

def stock_zygc_ym(symbol):
    """
    益盟-F10-主营构成
    http://f10.emoney.cn/f10/zbyz/1000001
    """
    url = f"http://f10.emoney.cn/f10/zygc/{symbol}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    year_list = [
        item.text.strip()
        for item in soup.find(attrs={"class": "swlab_t"}).find_all("li")
    ]

    big_df = pd.DataFrame()
    for i, item in enumerate(year_list, 2):
        temp_df = pd.read_html(r.text, header=0)[i]
        temp_df.columns = [
            "分类方向",
            "分类",
            "营业收入",
            "营业收入-同比增长",
            "营业收入-占主营收入比",
            "营业成本",
            "营业成本-同比增长",
            "营业成本-占主营成本比",
            "毛利率",
            "毛利率-同比增长",
        ]
        temp_df["报告期"] = item
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df = big_df[
        [
            "报告期",
            "分类方向",
            "分类",
            "营业收入",
            "营业收入-同比增长",
            "营业收入-占主营收入比",
            "营业成本",
            "营业成本-同比增长",
            "营业成本-占主营成本比",
            "毛利率",
            "毛利率-同比增长",
        ]
    ]
    return big_df
