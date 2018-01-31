import sys
import json
import re
import pandas as pd
import numpy

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

dist_df_cols = [
    'drv_spicy_food',
    'drv_fast_food',
    'drv_snack',
    'drv_coffee',
    'drv_formal_food',
    'drv_score<7',
    'drv_score>8',
    'drv_score>=7<=8',
    'drv_shop_power_small',
    'drv_shop_power_medium',
    'drv_shop_power_large'
]

def get_score(s):
    if pd.isnull(s):
        return s
    f = re.findall("\d+\.\d+", s)
    if len(f) is not 0:
        return f[0]
    return None

class HighConsumeGeo:
    """get high consuming block"""
    def __init__(self, input_file):
        self.json_file = input_file
        self.geo_info = []

    def read_data_in_csv(self, separator='\t'):
        df = pd.read_csv(self.json_file, sep=separator)
        dim = pd.read_excel('./dianping_cat_rank.xlsx')
        # merge 'drv_spicy_food', 'dinner_type'
        df = pd.merge(df, dim, on='mainCategoryName', how='left')
        df['drv_fast_food'] = df['dinner_type'].apply(lambda x: x=='快餐' and 1 or 0)
        df['drv_snack'] = df['dinner_type'].apply(lambda x: x=='小吃' and 1 or 0)
        df['drv_coffee'] = df['dinner_type'].apply(lambda x: x=='咖啡厅' and 1 or 0)
        df['drv_formal_food'] = df['dinner_type'].apply(lambda x: x in ['中餐', '烧烤', '料理', '西餐', '海鲜', '自助餐', '火锅'] and 1 or 0)

        # scoring
        df['taste_score'] = df['comment_score_list'].str.split(',').str.get(0).apply(lambda x: get_score(x)).astype(float)
        df['env_score'] = df['comment_score_list'].str.split(',').str.get(1).apply(lambda x: get_score(x)).astype(float)
        df['service_score'] = df['comment_score_list'].str.split(',').str.get(2).apply(lambda x: get_score(x)).astype(float)
        df['overall_score'] = (df['taste_score'] + df['env_score'] + df['service_score'])/3
        df['drv_score<7'] = 0
        df['drv_score>=7<=8'] = 0
        df['drv_score>8'] = 0
        lesser = df['overall_score'] < 7
        greater = df['overall_score'] > 8
        df.loc[lesser, 'drv_score<7'] = 1
        df.loc[greater, 'drv_score>8'] = 1
        df.loc[ ~lesser & ~greater, 'drv_score>=7<=8'] = 1

        df['drv_shop_power_small'] = 0
        df['drv_shop_power_medium'] = 0
        df['drv_shop_power_large'] = 0
        small = df['shopPower'] <= 30
        large = df['shopPower'] >= 40
        df.loc[small, 'drv_shop_power_small'] = 1
        df.loc[~small & ~large, 'drv_shop_power_medium'] = 1
        df.loc[large, 'drv_shop_power_large'] = 1
        df = df.fillna(0)
        for i in df.index:
            info = df.loc[i, dist_df_cols].to_dict()
            info.update({
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        df.loc[i, 'shopGlng'],
                        df.loc[i, 'shopGlat'],
                    ]
                },
                'count': df.loc[i, 'average_price']
            })
            self.geo_info.append(info)


    def read_data(self):
        """read data from shanghai dianping data"""
        with open(self.json_file) as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                jdata = json.loads(line)
                shopglat = jdata.get('shopGlat')
                shopglng = jdata.get('shopGlng')
                ap = jdata.get('average_price')
                m = re.match('[^0-9]*?([0-9]+)[^0-9]*', ap)
                if m:
                    p = int(m.group(1))
                    self.geo_info.append(
                        {
                            'geometry': {
                                'type': 'Point',
                                'coordinates': [shopglng, shopglat]
                            },
                            'count': p
                        })

    def average_price(self):
        """calculate avaerage price"""
        s = 0
        for i in self.geo_info:
            s += i.get('count')
        return s / len(self.geo_info)

    def write_info(self):
        """write geo info"""
        if not self.geo_info:
            return
        jstr = json.dumps(self.geo_info, ensure_ascii=False, cls=MyEncoder)
        print(jstr)

    def make_cluster(self):
        """put price in cluster"""
        for k,v in enumerate(self.geo_info):
            p = v.get('count')
            if p < 100:
                self.geo_info[k]['count'] = 1
            elif p >= 100 and p < 500:
                self.geo_info[k]['count'] = 5
            elif p >= 500 and p < 1000:
                self.geo_info[k]['count'] = 50
            else:
                self.geo_info[k]['count'] = 100


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 {} input_file'.format(sys.argv[0]))
    else:
        hc = HighConsumeGeo(sys.argv[1])
        # hc.read_data()
        hc.read_data_in_csv()
        hc.make_cluster()
        hc.write_info()
        #hc.average_price()


