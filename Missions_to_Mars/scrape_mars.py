from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    # NASA Mars News
    browser = init_browser()
    
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    time.sleep(3)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    slide = news_soup.select('ul.item_list li.slide')[0]

    news_title = slide.find("div", class_="content_title").get_text()
    news_p = slide.find("div", class_="article_teaser_body").get_text()

    # JPL Mars Space Images - Featured Image
    browser = init_browser()

    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html#'
    browser.visit(jpl_url)

    time.sleep(3)

    html = browser.html
    jpl_soup = BeautifulSoup(html, "html.parser")

    image = jpl_soup.select('div.floating_text_area a')
    image_url = image[0]['href']

    featured_image_url = ('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_url)

    # Mars Facts
    browser = init_browser()

    facts_url = 'https://space-facts.com/mars/#'

    tables = pd.read_html(facts_url)
    df = tables[0]
    html_table = df.to_html(header=False, index=False)
    mars_table = html_table.replace('\n', '')

    # Mars Hemispheres
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]

    # Store data in a dictionary
    listings = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_table": mars_table,
        "hemisphere_image_urls": hemisphere_image_urls,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return listings
