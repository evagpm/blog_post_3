# to run 
# cd Documents/PIC16B/blog_post_3/IMDB_scraper
# scrapy crawl imdb_spider -o results.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    #Chicago Fire tv show page
    start_urls = ['https://www.imdb.com/title/tt2261391/']

    """
    The method navigates to the cast and characters page and calls the parse_full_credits

    Inputs: self - an instance of the spider
            response - the page to parse 

    Output: a request to the cast and characters page with parse_full_credits
    """
    def parse(self, response):
        #Combine original url with fullcredits to get full url
        page = response.urljoin("fullcredits")
        yield scrapy.Request(page, callback = self.parse_full_credits)

    """
    The method scrapes the urls of the case member pages and calls parse_actor_page on each

    Inputs: self - the instance of the spider
            response - the page to parse

    Output: requests to each actors page calling parse_actor_page
    """
    def parse_full_credits(self, response):
        #The links to the actor's page are in the href attribute of the anchors of the 
        #table data entries with class primary_photo
        paths = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        #For each actor's relative path
        for path in paths:
            page = response.urljoin(path)

            #Navigate to that page
            yield scrapy.Request(page, callback = self.parse_actor_page)

    """
    The method scrapes the name and films for the actor

    Inputs: self - an instance of the spider
            response - the page to parse

    Output: a dict containing the actor and movie name for each film
    """
    def parse_actor_page(self, response):
        #Inside the table data on that the top the text in the first span is the name
        name = response.css("td.name-overview-widget__section span::text")[0].get()

        #The is a div for each film row and within that is a bold anchor with the film title
        films = response.css("div.filmo-row b a::text").getall()

        #For each film
        for film in films:
            #Output a dict with the actor and film name
            yield {
                "Actor": name,
                "Film": film
            }


