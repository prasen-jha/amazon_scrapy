import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AmazoncrawlSpider(CrawlSpider):
    name = 'amazonCrawl'
    allowed_domains = ['www.amazon.in']
    start_urls = ['https://www.amazon.in/s?k=spice+mix']

    product_link = LinkExtractor(restrict_xpaths='//div//h2/a')
    rule_product_link = Rule(product_link, callback='parse_item', follow=False)

    rules = (
        rule_product_link,
    )

    def parse_item(self, response):
        rating = response.xpath("//span[@id='acrPopover']/@title").get() or \
                 response.xpath("//span[@id='acrPopover']/@title")[0].get() if response.xpath("//span[@id='acrPopover']/@title") else 0

        yield {
            'product_name': str(response.xpath('//span[@id="productTitle"]/text()').get()).strip(),
            'rating': rating,
            # 'link': response.url,
        }
