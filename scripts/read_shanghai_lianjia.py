import json
import sys
import re

required_keys = {
    "经度": "小区经度",
    "纬度": "小区纬度",
    "小区名称": "小区名称",
    "挂牌均价": "小区挂牌均价",
}

rent_keys = {
    "price"
}

deal_keys = {
    "单价"
}

pattern = '([0-9]+?)[^0-9]*?元.*'

with open('../shanghai/lianjia-shanghai-20170710.json') as fp:
    for k, n in required_keys.items():
        print('{},'.format(n), end='')
    print('平均租金,平均交易价')

    while True:
        line = fp.readline().strip()
        if not line:
            break
        data = json.loads(line)
        jdict = data['xiaoqu_detail']
        j = jdict.get('经度')
        w = jdict.get('纬度')
        if not j and not w:
            continue
        total = 0
        a_rent = 0
        num = 0
        rent = jdict.get('rent')
        if rent:
            for i in rent:
                price = i.get('price')
                if not price:
                    continue
                total += int(price)
                num += 1
            if num > 0:
                a_rent = total / num
        total = 0
        a_deal = 0
        num = 0
        deal = jdict.get('deal')
        if deal:
            for i in deal:
                price = i.get('挂牌单价：')
                if price:
                    match = re.match(pattern, price)
                    p = int(match.group(1))
                    total += p
                    num += 1
            if num > 0:
                a_deal = total / num
        a = jdict.get('挂牌均价')
        if a=='暂无挂牌均价' and a_rent<=0 and a_deal<=0:
            continue
        for k, name in required_keys.items():
            if k in jdict:
                if jdict.get(k) == '暂无挂牌均价':
                    jdict[k] = 0
                print('{},'.format(jdict.get(k)), end='')
        print('{},{}'.format(a_rent, a_deal))

