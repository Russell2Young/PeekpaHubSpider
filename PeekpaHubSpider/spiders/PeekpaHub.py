# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy import Request
from bs4 import BeautifulSoup
from ..items import GoodsItem
from ..settings import MAX_PAGE_NUM, START_URL


class PeekpahubSpider(scrapy.Spider):
    name = 'PeekpaHub'
    allowed_domains = ['search.jd.com']
    start_urls = START_URL
    max_page = MAX_PAGE_NUM
    # allowed_domains = ['peekpahub.com']
    # start_urls = ['http://peekpahub.com/']
    # start_urls = ['https://search.jd.com/Search?keyword=%E9%9B%B6%E9%A3%9F&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=lingshi&stock=1&click=0&page=1']


    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content, "html.parser")
        # print(content)
        # brand_temp_list = soup.find_all('a', attrs={"onclick": re.compile(r"searchlog(\w+)")})

        # 品牌列表获取
        brand_temp_list = soup.find_all('li', attrs={"id": re.compile(r"brand-(\w+)")})
        brand_size = len(brand_temp_list)
        # print("total find: " + str(brand_size))
        # print(brand_temp_list)
        brand_list = list()
        for item in brand_temp_list:
            brand_title = item.find('a')['title']
            # brand_list.append(brand_title)
            brand_list.append(re.sub("[A-Za-z0-9\!\%\[\]\,\。\(\)\（\）\"\.\'\ ]", "", brand_title))
        # print(brand_list)

        # 最外层的所有零食信息列表
        goods_temp_list = soup.find_all('li', attrs={'class': 'gl-item'})

        for item in goods_temp_list:
            goods = GoodsItem()

            # 获取零食ID
            goods_id = item['data-sku']

            # 获取零食名字
            temp_div_title_list = item.find_all('div', attrs={'class': 'p-name'})
            temp_em_title_list = temp_div_title_list[0].find('em')
            goods_title = temp_em_title_list.text
            # print(goods_title)

            # 零食的图片和详情页URL
            temp_div_url_img_list = item.find_all('div', attrs={'class': 'p-img'})
            # goods_url = temp_div_url_img_list[0].find('a')['href']
            # temp_img = temp_div_url_img_list[0].find('img')
            # # print(temp_img)
            # goods_img = temp_img['source-data-lazy-img']
            # print(goods_img)
            goods_url = temp_div_url_img_list[0].find('a')['href'] if "http" in temp_div_url_img_list[0].find('a')['href'] else "http://" + temp_div_url_img_list[0].find('a')['href'][2:]
            goods_img = "http://" + temp_div_url_img_list[0].find('img')['source-data-lazy-img'][2:]

            # 零食的价格
            temp_div_price_list = item.find_all('div', attrs={'class': 'p-price'})
            goods_price = temp_div_price_list[0].find('i').text
            # print(goods_price)

            # 零食的店铺
            temp_div_shop_list = item.find_all('div', attrs={'class': 'p-shop'})
            temp_shop_list = temp_div_shop_list[0].find('a')
            goods_shop = "" if temp_shop_list is None else temp_shop_list.text

            # 零食的优惠
            temp_div_icon_list = item.find_all('div', attrs={'class': 'p-icons'})
            temp_icon_list = temp_div_icon_list[0].find_all('i')
            goods_icon = ""
            for icon in  temp_icon_list:
                goods_icon = goods_icon + "/" + icon.text

            # 零食的品牌
            goods_brand = self.getGoodsBrand(goods_title, brand_list)

            # 零食的扫描时间
            cur_time = datetime.datetime.now()
            cur_year = str(cur_time.year)
            cur_month = str(cur_time.month) if len(str(cur_time.month)) == 2 else "0" + str(cur_time.month)  # TODO
            cur_day = str(cur_time.day) if len(str(cur_time.day)) == 2 else "0" + str(cur_time.day)
            goods_time = cur_year + '_' + cur_month + '_' + cur_day

            goods_describe = ""

            # 大整合:将所有的信息放到之前创建的GoodsItem里面
            goods['goods_id'] = goods_id
            goods['goods_title'] = goods_title
            goods['goods_url'] = goods_url
            goods['goods_img'] = goods_img
            goods['goods_price'] = goods_price
            goods['goods_shop'] = goods_shop
            goods['goods_icon'] = goods_icon
            goods['goods_time'] = goods_time
            goods['goods_brand'] = goods_brand
            goods['goods_describe'] = ""
            yield goods

        cur_page_num = int(response.url.split('&page=')[1])
        next_page_num = cur_page_num + 1
        if cur_page_num < self.max_page:
            next_url = response.url[:-len(str(cur_page_num))] + str(next_page_num)
            yield Request(url=next_url, callback=self.parse, dont_filter=True)

    def getGoodsBrand(self, goods_title, brand_list):
        for brand in brand_list:
            if brand in goods_title:
                return brand
        return "No-Brand"


