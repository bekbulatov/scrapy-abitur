# -*- coding:utf8 -*-

import re

from abitur.items import AbiturItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector

class AbiturLoader(XPathItemLoader):
    default_input_processor = MapCompose(lambda s: re.sub('\s+', ' ', s.strip()))
    default_output_processor = TakeFirst()

class AbiturSpider(CrawlSpider):

    name = "abitur"
    allowed_domains = ["abitur.nica.ru"]
    start_urls = ["http://abitur.nica.ru/new/www/search.php?region=77&town=0&opf=0&type=0&spec=0&ed_level=0&ed_form=0&qualif=&substr=&page=1"]

    rules = (
             Rule(SgmlLinkExtractor(allow=('search\.php\?.+')), follow=True),
             Rule(SgmlLinkExtractor(allow=('vuz_detail\.php\?.+')), callback='parse_item'),
             )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        l = AbiturLoader(AbiturItem(), hxs)
        l.add_xpath('name', '//td[@id="content"]/h1/text()')
        l.add_xpath('state', '//td[@id="content"]/div/span[@class="gray"]/text()')
        l.add_xpath('description', '//div[@id="info"]/p/text()')
        l.add_xpath('students', '//div[@id="info"]/p/text()', re=u'(\d+)\s*человек')
        l.add_xpath('price', '//div[@class="cost"]/text()')
        l.add_xpath('address', '//div[@class="contact"]/p/text()')
        l.add_xpath('phone', '//div[@class="contact"]/p/text()', re=u'Телефон:(.*)')
        l.add_xpath('fax', '//div[@class="contact"]/p/text()', re=u'Факс:(.*)')
        l.add_xpath('site', '//div[@class="contact"]/p/a[contains(@href, "http://")]/@href')

        l.add_xpath('licence', '//table[@class="lic"][1]/tr[1]/td[2]/text()')
        l.add_xpath('licence_order', '//table[@class="lic"][1]/tr[2]/td[2]/text()')
        l.add_xpath('licence_department', '//table[@class="lic"][1]/tr[3]/td[2]/text()')
        l.add_xpath('licence_expired', '//table[@class="lic"][1]/tr[4]/td[2]/text()')

        l.add_xpath('accreditation', '//table[@class="lic"][2]/tr[1]/td[2]/text()')
        l.add_xpath('accreditation_order', '//table[@class="lic"][2]/tr[2]/td[2]/text()')
        l.add_xpath('accreditation_department', '//table[@class="lic"][2]/tr[3]/td[2]/text()')
        l.add_xpath('accreditation_expired', '//table[@class="lic"][2]/tr[4]/td[2]/text()')

        return l.load_item()
