import scrapy
import json

class TechsoupDetails(scrapy.Spider):
    name = "techsoup_details"
    start_urls = ["https://www.techsoup.ca/content/acrobat-pro-2020-windows-english"]
    count = 1

    with open('techsoup.json', 'r') as j:
        products = json.loads(j.read())

    def parse(self, response):
        product_details = response.css('div.product-details__field')
        try:
            yield {
                "name" : self.products[self.count]['name'].replace('–','-'),
                "donor" : (product_details.css('div.field.field-name-field-donor-partner')).css('a::text').getall(),
                "language" : (product_details.css('div.field.field-name-field-language')).css('a::text').getall(),
                "software_category" : (product_details.css('div.field.field-name-field-software-category')).css('a::text').getall(),
                "media" : (product_details.css('div.field.field-name-field-media')).css('a::text').getall(),
                "platform" : (product_details.css('div.field.field-name-field-platform')).css('a::text').getall(),
                "product_ID" : product_details.css('div.field-items::text').getall()[-1].strip(),
                "admin_fee" : (product_details.css('div.field.field-name-commerce-price')).css('div.field-item::text').get().replace("\u200e", ''),
                "url" : self.products[self.count]['url']
                }
        except:
            yield {
                "donor" : (product_details.css('div.field.field-name-field-donor-partner')).css('a::text').getall(),
                "language" : (product_details.css('div.field.field-name-field-language')).css('a::text').getall(),
                "software_category" : (product_details.css('div.field.field-name-field-software-category')).css('a::text').getall(),
                "media" : (product_details.css('div.field.field-name-field-media')).css('a::text').getall(),
                "platform" : (product_details.css('div.field.field-name-field-platform')).css('a::text').getall(),
                "product_ID" : product_details.css('div.field-items::text').getall()[-1].strip(),
                "admin_fee" : "None"
                }

        try:
            next_product = self.products[self.count]['url']
            self.count += 1
            yield response.follow(next_product, callback = self.parse, dont_filter=True)
        except IndexError:
            print("Finished")





