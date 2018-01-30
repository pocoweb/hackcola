import json
import sys
import re
from transfer_coors import TransferCoors

required_keys = {
    "经度": "小区经度",
    "纬度": "小区纬度",
    "gpslng": "GPS经度",
    "gpslat": "GPS纬度",
    "小区名称": "小区名称",
    "挂牌均价": "小区挂牌均价",
    "block_id": "区块ID"
}

rent_keys = {
    "price"
}

deal_keys = {
    "单价"
}

pattern = '([0-9]+?)[^0-9]*?元.*'
shanghai_center = ['121.4692482700', '31.2323498200']

with open('../shanghai/lianjia-shanghai-20170710.json') as fp:
    for k, n in required_keys.items():
        print('{}\t'.format(n), end='')
    print('平均租金\t平均交易价')

    while True:
        line = fp.readline().strip()
        if not line:
            break
        data = json.loads(line)
        jdict = data['xiaoqu_detail']
        j = jdict.get('经度')
        w = jdict.get('纬度')
        if not j or not w:
            continue
        tc = TransferCoors()
        glng, glat = tc.gcj02_to_wgs84(float(j), float(w))
        jdict['gpslng'] = str(glng)
        jdict['gpslat'] = str(glat)
        clng = float(shanghai_center[0])
        clat = float(shanghai_center[1])
        diff_lng = glng - clng
        diff_lat = glat - clat
        lng_index = int(int(1000*diff_lng)/11)
        lat_index = int(int(1000*diff_lat)/9)
        b_id = '{}_{}'.format(lng_index, lat_index)
        jdict['block_id'] = b_id
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
                #print('{},'.format(jdict.get(k)), end='')
                print('{}\t'.format(jdict.get(k)), end='')
        #print('{},{}'.format(a_rent, a_deal))
        print('{}\t{}'.format(a_rent, a_deal))

