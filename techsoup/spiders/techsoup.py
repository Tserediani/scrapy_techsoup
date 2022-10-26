import scrapy
import json

class Techsoup(scrapy.Spider):
    name = 'techsoup'
    start_urls = [r"https://www.techsoup.ca/product-catalog/products?page=1&referer_path=%2Fproduct-catalog"]
    pg = 1

    def parse(self,response):
        data = json.loads(response.text)
        selector = scrapy.Selector(text=data['products'], type="html")

        for products in selector.css('li.ts-stock-product'):
            yield {
                "name" : products.css('h2.ts-stock-product__title::text').get().strip(),
                "url" : f"https://www.techsoup.ca{products.css('a.ts-stock-product__url').attrib['href']}"
            }
        next_page = fr"https://www.techsoup.ca/product-catalog/products?page={self.pg}&referer_path=%2Fproduct-catalog"
        self.pg += 1
        if data['items_counts']['left_to_show'] != 0:
            yield response.follow(next_page, callback = self.parse)

