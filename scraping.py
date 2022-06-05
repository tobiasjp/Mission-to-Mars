# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager



def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_images(browser)
    }


    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_images(browser):
        # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)




    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.


    for x in range(0,4):
        browser.find_by_tag('h3')[x].click()
        


        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')

        full_hemi = hemisphere_soup('div', class_='container')
        

        for each_hemi in full_hemi:

            hemispheres = {}
        
            hemi_titles = each_hemi.h2.text

            hemi_urls_rel = each_hemi.find('img', class_='wide-image').get('src')
        
            hemi_urls = f'https://astrogeology.usgs.gov/cache/{hemi_urls_rel}'

            hemispheres = {'img_url':hemi_urls, 'title': hemi_titles}

            hemisphere_image_urls.append(hemispheres)

        browser.back()
        
        
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())












































##------ written code



# # Import Splinter and BeautifulSoup
# from splinter import Browser
# from bs4 import BeautifulSoup as soup
# import pandas as pd
# import datetime as dt
# from webdriver_manager.chrome import ChromeDriverManager




# def scrape_all():

# # set up splinter and the executable path. 
 
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=False)

#     # set our news title and paragraph varaibles
#     news_title, news_paragraph = mars_news(browser)

#     # Run all scraping functions and store results in dictionary
#     data = {
#         "news_title": news_title,
#         "news_paragraph": news_paragraph,
#         "featured_image": featured_image(browser),
#         "facts": mars_facts(),
#         "last_modified": dt.datetime.now()}

#     # stop the web driver

#     browser.quit()

#     return data


# def mars_news(browser):
#     # Visit the mars nasa news site
#     url = 'https://redplanetscience.com'
#     browser.visit(url)
#     # Optional delay for loading the page
#     browser.is_element_present_by_css('div.list_text', wait_time=1)



#     # get the html
#     # soup parse the hotmail
#     # create parent element

#     html = browser.html
#     news_soup = soup(html, 'html.parser')
#     try:
#         slide_elem = news_soup.select_one('div.list_text')

#         # find the title, but gives back the full html line
#         slide_elem.find('div', class_='content_title')


#         # Use the parent element to find the first `a` tag and save it as `news_title`
#         news_title = slide_elem.find('div', class_='content_title').get_text()
    


#         # Use the parent element to find the paragraph text
#         news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
#     except AttributeError:
#         return None, None
    
#     return news_title, news_p


# # ### featured images

# def featured_image(browser):

#     url = 'https://spaceimages-mars.com'
#     browser.visit(url)


#     #find and click the full image button

#     full_image_elem = browser.find_by_tag('button')[1]
#     full_image_elem.click()

#     # parse the resulting html with soup
#     html = browser.html
#     img_soup = soup(html, 'html.parser')


#     # find the relative image
#     try:

#         img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

#     except AttributeError:
#         return None

#     img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    

#     return img_url



# def mars_facts():
#     try:

#         url = 'https://galaxyfacts-mars.com'
#         df = pd.read_html(url)[0]
#     except BaseException:
#         return None

#     df.columns=['description', 'Mars', 'Earth']
#     df.set_index('description', inplace = True)

#     return df.to_html(classes="table table-striped")


# if __name__ == "__main__":
#     # If running as script, print scraped data
#     print(scrape_all())






