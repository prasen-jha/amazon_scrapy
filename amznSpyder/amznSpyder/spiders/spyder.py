import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AmznSpider(scrapy.Spider):
    name = 'amazon'
    # headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'}
    allowed_domains = ['www.amazon.in']
    start_urls = ['https://www.amazon.in/s?k=ginger+powder']

    product_link = LinkExtractor(restrict_xpaths='//div//h2/a/@href')
    rule_produt_link = Rule(product_link, callback='parse', follow=False)

    rules = (
        rule_produt_link,
    )

    def parse(self, response, **kwargs):
        for link in response.xpath("//div//h2/a/@href").extract():
            url = 'https://www.amazon.in' + link
            yield scrapy.Request(url, callback=self.parse_product,
                                 headers={
                                     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'})

    def parse_product(self, response):
        yield {
            'product_name': str(response.xpath('//span[@id="productTitle"]/text()').get()).strip(),
            'rating': response.xpath(""),
            'link': response.url,
        }
