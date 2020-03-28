
import pdb
import pandas as pd
from setting import mafeng_name_idx

# 读取整个csv文件


def csv_distinct(path):
    csv_data = pd.read_csv(path)
    csv_data.drop_duplicates().to_csv(path, index=False, header=False)


def run():
    addr = 'MaFeng'
    for i in mafeng_name_idx:
        try:
            idx = i
            print(i)
            f1 = './{}/{}-{}-users_urls.csv'.format(addr, idx, mafeng_name_idx[idx])
            f2 = './{}/{}-{}-travels_urls.csv'.format(addr, idx, mafeng_name_idx[idx])
            csv_distinct(f1)
            csv_distinct(f2)
        except Exception:
            continue


if __name__ == "__main__":
    run()
