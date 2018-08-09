"""
InstaScraper is an images scraping spider class, used to scrape instagram by a given tag.
The url we are using is helping us to get a full dictionary of an instagram page. In this case,
we don't need to scrape the urls in the html DOM, a simple request retrieves the dictionary as
mentioned above.

For any further changes, let us know what you think about this program.

This program is created at the end of a project in the INSA Rouen engineering school.
This is a simple Web Scraping example or illustration and not a complete solution for images scraping.
"""

import shutil
import requests
import os
import time
from random import randint


class InstaScraper:
    """
    # Parameters :
    ------------------------------------------------------------------------------------
    tag : a string which is used in order to search for the images
    name : the scraper name
    url_source : the main url string, it is used to get the page's data dictionary
    urls : list of urls which are taken from the page's data dictionary

    # Functions :
    ------------------------------------------------------------------------------------
    get_urls() : the function which is used to get the images urls from the url_source dictionary
    load_images() : the function which is used to download the images by using self.urls
    """
    tag = ''
    name = 'insta_scraper'
    url_source = ''
    urls = ''

    def __init__(self, tag):
        """
        :param tag
        """
        self.tag = tag
        self.url_source = 'https://www.instagram.com/explore/tags/' + tag + '/?__a=1'

    def get_urls(self):
        """
        This function get the images urls from the url_source dictionary
        """
        # urls_list is the urls list that we will scrape
        urls_list = []

        # verify if the tag is not provided
        if self.tag == '':
            print('The current object doesn\'t have a tag or the current tag is empty. Please provide one.')
        else:
            # request the url_source and get its content
            response = requests.get(self.url_source)

            # get the response's content as a dictionary
            data_dict = response.json()

            # urls_number is the number of available urls
            urls_number = len(data_dict['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
            for i in range(0, urls_number):
                is_video = data_dict['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['is_video']

                # verify if the current element is a video, in case it is, we ignore it
                if not is_video:
                    display_url = data_dict['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node'][
                        'display_url']
                    urls_list.append(display_url)
            self.urls = urls_list

    def load_images(self):
        """
        This function takes the urls strings 'urls' and download the associated images
        """

        # verify if self.urls is empty. in case it is not, we download the images from the urls list
        if self.urls == '':
            print('The scraping object doesn\'t have a dictionary of urls to scrape.'
                  + '\n Please use .get_urls() to load the urls.')
        else:
            i = 1
            for url in self.urls:
                response = requests.get(url, stream = True)
                directory = 'images/' + self.tag
                if not os.path.exists(directory):
                    os.makedirs(directory)
                if response.status_code == 200:
                    with open('./images/{}/insta_{}_direct.jpg'.format(self.tag, str(i)), 'wb') as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)
                    i = i+1
                else:
                    print("Error [{}] : Cannot get the url! :(".format(str(response.status_code)))
                time.sleep(randint(1, 3))
