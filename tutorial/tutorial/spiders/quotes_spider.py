import scrapy

# Try running this with
#       scrapy crawl quotes --output=out.json --output-format=json
# Check out Items. It allows the convinient storage of formatted data.

# Possible uses:
# Maintain my own directory of Lehigh students
#   Cross reference my classes, etc. See who is in them.
# Download everything

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # This is used as our start_requests() return by default
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # scrapy.Request would require the url to be recreated. This shortcut avoids this.
            yield response.follow(next_page, callback=self.parse)