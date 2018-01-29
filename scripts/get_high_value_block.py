import sys
import json


class HighValueGeos:
    """get high value blocks' GEO information"""

    def __init__(self, input_file):
        """initial values"""
        self.fcsv = input_file
        self.geo_infor = []
        self.weight_dict = {
            '0': 1,
            '1': 500,
            '2': 10
        }

    def read_data(self):
        """read GEO information of high-value blocks"""
        with open(self.fcsv) as fp:
            for line in fp:
                line = line.strip()
                if not line or len(line) == 0:
                    continue
                fields = line.split(',')
                if not fields[7].isdigit():
                    continue
                lng = fields[0]
                lat = fields[1]
                cluster = fields[7]
                self.geo_infor.append(
                    {
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [lng, lat]
                        },
                        'count': self.weight_dict[cluster]
                    })

    def write_data(self):
        if not self.geo_infor:
            return
        j = json.dumps(self.geo_infor, ensure_ascii=False)
        print(j)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 {} input_file'.format(sys.argv[0]))
    else:
        hv = HighValueGeos(sys.argv[1])
        hv.read_data()
        hv.write_data()
