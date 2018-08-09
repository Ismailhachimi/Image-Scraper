"""
GoogleScraper is a simple image scraper, used to scrape google by a specific query tag.

For any further changes, please let me know what you think about this piece of code.

This code is one of a project solutions in the computer science department at INSA Rouen.

This is made to give (only) an illustration of Web Scraping concept.
This is not a full complete solution to scrape huge quantity of data.

Keep tracking this repository to get the latest updates.
"""

import os
import shutil
import requests
import time

from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options


class GoogleScraper:
    """
    # Parameters :
    ------------------------------------------------------------------------------------
    query : (or tag) a string which is used to search for the images
    name : the scraper name
    url_source : the main url string that is used to get the page's data dictionary
    google_urls : list of urls which are taken from the page's data dictionary
    images_urls : list of images direct urls (parsed urls from google_urls)

    # Functions :
    ------------------------------------------------------------------------------------
    get_urls() : the function which is used to get images_urls from the url_source dictionary
    parse_urls() : the function help pre-process the previous scraped urls to images_urls
    load_images() : the function which is used to download the images from images_urls
    """

    query = ''
    name = 'google_scraper'
    url_source = ''
    google_urls = []
    images_urls = []

    def __init__(self, query, size):
        """
        GoogleScraper's constructor
        :param query: the tag that is used to search for the images
        :param size: the images size. 'l' for long, 'm' for medium and 's' for small
        """
        if size in ['l', 'm', 's']:
            self.url_source = 'https://www.google.com/search?q={}&tbm=isch&tbs=isz:{}'.format(query, size)
            self.query = query
            self.size = size
        else:
            raise ValueError("The given size is not correct. Please make sure it's 'l', 'm' or 's")

    def get_urls(self):
        """
        This function scrape the google images urls from the data dictionary in the url_source
        """
        # urls_list is the urls list that we will scrape
        urls = []

        # verify if the tag is not provided
        if not self.query:
            print("The current object doesn't have a tag or the current tag is empty. Please provide one.")
        else:
            # instantiate a chrome options object to set the size and headless preference
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")

            # get the chrome_driver from the current directory
            chrome_driver = os.getcwd() + '/chromedriver'

            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

            driver.get(self.url_source)

            hyperlink_tags = driver.find_elements_by_xpath("//div[@class='rg_bx rg_di rg_el ivg-i']/a")

            for tag in hyperlink_tags:
                tmp = tag.get_attribute("href")
                to_eliminate = self.url_source + '#'
                if tmp != to_eliminate:
                    urls.append(tmp)

            driver.close()
            self.google_urls = urls

    def parse_urls(self):
        """
        This function takes the google urls and pre-process them to get the direct urls
        """
        if len(self.google_urls) == len(self.images_urls):
            print("The urls have been already parsed. You may use now load_images to download.")
        else:
            auth_urls_avoided = ['photobucket']
            urls = []
            for url in self.google_urls:
                if url != self.url_source+'#' and auth_urls_avoided[0] not in url:
                    # remove the google image response signature
                    url_google = url.split('https://www.google.com/imgres?imgurl=')[1]

                    # parse the rest of the url to get the right image url
                    url_image = url_google.split('&')[0].replace('%2F', '/').replace('%3A', ':')
                    urls.append(url_image)
            self.images_urls = urls
            print("The urls have been parsed successfully.")

    def load_images(self):
        """
        This function takes the parsed urls strings 'images_urls' and download the associated images
        """
        if not self.images_urls:
            print("The scraping object doesn't have a dictionary of urls to scrape."
                  + "\nPlease use .get_urls() to load the images urls.")
        else:
            number_error = 0
            i = 1
            for url in self.images_urls:
                url = verify_url(url)
                # print('\n'+url+'\n')
                if url is not '':
                    try:
                        response = requests.get(url, stream=True)
                    except requests.exceptions.ConnectionError:
                        continue

                    directory = 'images/' + self.query
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    if response.status_code == 200:
                        tmp_time_str = str(datetime.now()).split('.')[0].replace(' ', '_')
                        with open(directory + '/google_{}.jpg'.format(str(i) + '_' + tmp_time_str), 'wb') as f:
                            response.raw.decode_content = True
                            shutil.copyfileobj(response.raw, f)
                        i = i+1
                    else:
                        number_error += 1
                        print("Error [{}] : Cannot get the url! :(".format(str(response.status_code)))
                    time.sleep(0.5)
                else:
                    number_error += 1
                    print("OhOh ! : An invalid link :(")

            if number_error == 0:
                print("{} images have been downloaded successfully.".format(str(i-1)))
            else:
                print("{} images have been downloaded except ".format(str(i-1))
                      + "{} images with an error.".format(str(number_error)))
        print('Google scraping has finished')


def verify_url(url):
    """
    Verify the given url and return a valid url
    :param url: image url
    :return: Valid url
    """
    # NOTE : For now, we accept .jpg format only
    valid_url = ''
    if 'http' in url or 'https' in url:
        if '.jpg' in url:
            valid_url = '.jpg'.join(url.split('.jpg')[0:-1])+'.jpg'
    return valid_url
