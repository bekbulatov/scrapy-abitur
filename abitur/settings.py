# Scrapy settings for abitur project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'abitur'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['abitur.spiders']
NEWSPIDER_MODULE = 'abitur.spiders'
DEFAULT_ITEM_CLASS = 'abitur.items.AbiturItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

