# coding=utf-8
# author=zhangjingyuan
# python3
from lxml import etree
import re
import requests
import js2py
import csv
import time
import random
from setting import User_Agent_List, mafeng_name_idx


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.mafengwo.cn',
    'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': random.choice(User_Agent_List)
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'
}


def get_521_content(url):
    req = requests.get(url=url, headers=headers)
    print(req)
    cookies = req.cookies
    cookies = '; '.join(['='.join(item) for item in cookies.items()])
    txt_521 = req.text
    txt_521 = ''.join(re.findall('<script>(.*?)</script>', txt_521))
    return (txt_521, cookies, req)


def fixed_fun(js_html, url):
    js = js_html.replace("<script>", "").replace("</script>", "").replace("{eval(", "{var my_data_1 = (")
    # print(js)
    # 使用js2py的js交互功能获得刚才赋值的data1对象
    context = js2py.EvalJs()
    context.execute(js)
    js_temp = context.my_data_1
    index1 = js_temp.find("document.")
    index2 = js_temp.find("};if((")
    js_temp = js_temp[index1:index2].replace("document.cookie", "my_data_2")
    new_js_temp = re.sub(r'document.create.*?firstChild.href', '"{}"'.format(url), js_temp)
    context.execute(new_js_temp)
    data = context.my_data_2
    __jsl_clearance = str(data).split(';')[0]
    return __jsl_clearance


def get_user_content(url):
    txt_521, cookies, req = get_521_content(url)
    if req.status_code == 521:
        __jsl_clearance = fixed_fun(txt_521, url)
        headers['Cookie'] = __jsl_clearance + ';' + cookies
        headers['Referer'] = url
        res1 = requests.get(url=url, headers=headers)
    else:
        res1 = req
    print(res1)

    return res1


def save_need(html, addr, idx, name):
    if html.xpath('//div[@class="MAvatar"]/div[@class="MAvaName"]/i/@class'):
        gender_res = html.xpath('//div[@class="MAvatar"]/div[@class="MAvaName"]/i/@class')[0]
    else:
        gender_res = '未知'
    if gender_res == 'MGenderFemale':
        gender = '女'
    elif gender_res == 'MGenderMale':
        gender = '男'
    else:
        gender = '未知'
    if html.xpath('//span[@class="MAvaPlace flt1"]/@title'):
        addr_res = html.xpath('//span[@class="MAvaPlace flt1"]/@title')[0]
    else:
        addr_res = 'None'
    if html.xpath('//div[@class="MAvaName"]')[0]:
        username = html.xpath('//div[@class="MAvaName"]')[0].text.replace(' ', '').replace('\n', '')
    else:
        username = 'None'

    with open("./{}/{}-{}-extract_users.csv".format(addr, idx, name), "a") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([username, gender, addr_res])


def run(addr, idx):
    name = mafeng_name_idx[idx]
    users = open("./{}/{}-{}-users_urls.csv".format(addr, idx, name), 'r')
    fail_users = []

    for user in users:
        try:
            url = "http://www.mafengwo.cn" + user.replace('\n', '')
            print(url)
            response = get_user_content(url)
            html = response.content.decode()

            # with open("./users_htmls/{}".format(user.split('/')[-1]), "a") as f:
            #     f.write(html)
            html = etree.HTML(html)
            save_need(html,  addr, idx, name)
        except Exception as e:
            fail_users.append(user)
            with open("error_users.csv", "a") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([user])
            print(e)
            print(user)
        finally:
            time.sleep(random.randint(8, 15))
    return True


if __name__ == "__main__":
    # for i in mafeng_name_idx:
    idx = 10589
    addr = 'MaFeng'
    # idx = 10547
    # if idx in [10547, 10024]:
    #     continue
    print(idx)
    status = run(addr, idx)

    if status:
        idx = 10825
        status = run(addr, idx)
        if status:
            idx = 11729
            status = run(addr, idx)
            if status:
                idx = 186782
                status = run(addr, idx)
