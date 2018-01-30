import sys
import json

DINANPING_BLOCK_KEYS = {
    'total_price',
    'total_comments',
    'total_shop_num'
}

LIANJIA_BLOCK_KEYS = {
    'total_deal_price',
    'total_rent_price',
    'total_onsale_price',
}


class GetBlockInfo:
    """get block information"""

    def __init__(self, data_file):
        self.data_file = data_file
        self.block_dict = {}

    def _read_dianping_data(self):
        with open(self.data_file) as fp:
            for line in fp:
                line = line.strip()
                fields = line.split('\t')
                if fields[0] == '城市名称':
                    continue
                if len(fields) != 24:
                    continue
                block_index = fields[23]
                if block_index not in self.block_dict:
                    self.block_dict[block_index] = {}

                for k in DIANPING_BLOCK_KEYS:
                    if k not in self.block_dict[block_index]:
                        self.block_dict[block_index][k] = 0

                # average consume price
                price = fields[9]
                if price:
                    self.block_dict[block_index]['total_price'] += int(price)
                # comment number
                c_num = fields[10]
                if c_num:
                    self.block_dict[block_index]['total_comments'] += int(
                        c_num)
                # total shop number
                self.block_dict[block_index]['total_shop_num'] += 1

    def _read_lianjia_data(self):
        with open(self.data_file) as fp:
            for line in fp:
                line = line.strip()
                fields = line.split('\t')
                if fields[0] == '小区经度':
                    continue
                block_index = fields[6]
                if block_index not in self.block_dict:
                    self.block_dict[block_index] = {}

                for k in LIANJIA_BLOCK_KEYS:
                    if k not in self.block_dict[block_index]:
                        self.block_dict[block_index][k] = 0

                # deal price
                deal_p = fields[8]
                if deal_p:
                    self.block_dict[block_index]['total_deal_price'] += int(deal_p)

                # onsale price
                # TODO: calculate every keys...

    def format_dianping_block_info(self):
        self._read_dianping_data()
        print('block_id\ttotal_price\ttotal_comments\ttotal_shop_number')
        for index, body in self.block_dict.items():
            block_info_list = []
            block_info_list.append(index)
            for k in DIANPING_BLOCK_KEYS:
                block_info_list.append(str(body[k]))
            print('\t'.join(block_info_list))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 {} data_file [dianping | lianjia]'.format(sys.argv[0]))
    else:
        bi = GetBlockInfo(sys.argv[1])
        if sys.argv[2] == 'dianping':
            bi.format_dianping_block_info()
        elif sys.argv[2] == 'lianjia':
            bi.format_lianjia_block_info()
        else:
            print('Usage: python3 {} data_file [dianping | lianjia]'.format(sys.argv[0]))


