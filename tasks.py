from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium

browser = Selenium()



@task
def minimal_task():
    open_news_browser()

# STEP 1
# Open the site by following the link
def open_news_browser():
    browser.open_available_browser("https://www.reuters.com/")



# STEP 2
# Enter a phrase in the search field

# STEP 3
# On the result page, If possible select a news category or section from the Choose the latest (i.e., newest) news


# STEP 4
# Get the values: title, date, and description.


# STEP 5
'''
Store in an Excel file:
title, date, description (if available), picture filename, count of search phrases in the title and description True or False, depending on whether the title or description contains any amount of money Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
'''

# STEP 6
# Download the news picture and specify the file name in the Excel file


# STEP 7

# Follow steps 4-6 for all news that falls within the required time period