import sys
import json

DIANPING_BLOCK_KEYS = {
    'total_price',
    'total_comments',
    'total_shop_num'
}

LIANJIA_BLOCK_KEYS = {
    'total_deal_price',
    'total_rent_price',
    'total_onsale_price',
    'total_lianjia_shop_num'
}


class GetBlockInfo:
    """get block information"""

    def __init__(self, dianping_file, lianjia_file):
        self.dianping_file = dianping_file 
        self.lianjia_file = lianjia_file
        self.block_dict = {}

    def _read_dianping_data(self):
        with open(self.dianping_file) as fp:
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
        with open(self.lianjia_file) as fp:
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
                    self.block_dict[block_index]['total_deal_price'] += float(deal_p)

                # onsale price
                sale_p = fields[5]
                if sale_p:
                    self.block_dict[block_index]['total_onsale_price'] += float(sale_p)

                # rent price
                rent_p = fields[7]
                if rent_p:
                    self.block_dict[block_index]['total_rent_price'] += float(rent_p)

                # lianjia shop number
                self.block_dict[block_index]['total_lianjia_shop_num'] += 1


    def format_block_info(self):
        self._read_dianping_data()
        self._read_lianjia_data()
        print('block_id\ttotal_price\ttotal_comments\ttotal_shop_number\ttotal_deal_price\ttotal_onsale_price\ttotal_rent_price')
        for index, body in self.block_dict.items():
            block_info_list = []
            block_info_list.append(index)
            for k in DIANPING_BLOCK_KEYS:
                if k in body:
                    block_info_list.append(str(body[k]))
                else:
                    block_info_list.append('')
            for k in LIANJIA_BLOCK_KEYS:
                if k in body:
                    block_info_list.append(str(body[k]))
                else:
                    block_info_list.append('')
            print('\t'.join(block_info_list))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 {} dianping_file, lianjia_file'.format(sys.argv[0]))
    else:
        bi = GetBlockInfo(sys.argv[1], sys.argv[2])
        bi.format_block_info()


