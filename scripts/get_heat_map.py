import json
import sys

class HeatMap:
    """generate heatmap geo"""
    def __init__(self, block, consume):
        self.factor = 1
        self.b = block
        self.c = consume
        self.total = []

    def change_weight(self, input_file, weight_factor, operater='+'):
        """change every weight number in GEO information"""
        with open(input_file) as fp:
            l = fp.readline().strip()
            j = json.loads(l)
            for i in j:
                count = i.get('count') / weight_factor 
                if operater=='+':
                    i['count'] = count
                else:
                    i['count'] = -count
                self.total.append(i)

    def gen_geo(self):
        """generate geo for heatmap"""
        self.change_weight(self.b, self.factor, '+')
        self.change_weight(self.c, self.factor, '-')
        jstr = json.dumps(self.total, ensure_ascii=False)
        print(jstr)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 {} block_geo consume_geo'.format(sys.argv[0]))
    else:
        hm = HeatMap(sys.argv[1], sys.argv[2])
        hm.gen_geo()

