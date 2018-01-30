import json
import sys
import re
from transfer_coors import TransferCoors

REQUIRED_KEYS = {
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
    "review_count": "评论数",
    'navi': 'navi',
    'comment_list': 'commenct_list',
    'mainCategoryName': 'main_category',
    'comment_score_list': 'comment_score_list',
    'power': 'power',
    'shopPower': 'shop_power'
}

ADDITION_KEYS = {
    'gpsshopglng': 'GPS坐标经度',
    'gpsshopglat': 'GPS坐标纬度',
    'bdshopglng': 'Baidu坐标经度',
    'bdshopglat': 'Baidu坐标纬度',
    'shopPower': '店铺能力',
    'power': '能力',
    'manaScore': '魔法值',
    'voteTotal': '投票数',
    'taste': '口味',
    'env': '环境',
    'service': '服务',
    'shopId': '店铺ID',
    'blockId': '区块ID'
}

CONSUME_PRICE_PATTERN = '人[^0-9]*?([0-9]+?)[^0-9]*?元.*'


class ReadDianping:
    """read dianping data"""

    def __init__(self, data_file):
        """initial variables"""
        # center of shanghai (government), 
        # in google earth coordinates
        self.shanghai_center = ['121.4692482700', '31.2323498200']
        self.data_file = data_file
        self.res = []
        self.enrich_fields = []

    def _check_keys(self, jdata):
        """check if the required keys exists"""
        for k in REQUIRED_KEYS.keys():
            if k not in jdata:
                return False
        return True

    def _read_file(self):
        """read the dianping data"""
        with open(self.data_file) as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                jdata = json.loads(line)
                a = jdata.get('average_price')
                if not a:
                    continue
                r = re.match(CONSUME_PRICE_PATTERN, a)
                if not r:
                    continue
                price = r.group(1)
                jdata['average_price'] = price
                r_count = jdata.get('review_count')
                g = re.match('([0-9]+)[^0-9]*', r_count)
                if g:
                    jdata['review_count'] = g.group(1)
                else:
                    jdata['review_count'] = ''
                fields = []
                for key in REQUIRED_KEYS:
                    if key in jdata:
                        value = jdata[key]
                        if type(value) is list:
                            if key == 'navi':
                                value = [i['text'].replace('\t', ' ') for i in value]
                            elif key == 'comment_list':
                                value = [i['content'].replace('\t', ' ') for i in value]
                            fields.append(','.join(value))
                        else:
                            fields.append(jdata[key])
                self.res.append(fields)

    def gen_csv_file(self, separator='\t'):
        """generate csv file"""
        self._read_file()
        l = []
        for k, name in REQUIRED_KEYS.items():
            l.append(k)
        s = separator.join(l)
        print(s)
        if not self.res:
            return
        for sub_list in self.res:
            s = separator.join(sub_list)
            print(s)

    def _get_block_id(self, lng, lat):
        """classify the shops by 1km*1km grip"""
        clng = float(self.shanghai_center[0])
        clat = float(self.shanghai_center[1])
        diff_lng = lng - clng
        diff_lat = lat - clat
        lng_index = int(int(1000*diff_lng)/11)
        lat_index = int(int(1000*diff_lat)/9)
        return '{}_{}'.format(lng_index, lat_index)

    def tag_shops(self, transfer_coors=False):
        """tag every shops"""
        name_list = []
        for key, name in REQUIRED_KEYS.items():
            name_list.append(name)
        for key, name in ADDITION_KEYS.items():
            name_list.append(name)
        s = '\t'.join(name_list)
        print(s)
        with open(self.data_file) as fp:
            for line in fp:
                line = line.strip()
                jdata = json.loads(line)

                ret = self._check_keys(jdata)
                if not ret:
                    continue
                a = jdata.get('average_price')
                r = re.match(CONSUME_PRICE_PATTERN, a)
                if r:
                    jdata['average_price'] = r.group(1)
                else:
                    jdata['average_price'] = ''
                r_count = jdata.get('review_count')
                g = re.match('([0-9]+)[^0-9]*', r_count)
                if g:
                    jdata['review_count'] = g.group(1)
                else:
                    jdata['review_count'] = ''
                if transfer_coors:
                    lng = jdata['shopGlng']
                    lat = jdata['shopGlat']
                    tc = TransferCoors()
                    glng, glat = tc.gcj02_to_wgs84(float(lng), float(lat))
                    jdata['gpsshopglng'] = str(glng)
                    jdata['gpsshopglat'] = str(glat)
                    block_id = self._get_block_id(float(lng), float(lat))
                    blng, blat = tc.gcj02_to_bd09(float(lng), float(lat))
                    jdata['bdshopglng'] = str(blng)
                    jdata['bdshopglat'] = str(blat)
                else:
                    jdata['gpsshopglng'] = ''
                    jdata['gpsshopglat'] = ''
                    block_id = ''
                    jdata['bdshopglng'] = ''
                    jdata['bdshopglat'] = ''
                fields = []
                for key in REQUIRED_KEYS:
                    fields.append(jdata.get(key))
                fields.append(jdata.get('gpsshopglng'))
                fields.append(jdata.get('gpsshopglat'))
                fields.append(jdata.get('bdshopglng'))
                fields.append(jdata.get('bdshopglat'))
                fields.append(jdata.get('shopPower'))
                fields.append(jdata.get('power'))
                fields.append(jdata.get('manaScore'))
                fields.append(jdata.get('voteTotal'))
                c_score_list = jdata.get('comment_score_list')
                if c_score_list:
                    for c in c_score_list:
                        score = c.split('：')[1]
                        fields.append(score)
                fields.append(jdata.get('shopId'))
                fields.append(block_id)
                for i, f in enumerate(fields):
                    if not f:
                        fields[i] = ''
                self.enrich_fields = fields
                s = '\t'.join(fields)
                print(s)


if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage: python3 {} data_file [transfer_coors=False]'.format(sys.argv[0]))
    else:
        rd = ReadDianping(sys.argv[1])
        rd.gen_csv_file()

