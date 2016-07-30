#!/usr/bin/env python
import sys
from urllib2 import urlopen
import os
import re
import json

reload(sys)
sys.setdefaultencoding("utf-8")


def log(str):
    print(str)


def get_url(url_base, arg_dict):
    return "%s?%s" % (url_base, "&".join(["%s=%s" % (k, str(v)) for k, v in arg_dict.items()]))


def get_data(url):
    return urlopen(url).read()


def crawler_all_fund(force=False):
    if os.path.isfile('./funds.csv') and not force:
        with open('./funds.csv', 'r') as f:
            data = [[t.strip() for t in l.decode('gbk').split(',')] for l in f.readlines()]
            titles = data[0]
            return sorted([dict(zip(titles, fund)) for fund in data[1:]], key=lambda x: x['symbol'])
    url_base = 'http://vip.stock.finance.sina.com.cn/fund_center/data/jsonp.php/IO/NetValue_Service.getNetValueOpen'
    args = {
        'page': 0,
        'num': 1000,
        'sort': "symbol",
        'asc': 0
    }
    url = get_url(url_base, args)
    data = get_data(url)

    total_num = int(re.findall("(?<=total_num:)\d*(?=,)", data)[0])
    print(total_num)
    page_size = args['num']
    page_len = (total_num + page_size - 1) / page_size
    funds = []
    for i in range(page_len):
        args['page'] = i + 1
        data = get_data(get_url(url_base, args)).decode('gbk')
        data = data.replace(',', ',"').replace('{', '{"').replace(':', '":').replace('},"', '},')
        data = re.findall("(?<=IO\(\().*(?=\)\))", data)[0]
        data = json.loads(data)
        funds += data.get('data', [])

    titles = sorted(list(set([k for l in funds for k in l])))
    print(titles)
    with open('./funds.csv', 'w') as f:
        f.write(", ".join(titles))
        f.write('\n')
        for l in funds:
            # print(", ".join(["%s = %s" % (k, v) for k, v in l.items()]))
            f.write(", ".join([unicode(l.get(k, "")).encode("gbk") for k in titles]))
            f.write('\n')
    return funds


if __name__ == '__main__':
    print("start all fund crawler.")
    crawler_all_fund(force=True)
