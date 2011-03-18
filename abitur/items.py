# -*- coding:utf8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

import re
from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import MapCompose

MONTHS = {
    u'января': '01',
    u'февраля': '02',
    u'марта': '03',
    u'апреля': '04',
    u'мая': '05',
    u'июня': '06',
    u'июля': '07',
    u'августа': '08',
    u'сентября': '09',
    u'октября': '10',
    u'ноября': '11',
    u'декабря': '12'
}

def parse_date(x):
    match = re.match('(?P<day>\d{1,2})(?P<month>.+)(?P<year>\d{4})', x)
    if not match:
        return None
    return '.'.join([match.group('day').zfill(2), MONTHS[match.group('month').strip()], match.group('year')])


def parse_price(x):
    if u'нет данных' in x:
        return None
    match = re.search(u'от\s*(?P<min>[\d\.]+)\s*до\s*(?P<max>[\d\.]+)', x)
    min = float(match.group('min')) * 1000
    max = float(match.group('max')) * 1000
    if min == max:
        return "%d" % min
    return '%d-%d' % (min, max)


class AbiturItem(Item):

    name = Field()
    state = Field(input_processor=MapCompose(lambda s: not re.match(u'\s*не', s)))
    description = Field()
    students = Field(input_processor=MapCompose(lambda s: int(s)))
    price = Field(input_processor=MapCompose(parse_price))
    address = Field()
    phone = Field()
    fax = Field()
    site = Field()

    licence = Field()
    licence_order = Field()
    licence_department = Field()
    licence_expired = Field(input_processor=MapCompose(parse_date))

    accreditation = Field()
    accreditation_order = Field()
    accreditation_department = Field()
    accreditation_expired = Field(input_processor=MapCompose(parse_date))
