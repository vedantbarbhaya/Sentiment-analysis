# Importing Scrapy Library
import scrapy
import time
from Robo import AmazonBrowsing
# Scrapy is a web crawling framework for a developer to write code to create 
# which define how a particular site (or a group of websites) will be scrapped.

# A scrapy project enables users to collate different components of the crawlers into a single folder. 
# To create a scrapy project use following command in terminal

# scrapy startproject amazon_reviews_scraping 

# The project file consists of two items. A project folder and a scrapy config file for the project.
# This config file can be used deploy and run proects on the server.

# A spider is a chunk of python code which determines how a web page will be scrapped.
# It is the main component which crawls different web pages and extracts content out of it.

# To create spider use the following code in the terminal

# scrapy genspider amazon_review your-link-here

# Now 

# Creating a new class to implement Spider
class AmazonReviewsSpider(scrapy.Spider):
    
# On the reviews page, there is a division with id "cm_cr-review_list". 
# This division multiple sub-division within which the review content resides. 
# We are planning to extract both rating stars and review comment from the web page. 
# We need to one more level deep into one other sub-divisions to prepare a scheme on 
# fetching both star rating and review comment.    
    
    # Spider name
    name = 'amazon_reviews'
    
    # Domain names to scrape
    allowed_domains = ['amazon.in']
    
# We begin by extending the Spider class and mentioning the URLs we plan on scraping. 
# Variable start_urls contains the list of the URLs to be crawled by the spider.    
    
    # Base URL for the MacBook air reviews
    linkObject = AmazonBrowsing()
    time.sleep(8)
    myBaseUrl = linkObject.getReviewPage()
    start_urls=[]
   
    # Creating list of urls to be scraped by appending page number a the end of base url
    for i in range(1,121):
        start_urls.append(myBaseUrl+str(i))
   
    # Defining a Scrapy parser
    def parse(self, response):
       
# We need to define a parse function which gets fired up whenever our spider visits a new page. 
# In the parse function, we need to identify patterns in the targeted page structure. 
# Spider then looks for these patterns and extracts them out from the web page.       
        
            data = response.css('#cm_cr-review_list')
             
            # Collecting product star ratings
            star_rating = data.css('.review-rating')
            
            # Collecting user reviews
            comments = data.css('.review-text')
            count = 0
            
            # Combining the results
            for review in star_rating:
                yield{'stars': ''.join(review.xpath('.//text()').extract()),
                      'comment': ''.join(comments[count].xpath(".//text()").extract())
                     }
                count=count+1
                
# We can run this spider by using the runspider command. 
# It takes to input the spider file to run and the output file to store the collected results.  
# Use the below command in terminal to run the code:
                
#scrapy runspider /Users/-Add code to amazon scrapy directory here-/Amazon_Reviews.py -o reviews.csv                
                
                
                
                
                
                
                
                
                
                
                
