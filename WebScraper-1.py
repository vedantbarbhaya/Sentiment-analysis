# PROGRAM TO GET ALL-REVIEWS LINK OF USER ENTERED PRODUCT
from selenium import webdriver
# used for web browsing
from selenium.webdriver.common.keys import Keys
# used to perform the click action on a button
import time
# to give certain delay
import re
# Regular expressions for string matching
class AmazonBrowsing:
    reviewPageLink = []
    def __init__(self):
        browser = webdriver.Chrome('/Users/vishalkundar/Downloads/chromedriver')
        # the chrome driver allows us to browse the web
        browser.get('https://www.amazon.in')
        # base url - this site will open up first
        productName = input("Enter name of the product: ")
        # this is to be entered in search bar
        searchbar = browser.find_element_by_id("twotabsearchtextbox")
        # id of search bar
        searchbar.send_keys(productName)
        searchbar.send_keys(Keys.ENTER)
        # enters and hits send

        time.sleep(2)
        #delay
        lists = []
        productPage = browser.find_elements_by_class_name('a-link-normal')
        # since there are a lot of links we are storing them in a list
        pattern = productName.split(' ')
        startingName = pattern[0]
        # For getting the starting word of user entered product
        for product in productPage:
            if re.search(startingName,product.get_attribute('href')):
                if re.search('B07',product.get_attribute('href')):
                    lists.append(product.get_attribute('href'))
        # B07 is common regex in product page
        productPageLink = lists[0]    
        # the 0th index conatins link to product page
        browser.get(productPageLink)
        # switching to product page
        time.sleep(2)
        # giving time for page to load
        reviewPage = browser.find_element_by_class_name('a-link-emphasis')
        # link under this class
        link = reviewPage.get_attribute('href')
        # link stored
        self.reviewPageLink.append(link +"&pageNumber=")
        # appending page number as it is not there by default
        #browser.get(reviewPageLink[0])
    def getReviewPage(self):
        return self.reviewPageLink[0]
