

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# set up splinter and the executable path. 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# get the html
# soup parse the hotmail
# create parent element

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# find the title, but gives back the full html line
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### featured images

url = 'https://spaceimages-mars.com'
browser.visit(url)





#find and click the full image button

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()





# parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')





# find the relative image

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel





img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url





url = 'https://galaxyfacts-mars.com'
browser.visit(url)





# html = browser.html
# mars_facts_soup = soup(html, 'html.parser')

df = pd.read_html(url)[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace = True)
df




# convert dataframe into HTML

df.to_html()



# end browser

browser.quit()








