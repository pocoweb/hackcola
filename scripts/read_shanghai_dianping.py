import json
import sys
import re

required_keys = {
        "cityCnName": "城市名称",
        "county": "县区名称",
        "fullName": "店铺名称",
        "categoryName": "类别名称",
        "address": "地址",
        "cityGlng": "城市经度",
        "cityGlat": "城市纬度",
        "shopGlng": "店铺经度",
        "shopGlat": "店铺纬度",
        "average_price": "人均消费",
        "review_count": "评论数"
}

pattern = '人均：[^0-9]*?([0-9]+?)[^0-9]*?元.*'

with open('../shanghai/dianping-shanghai-shops-20180121-new.json') as fp:
    for k, name in required_keys.items():
        print('{},'.format(name), end='')
    print('\n', end='')
    while True:
        line = fp.readline().strip()
        if not line:
            break
        jdict = json.loads(line)
        a = jdict.get('average_price')
        if not a:
            continue
        r = re.match(pattern, a)
        if not r:
            continue
        price = int(r.group(1))
        jdict['average_price'] = price
        for key in required_keys:
            print('{},'.format(jdict.get(key)), end='')
        print('\n', end='')
