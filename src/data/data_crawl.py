import requests
import json
from pymysql import connect
from threading import Thread, Lock
from time import sleep


class PureFinance(object):
    def __init__(self, code, rate_limit=1):
        self.code = code
        self.rate_limit = rate_limit
        self.conn = connect(host='localhost', port=3306, database='financedb', user='root', password='mysql')
        self.lock = Lock()

        print("开始初始化数据库表，删除该基金下错误数据...")
        cur = self.conn.cursor()
        sql_str = "DELETE FROM fund WHERE fundname=%s;"
        row_count = cur.execute(sql_str, [self.code])
        print("表中受影响行数为 {}".format(row_count))
        self.conn.commit()
        cur.close()

    def fetch_data(self, page):
        url = "http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18304038998523093684_1586160530315"
        temp_url = f"{url}&fundCode={self.code}&pageIndex={page}&pageSize=20"
        header = {"Referer": f"http://fundf10.eastmoney.com/jjjz_{self.code}.html"}

        jsonData = requests.get(temp_url, headers=header).content.decode()
        dictData = json.loads(jsonData[41:-1])
        return dictData

    def process_page(self, page):
        dictData = self.fetch_data(page)
        listData = dictData.get("Data", {"LSJZList": []}).get("LSJZList")
        tmpList = []

        for item in listData:
            npvDate = item.get("FSRQ")
            npv = item.get("DWJZ")
            tempRate = item.get("JZZZL")
            rate = "0.00" if tempRate == "" else tempRate
            tmpList.append((self.code, str(npvDate), str(npv), str(rate)))

        with self.lock:
            cur = self.conn.cursor()
            sql = "INSERT INTO fund (fundname, funddate, NPV, rate) VALUES (%s, %s, %s, %s);"
            cur.executemany(sql, tmpList)
            self.conn.commit()
            cur.close()

        sleep(1 / self.rate_limit)

    def getNPV(self):
        dictData = self.fetch_data(1)
        totalCount = dictData.get("TotalCount", 0)
        pageTotal = (totalCount + 19) // 20
        print("总页数为 {}".format(pageTotal))

        threads = []
        for page in range(1, pageTotal + 1):
            thread = Thread(target=self.process_page, args=(page,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return {"message": "ok", "status": 200}

    def close(self):
        self.conn.close()


# 使用方式
fund = PureFinance('970196', rate_limit=6)
mes = fund.getNPV()
fund.close()
print(mes)
