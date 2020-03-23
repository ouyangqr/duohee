# coding=utf-8
import requests
from lxml import etree
import time
import random
import js2py
import re
import csv
from setting import User_Agent_List, mafeng_name_idx
import os


class Travels():

    def __init__(self, addr, idx, start_index):
        self.addr = addr
        self.name = mafeng_name_idx[idx]
        self.idx = idx
        self.start_index = start_index

        # 浏览器copy的headers 除去coocie 其余的保留
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.mafengwo.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }

    def analysis_fun(self, js_521, url):
        """解析521的js"""
        # print(js_521)
        js = js_521.replace("<script>", "").replace("</script>", "").replace("{eval(", "{var my_data_1 = (")
        # print(js)
        # 使用js2py的js交互功能获得刚才赋值的data1对象
        context = js2py.EvalJs()
        context.execute(js)
        js_temp = context.my_data_1
        # print(js_temp)
        index1 = js_temp.find("document.")
        index2 = js_temp.find("};if((")
        js_temp = js_temp[index1:index2].replace("document.cookie", "my_data_2")
        new_js_temp = re.sub(r'document.create.*?firstChild.href', '"{}"'.format(url), js_temp)
        # print(new_js_temp)
        context.execute(new_js_temp)
        data = context.my_data_2
        # print(data)
        __jsl_clearance = str(data).split(';')[0]
        return __jsl_clearance

    def get_521_content(self, response):
        """获取521响应的js cookies"""
        cookies = response.cookies
        cookies = '; '.join(['='.join(item) for item in cookies.items()])
        js_521 = response.text
        js_521 = ''.join(re.findall('<script>(.*?)</script>', js_521))
        return (js_521, cookies, response)

    def parse_url(self, line, url):
        '''一个发送请求，获取响应，同时etree处理html'''
        print("parsing url:", url)
        response = requests.get(url, headers=self.headers, timeout=10)  # 发送请求
        if response.status_code == 521:
            # 网站反爬虫机制 解析页面的js
            js_521, cookies, response = self.get_521_content(response)
            jsl_clearance = self.analysis_fun(js_521, url)
            self.headers['Cookie'] = jsl_clearance + ';' + cookies
        if response.status_code == 403:
            pass
        response = requests.get(url=url, headers=self.headers)
        print(response)
        html = response.content.decode()  # 获取html字符串
        self.save_html_2_file(line, html)
        html = etree.HTML(html)  # 获取element 类型的html
        return html

    def get_title(self, html):
        '''获取一个页面的title'''
        title = html.xpath('//*[@class="headtext lh80"]')[0].text
        return title

    def get_page_content(self, html):
        '''获取页面的文字数据'''
        page_content = html.xpath('string(//div[@class="view_con"])')
        page_content = ','.join(page_content.replace(' ', '').split())
        return page_content

    def get_img(self, html):
        '''获取帖子里面的所有图片'''
        img_list = html.xpath('//div[@class="add_pic _j_anchorcnt _j_seqitem"]/a/img/@data-src')
        img_list = [i.split('?image')[0] for i in img_list]
        return img_list

    def save_html_2_file(self, line, html):
        # 创建的目录
        path = "./{}/travels_htmls/{}-{}-htmls".format(self.addr, self.idx, self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        with open("./{}/travels_htmls/{}-{}-htmls/{}".format(self.addr, self.idx, self.name, line), "a") as f:
            f.write(html)

    def save_item(self, title, url, page_content, page_img):
        '''保存一篇游记信息'''
        with open("./{}/{}-{}-extract_travels.csv".format(self.addr, self.idx, self.name), "a") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([title, url, page_content, page_img])

    def run(self):
        travels = open("./{}/{}-{}-travels_urls.csv".format(self.addr, self.idx, self.name), 'r')
        i = 0
        fail_travels = []
        for line in travels:
            i += 1
            if i < self.start_index:
                continue
            try:
                if line == '\n':
                    break
                url = "http://www.mafengwo.cn" + line.replace('\n', '')
                print(url)
                html = self.parse_url(line.split('/')[-1], url)
                title = self.get_title(html)
                page_content = self.get_page_content(html)
                page_img = self.get_img(html)
                self.save_item(title, url, page_content, page_img)
            except Exception as e:
                fail_travels.append(line)
                with open("error_travels.csv", "a") as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow([line])
                print(e)
                print(line)
            finally:
                time.sleep(random.randint(8, 15))


if __name__ == "__main__":
    tieba = Travels("MaFeng", 10589, 0)
    tieba.run()
