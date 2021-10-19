import pymysql
from get_funds_code import get_one_page
import re
import json

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