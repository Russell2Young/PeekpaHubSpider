# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
from .items import GoodsItem


class PeekpahubspiderPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://118.24.243.44/", 27017)
        self.db = self.client["PeekpaHubTest"]
        self.collection = self.db["LingShi"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, GoodsItem):
            try:
                collection_name = self.getCollection(item['goods_brand'])
                old_item = self.db[collection_name].find_one({"goods_id": item["goods_id"]})
                if old_item is None:
                    logging.info("items: " + item['goods_id'] + " has INSERTED in " + collection_name + " db.")
                    self.db[collection_name].insert(dict(item))
                # if self.db[collection_name].find_one({"goods_id": item["goods_id"]}) is None:
                #     logging.info("items: " + item["goods_id"] + "insert in " + collection_name + "db.")
                #     self.db[collection_name].insert(dict(item))
                # 判断是否需要更新:
                elif self.needToUpdate(old_item, item):
                    self.db[collection_name].remove({'goods_id': item['goods_id']})
                    self.db[collection_name].insert(dict(item))
                    logging.info("items: " + item['goods_id'] + " has INSERTED in " + collection_name + " db.")
                else:
                    logging.info("items: " + item["goods_id"] + "has in " + collection_name + "db.")
            except Exception as e:
                logging.error("PIPLINE EXCEPTION: " + str(e))
        # self.collection.insert(dict(item))
        return item

    # 若价格发生变化,把价格变化信息写在 goods_describe 里面
    def needToUpdate(self, old_item, new_item):
        if old_item['goods_price'] != new_item['goods_price']:
            old_time = old_item['goods_time']
            old_price = float(old_item['goods_price'])
            new_price = float(new_item['goods_price'])
            minus_price = round((new_price - old_price), 2)
            logging.info("needToUpdate")
            if minus_price >= 0:
                new_item["goods_describe"] = "比" + old_time + "涨了" + str(minus_price) + "元"
            else:
                new_item["goods_describe"] = "比" + old_time + "降了" + str(minus_price) + "元"
            return True
        return False

    '''
        brand_list = 
        ['乐事', '旺旺', '三只松鼠', '卫龙', '口水娃', '奥利奥', '良品铺子', '达利园', '盼盼',
         '稻香村', '好丽友', '徐福记', '盐津铺子', '港荣', '上好佳', '百草味', '雀巢', '波力',
          '甘源牌', '喜之郎', '可比克', '康师傅', '嘉士利', '嘉华', '友臣', '来伊份', '豪士', 
          '米多奇', '闲趣', '稻香村', '', '桂发祥十八街', '趣多多', '好巴食', '北京稻香村', '法丽兹',
           '无穷', '源氏', '华美', '葡记']
        '''
    def getCollection(self, brand):
        if brand == '乐事':
            return "Leshi"
        elif brand == '旺旺':
            return "Wangwang"
        elif brand == '三只松鼠':
            return "Sanzhisongshu"
        elif brand == '卫龙':
            return "Weilong"
        elif brand == '口水娃':
            return "Koushuiwa"
        elif brand == '奥利奥':
            return "Aoliao"
        elif brand == '良品铺子':
            return "Liangpinpuzi"
        else:
            return "Linshi"
