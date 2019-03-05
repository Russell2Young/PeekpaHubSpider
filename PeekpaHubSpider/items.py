# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 创建我们爬取数据最后封装的对象类
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field()  # 零食ID
    goods_title = scrapy.Field()  # 零食名称
    goods_url = scrapy.Field()  # 零食详情页url
    goods_img = scrapy.Field()  #零食图片
    goods_price = scrapy.Field()  #零食价格
    goods_shop = scrapy.Field()  # 零食店铺
    goods_icon = scrapy.Field()  # 零食优惠活动
    goods_time = scrapy.Field()  # 零食的扫描时间
    goods_brand = scrapy.Field()  # 零食品牌
    goods_describe = scrapy.Field()  # 零食描述
    # goods_title = scrapy.Field()
    # goods_title = scrapy.Field()
    # goods_title = scrapy.Field()
