import json
import sys
import math


class TransferCoors:
    """transfer coors among wgs84，GCJ02, BD09 formats"""

    def __init__(self):
        self.PI = 3.14159265358979324

    def gcj02_to_wgs84(self, lng, lat):
        """transfer coors from gcg02 to wgs84"""
        ret = []
        # Krasovsky ellipsoid
        a = 6378245.0
        # The first eccentricity square of Krasovsky ellipsoid
        ee = 0.00669342162296594323

        # prepare for calculate
        x = lng - 105.0
        y = lat - 35.0

        # translate longitude
        dlon = 300.0 + x + 2.0 * y + 0.1 * x * x + \
            0.1 * x * y + 0.1 * math.sqrt(abs(x))
        dlon += (20.0 * math.sin(6.0 * x * self.PI) + 20.0 *
                 math.sin(2.0 * x * self.PI)) * 2.0 / 3.0
        dlon += (20.0 * math.sin(x * self.PI) + 40.0 *
                 math.sin(x / 3.0 * self.PI)) * 2.0 / 3.0
        dlon += (150.0 * math.sin(x / 12.0 * self.PI) + 300.0 *
                 math.sin(x / 30.0 * self.PI)) * 2.0 / 3.0

        # translate latitude
        dlat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * \
            y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        dlat += (20.0 * math.sin(6.0 * x * self.PI) + 20.0 *
                 math.sin(2.0 * x * self.PI)) * 2.0 / 3.0
        dlat += (20.0 * math.sin(y * self.PI) + 40.0 *
                 math.sin(y / 3.0 * self.PI)) * 2.0 / 3.0
        dlat += (160.0 * math.sin(y / 12.0 * self.PI) + 320 *
                 math.sin(y * self.PI / 30.0)) * 2.0 / 3.0
        radlat = lat / 180.0 * self.PI
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) *self.PI)
        dlon = (dlon * 180.0) / (a / sqrtmagic * math.cos(radlat) * self.PI)
        wgslon = lng - dlon
        wgslat = lat - dlat
        return wgslon, wgslat

    def gcj02_to_bd09(self, lng, lat):
        # x PI
        x_pi = self.PI * 3000.0 / 180.0 
        x = lng
        y = lat
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return bd_lng, bd_lat


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 {} baidu_mapv_geo_file'.format(sys.argv[0]))
    else:
        tc = TransferCoors(sys.argv[1])
        print(tc.gcg02_to_wgs84())
