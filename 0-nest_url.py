# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import re
import time
import io
import gzip
import random
import csv
from setting import User_Agent_List, mafeng_name_idx
from lxml import etree


headerS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'mfw_uuid=5c84cb93-758a-762e-0127-ea70f6cb3e64; _r=bing; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A12%3A%22cn.bing.com%2F%22%3Bs%3A1%3A%22t%22%3Bi%3A1552206739%3B%7D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A20%3A%22https%3A%2F%2Fcn.bing.com%2F%22%3Bs%3A2%3A%22hp%22%3Bs%3A11%3A%22cn.bing.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-03-10+16%3A32%3A19%22%3B%7D; __mfwlv=1552358747; __mfwvn=3; __mfwlt=1552363839; uva=s%3A144%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222019-03-10%22%3Bs%3A2%3A%22lt%22%3Bi%3A1552206739%3Bs%3A10%3A%22last_refer%22%3Bs%3A20%3A%22https%3A%2F%2Fcn.bing.com%2F%22%3Bs%3A5%3A%22rhost%22%3Bs%3A11%3A%22cn.bing.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1552206739%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A11%3A%22cn.bing.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5c84cb93-758a-762e-0127-ea70f6cb3e64; UM_distinctid=16966bb483d45-0f494e03ad41f4-4c312f7f-144000-16966bb483e2ab; CNZZDATA30065558=cnzz_eid%3D1199525799-1552206059-null%26ntime%3D1552353780; PHPSESSID=madinq41vdjrvfvsk97bhp7cf0; all_ad=1',
    'Host': 'www.mafengwo.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(User_Agent_List)
}


def create_travels_users(addr, idx, min, max):
    # 1. 创建文件对象
    f1 = open('./{}/{}-{}-users_urls.csv'.format(addr, idx, mafeng_name_idx[idx]), 'a', encoding='utf-8')
    f2 = open('./{}/{}-{}-travels_urls.csv'.format(addr, idx, mafeng_name_idx[idx]), 'a', encoding='utf-8')

    # 2. 基于文件对象构建 csv写入对象
    csv_writer1 = csv.writer(f1)
    csv_writer2 = csv.writer(f2)

    for i in range(min, max):
        try:
            url = "http://www.mafengwo.cn/yj/{}/2-0-".format(idx) + str(i) + ".html"
            request = urllib.request.Request(url, data=None, headers=headerS)
            response = urllib.request.urlopen(request)
            page = response.read()
            iopage = io.BytesIO(page)  # 存入内存中
            depage = gzip.GzipFile(fileobj=iopage, mode="rb")  # 打开一个压缩文件
            html = depage.read().decode('utf-8')  # gzip解压缩
            # 比较时间
            xhtml = etree.HTML(html)
            create_time = xhtml.xpath('//span[@class="comment-date"]')[0].text
            # new_time = datetime.datetime.now().strftime('%Y-%m-%d')
            need_time = "2019-01-01"
            print(i)
            print(create_time)
            if create_time < need_time:
                break
            user_url = xhtml.xpath('//span[@class="author"]/a[1]/@href')  # 用户地址
            travel_url = xhtml.xpath('//a[@class="title-link"]/@href')  # 游记地址 查找其中形如/i/…….html的链接

            print(user_url)
            print(travel_url)
            for user in user_url:
                csv_writer1.writerow([user])
            for travel in travel_url:
                csv_writer2.writerow([travel])

            time.sleep(random.randint(4, 7))
            # time.sleep(random.random())
        except Exception as e:
            print('因错误结束', e)
        finally:
            pass

    # 5. 关闭文件
    f1.close()
    f2.close()


if __name__ == "__main__":
    create_travels_users('MaFeng', 19288, 1, 500)
