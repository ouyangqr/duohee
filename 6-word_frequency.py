import pdb
import jieba
import re
import csv
from collections import Counter

cut_words = []

with open("./MaFeng/10010-西塘-extract_travels.csv", 'r') as f:
    reader = csv.reader(f)
    line = ''
    for row in reader:
        line += row[2]

    line.strip('\n')
    line = re.sub("[A-Za-z0-9\：\·\—\，\。\“ \”]", "", line)
    seg_list = jieba.cut(line, cut_all=False)
    cut_words.append(" ".join(seg_list))
    print(cut_words)

line = cut_words[0]
ci_list = line.split()
c = Counter()
for x in ci_list:
    if len(x) > 1 and x != '\r\n':
        c[x] += 1

with open('ci_pin.text', 'a') as f:
    print('\n词频统计结果：')
    for (k, v) in c.most_common():  # 输出词频最高的前两个词
        f.write("%s:%d\n" % (k, v))
        # print("%s:%d" % (k, v))


"""
['央视网 消息 当地 时间 日 美国国会参议院 以票 对票 的 结果 通过 了
 一项 动议 允许 国会 在 总统 以 国家 安全 为 由 决定 征收 关税 时 发挥
 一定 的 限制 作用 这项 动议 主要 针对 加征 钢铝 关税 的 调查 目前 尚
 不 具有 约束力 动议 的 主要 发起者 共和党 参议员 鲍勃 科克 说 日 的
 投票 只是 一 小步 他会 继续 推动 进行 有 约束力 的 投票']
 """
