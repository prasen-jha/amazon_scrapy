import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# TODO: Add more values to extract e.g:
#  ingredient type, amazon seller rank, weight and quantity

# TODO: Add item pipeline and store data to a csv
#   Add pipeline to store data to database
#   Duplicate filter mechanism


class AmazoncrawlSpider(CrawlSpider):
    name = 'amazonCrawl'
    allowed_domains = ['www.amazon.in']
    start_urls = ['https://www.amazon.in/s?k=spice+mix']

    # Rules for extraction of links
    product_link = LinkExtractor(restrict_xpaths='//div//h2/a')
    rule_product_link = Rule(product_link, callback='parse_item', follow=False)

    next_page_link = LinkExtractor(restrict_xpaths="//ul[@class='a-pagination']//li/a/")
    rule_next_page = Rule(next_page_link, follow=True)

    rules = (
        rule_product_link,
        rule_next_page
    )

    def parse_item(self, response):
        rating = response.xpath("//span[@id='acrPopover']/@title").get() or \
                 response.xpath("//span[@id='acrPopover']/@title")[0].get() if response.xpath("//span[@id='acrPopover']/@title") else 0

        yield {
            'product_name': str(response.xpath('//span[@id="productTitle"]/text()').get()).strip(),
            'rating': rating,
            # 'link': response.url,
        }
