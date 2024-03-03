import scrapy
import json

class APISpider(scrapy.Spider):
    name = "data"
    start_page = 0
    allowed_domains = ["hm.com"]
    # threse are the APIs links of all website and scrapy framework will extract them all 
    start_urls = ["https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:men_all:sale:false:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:men_all:sale:true:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:ladies_all:sale:false:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:ladies_all:sale:true:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:kids_newbornbaby_viewall:sale:false:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:kids_newbornbaby_viewall:sale:true:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:home_all:sale:false:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:home_all:sale:true:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:beauty_all:sale:false:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:beauty_all:sale:true:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:kids_viewall:sale:false:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:kids_viewall:sale:true:oldSale:false:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false",
                  "https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:sportswear_kids_all:category:sportswear_kids_accessories:category:sportswear_women:category:sportswear_men:sale:true:isNew:false&currentPage=0&pageSize=36&skipStockCheck=false"]

    def parse(self, response):
        #Here we will extract the body of the json file and filter it after
        data = json.loads(response.body)
        results=data.get("results")

        for item in results:
            dbq_prd_type = "E0003"
            website_name = "United Kingdom - H&M"
            competence_date = "2024-03-03"
            brand = item.get("brandName") 
            product_code = item.get("searchEngineProductId")
            country_code = +44
            currency_code = item.get("price").get("currencyIso")
            price = item.get("price").get("formattedValue")
            CategoryCode = item.get("mainCategoryCode") 
            title = item.get("name")
            img_url = item.get("images")[0]["baseUrl"]
            item_url = item.get("linkPdp")
            colors = item.get("articleColorNames") 
            variantSizes = item.get("variantSizes")
            sizes = [item["filterCode"] for item in variantSizes]
        
            yield {
                "dbq_prd_type": dbq_prd_type,
                "website_name": website_name,
                "competence_date": competence_date,
                "brand": brand,
                "title": title,
                "price": price,
                "product_code": product_code,
                "country_code": country_code,
                "currency_code": currency_code,
                "CategoryCode": CategoryCode,
                "sizes": sizes,
                "colors": colors,
                "img_url": img_url,
                "item_url": "https://www2.hm.com/" + item_url,
            }

        #here we extract the number of pages to paginate the all website 
        num_pages = data.get("pagination")["numberOfPages"]  

        for page_number in range(0, num_pages):
            next_page_url = [
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:men_all:sale:false:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:men_all:sale:true:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:ladies_all:sale:false:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:ladies_all:sale:true:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:kids_newbornbaby_viewall:sale:false:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:kids_newbornbaby_viewall:sale:true:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:home_all:sale:false:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:home_all:sale:true:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:beauty_all:sale:false:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:beauty_all:sale:true:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:kids_viewall:sale:false:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:kids_viewall:sale:true:oldSale:false:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false",
                f"https://www2.hm.com/hmwebservices/service/products/plp/hm-greatbritain/Online/en?q=:stock:category:sportswear_kids_all:category:sportswear_kids_accessories:category:sportswear_women:category:sportswear_men:sale:true:isNew:false&currentPage={page_number}&pageSize=36&skipStockCheck=false"]
            for url in next_page_url:
                yield response.follow(url, callback=self.parse)



        


    
