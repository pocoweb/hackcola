import json
import sys

class TransferCoors:
    """transfer coors among wgs84，GCJ02, BD09 formats"""
    def __init__(self, geo_file):
        """read geo information in Baidu mapv format"""
        self.geo_file = geo_file

    def _gcg02_to_wgs84(self, coors):
        """transfer coors from gcg02 to wgs84"""
        ret = []
        # Krasovsky ellipsoid
        a = 6378245.0
        # The first eccentricity square of Krasovsky ellipsoid
        ee = 0.00669342162296594323
        # PI
        PI = 3.14159265358979324
        lng = float(coors[0])
        lat = float(coors[1])
        x = lng - 105.0
        y = lat - 35.0
        # translate longitude
        dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));
        dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
        dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
        dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
        # translate latitude
        dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x));
        dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
        dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
        dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0;
        radLat = lat / 180.0 * PI
        magic = math.sin(radLat)
        magic = 1 - ee * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
        dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI);
        wgsLon = lon - dLon
        wgsLat = lat - dLat
        return wgsLon,wgsLat

    def transfer_file(self, source='gcg02', target='wgs84'):
        """read data file in Baidu mapv format and
        translate coors to target coded format"""
        with open(self.geo_file) as fp:
            for line in fp:
                jdata = json.loads(line)
                for index, item in enumerate(jdata):
                    coor_list = item['geometry']['coordinates']
                    lng, lat = self._gcg02_to_wgs84(coor_list)
                    coor_list = [str(lng), str(lat)]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 {} baidu_mapv_geo_file'.format(sys.argv[0]))
    else:
        tc = TransferCoors(sys.argv[1])
        tc.transfer_file()
