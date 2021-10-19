import pymysql
import requests
import re
import json

def get_one_page(fundcode, pageIndex=1):
    '''
    获取基金净值某一页的html
    :param fundcode: str格式，基金代码
    :param pageIndex: int格式，页码数
    :return: str格式，获取网页内容
    '''
    url = 'http://api.fund.eastmoney.com/f10/lsjz'
    cookie = 'EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=01-24 17:11:50@#$%u957F%u4FE1%u5229%u5E7F%u6DF7%u5408A@%23%24519961; st_pvi=27838598767214; st_si=11887649835514'
    headers = {
        'Cookie': cookie,
        'Host': 'api.fund.eastmoney.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'http://fundf10.eastmoney.com/jjjz_%s.html' % fundcode,
    }
    params = {
        'callback': 'jQuery18307633215694564663_1548321266367',
        'fundCode': fundcode,
        'pageIndex': pageIndex,
        'pageSize': 1,
    }
    try:
        r = requests.get(url=url, headers=headers, params=params)
        if r.status_code == 200:
            return r.text
        return None
    except Exception:
        return None

def main():
    path = './基金代码爬取/fundcode.csv'
    with open(path,mode='r') as f:
        code = []
        data = f.readlines()
        # print(data)
        for d in data:
            code.append(d.strip().split(','))
    codes = code[1:]
    # print(codes)
     # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root", password="12345678", database="stock_db", charset="utf8")
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()
    sql = "INSERT INTO stock_db.fund_info (code, name, type, dwjz, ljjz, jzzzl, time) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    try:
        for i in range(1081,1082):
            html = get_one_page(codes[i][0],1)
            content = re.findall('\((.*?)\)', html)[0]
            lsjz_list = json.loads(content)['Data']['LSJZList']
            if lsjz_list:
                jtime = lsjz_list[0]["FSRQ"]  # 时间
                DWJZ = lsjz_list[0]["DWJZ"] # 单位净值
                LJJZ = lsjz_list[0]["LJJZ"] # 累计净值
                JZZZL = lsjz_list[0]["JZZZL"] # 涨跌幅
                FundType = json.loads(content)['Data']['FundType']
                print("基金代码：%s，基金名称：%s, 基金类型：%s,单位净值：%s，累计净值：%s，涨跌幅：%s, 更新时间：%s" % (codes[i][0], codes[i][1], FundType, DWJZ, LJJZ, JZZZL,jtime))
                cursor.execute(sql, (codes[i][0], codes[i][1], FundType, DWJZ, LJJZ, JZZZL,jtime,))
                conn.commit()  # 提交事物
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()