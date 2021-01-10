##Load Dependencies
import pandas as pd
import requests
import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

#Initialize Browser
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


#Scape code
def scrape():
    browser = init_browser()
    mars_stuff = {}

#Nasa Mars News
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')
#Nasa News Article Title and Paragraph
    nasa_title = nasa_soup.find_all('div',class_="content_title")[1].text
    nasa_p = nasa_soup.find_all('div',class_='article_teaser_body')[0].text
    mars_stuff['nasa_news_title'] = nasa_title
    mars_stuff['nasa_news_paragraph'] = nasa_p
    
#JPL Mars Space Images - Featured Image
    jpl_website='https://www.jpl.nasa.gov'
    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    jpl_html= browser.html
    jpl_soup= bs(jpl_html, 'html.parser')
#JPL featured image
    jpl_image=jpl_soup.find_all('img')[3]["src"]
    jpl_image_url=jpl_website+jpl_image
    mars_stuff['jpl_featured_image'] = jpl_image_url
   
#Mars Facts
    facts_url='https://space-facts.com/mars/'
    browser.visit(facts_url)
#Table read
    facts_table=pd.read_html(facts_url)
    facts_df=facts_table[0]
    facts_df.columns=['Description', 'Value']
    facts_html= facts_df.to_html(classes = 'table')
    mars_stuff['mars_facts']=facts_html

#Mars Hemispheres
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemi_html= browser.html
    hemi_soup=bs(hemi_html, 'html.parser')
    items=hemi_soup.find_all('div', class_='item')
    base_hemi= 'https://astrogeology.usgs.gov'
#Hemisphere Dictionary
    hemi_image_dict=[]
    for i in items:
        title=i.find('h3').text
        image_url=i.find('a', class_='itemLink product-item')['href']
        browser.visit(base_hemi+image_url)
        image_url=browser.html
        image_soup=bs(image_url, 'html.parser')
        full_image=base_hemi+image_soup.find('img', class_='wide-image')['src']
        hemi_image_dict.append({"title" : title, "image_url" : full_image})
    
    mars_stuff["hemisphere_images"] = hemi_image_dict

    browser.quit()

    return mars_stuff