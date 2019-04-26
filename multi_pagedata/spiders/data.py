import scrapy

class multi_pagedata(scrapy.Spider):

    name = "test"
    start_urls = ["http://lab.scrapyd.cn/"]

    def parse(self, response):

        data = response.css('div.quote')

        for i in data:
            text = i.css('.text::text').extract_first()
            author = i.css('.author::text').extract_first()

            tags = i.css('.tags .tag::text').extract()
            tags = ",".join(tags)

            filename = '%s-语录.txt' %author

            with open(filename,"a+",encoding="utf-8") as f:
                f.write(text)
                f.write('\n')
                f.write("标签:"+tags)
                f.write("\n-------------\n")
                f.close()

        next_page = response.css('li.next a::attr(href)').extract_first()

        if next_page is not None:

            next_page = response.urljoin(next_page)
            yield  scrapy.Request(next_page,callback=self.parse)
