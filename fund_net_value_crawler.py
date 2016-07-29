#!/usr/bin/env python
from urllib2 import urlopen
import json

def get_url(url_base, arg_dict):
    return "%s?%s" % (url_base, "&".join(["%s=%s" % (k, str(v)) for k, v in arg_dict.items()]))


def get_data(url):
    return urlopen(url).read()


def get_net_value(fund_number, begin_date='', end_date=''):
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
        print(data)
        data = json.loads(data)['result']['data']['data']
        print(data)
        net_values += data
    print("\n".join([",".join(["%s=%s" % (k, v) for k, v in net_value.items()])for net_value in net_values]))
    titles = sorted(list(set([k for l in net_values for k in l])))
    with open("%s.csv" % fund_number, 'w') as f:
        f.write(", ".join(titles))
        f.write('\n')
        f.write('\n'.join(", ".join([str(net_value.get(k, "")) for k in titles]) for net_value in net_values))


if __name__ == "__main__":
    get_net_value('590008')
