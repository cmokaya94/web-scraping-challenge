from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from splinter import Browser

def init_browser():
    # Setting up windows browser with chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    #URL to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)    
    time.sleep(4)

    html = browser.html
    soup = bs(html, "html.parser")
    # Print text
    news_title = soup.find('div', class_="content_title").get_text()
    news_p = soup.find('div', class_="article_teaser_body").get_text()    

    #Mars Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # Go to 'FULL IMAGE'
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(4)
    # Go to 'more info'
    browser.click_link_by_partial_text('more info')
    time.sleep(4)

    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = bs(html, 'html.parser')
    # Scrape the URL
    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'


    #Mars Weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    timeout = 5
    try:
        myElem = WebDriverWait(browser,timeout)
    except:
        print("Timed out waiting for page to load")
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('div', class_= "css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").get_text()
    


    #Mars Facts
    fact_url = 'http://space-facts.com/mars/'
    browser.visit(fact_url)
    tables = pd.read_html(fact_url)
    tables

    ##Formatting 
    facts_df = tables[0]
    facts_df.columns = ["Description", "Values"]
    facts_df
    final_df=facts_df.set_index("Description")

    ##
    html_table=final_df.to_html()


    #Mars Hemispheres

    pic_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(pic_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    hemis_titles = soup.find_all('h3')

    for i in range(len(hemis_titles)):
        hemis_title = hemis_titles[i].text
        print(hemis_title)
        
        hemis_images = browser.find_by_tag('h3')
        hemis_images[i].click()
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        img_url = soup.find('img', class_='wide-image')['src']
        img_url = "https://astrogeology.usgs.gov" + img_url
        print(img_url)
        
        hemis_dict = {"title": hemis_title, "img_url":img_url}
        hemisphere_image_urls.append(hemis_dict)
    hemisphere_image_urls

  # Store data in a dictionary
    mars_data = {
       #News Title
       "news_title": news_title,
       #News Title
       "news_p": news_p,
       #Featured Image
       "featured_image_url": featured_image_url,
       #Mars Weather
       "mars_weather": mars_weather,
       #Mars Facts
       "html_table":html_table,
       #Mars Four Hemispheres
       "hemisphere_image_urls":hemisphere_image_urls}
    browser.quit()
    return mars_data