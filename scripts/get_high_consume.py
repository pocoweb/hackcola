import sys
import json
import re

class HighConsumeGeo:
    """get high consuming block"""
    def __init__(self, input_file):
        self.json_file = input_file
        self.geo_info = []

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
        jstr = json.dumps(self.geo_info, ensure_ascii=False)
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
        hc.read_data()
        hc.make_cluster()
        hc.write_info()
        #hc.average_price()


