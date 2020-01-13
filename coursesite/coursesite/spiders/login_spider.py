import scrapy
from selenium import webdriver

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass

class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ['https://coursesite.lehigh.edu/auth/saml/login.php']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open('./credentials.txt', 'r') as credential_file:
            self.username = credential_file.readline().rstrip()
            self.password = credential_file.readline().rstrip()
        self.driver = webdriver.Firefox(executable_path='../geckodriver.exe')

    def parse(self, response):
        self.driver.get(response.url)
        print(self.driver.current_url)

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }