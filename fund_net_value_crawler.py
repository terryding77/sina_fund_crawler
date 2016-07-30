#!/usr/bin/env python
from urllib2 import urlopen
import os
import json
import argparse


def get_url(url_base, arg_dict):
    return "%s?%s" % (url_base, "&".join(["%s=%s" % (k, str(v)) for k, v in arg_dict.items()]))


def get_data(url):
    return urlopen(url).read()


def get_net_value(fund_number, begin_date='', end_date='', force=False):
    if os.path.isfile('./%s.csv' % fund_number) and not force:
        with open('./%s.csv' % fund_number, 'r') as f:
            data = [[t.strip() for t in l.split(',')] for l in f.readlines()]
            titles = data[0]
            return sorted([dict(zip(titles, net_value)) for net_value in data[1:]], key=lambda x: x['fbrq'])
    url_base = 'http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav'
    args = {
        'symbol': fund_number,
        'datefrom': begin_date,
        'dateto': end_date,
        'page': 1,
        'num': 1000
    }
    data = get_data(get_url(url_base, args))
    total_num = int(json.loads(data)['result']['data']['total_num'])
    print(total_num)
    page_size = args['num']
    page_len = (total_num + page_size - 1) / page_size
    net_values = []
    for i in range(page_len):
        args['page'] = i + 1
        data = get_data(get_url(url_base, args)).decode('gbk')
        data = json.loads(data)['result']['data']['data']
        net_values += data
    # print("\n".join([",".join(["%s=%s" % (k, v) for k, v in net_value.items()]) for net_value in net_values]))
    titles = sorted(list(set([k for l in net_values for k in l])))
    with open("./%s.csv" % fund_number, 'w') as f:
        f.write(", ".join(titles))
        f.write('\n')
        f.write('\n'.join(", ".join([str(net_value.get(k, "")) for k in titles]) for net_value in net_values))
    return net_values


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--fund_number", type=str)
    parser.add_argument("all")
    args = parser.parse_args()
    if args.all:
        from funds_crawler import crawler_all_fund
        funds = crawler_all_fund(force=True)
        for fund in funds:
            get_net_value(fund_number=fund['symbol'],force=True)
    else:
        get_net_value(args.fund_number, force=True)

