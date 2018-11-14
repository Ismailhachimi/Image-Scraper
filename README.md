# Mini Image Scraper - Scrapic

Scrapic is a very basic scraper which takes a tag and search for its related images on google and instagram and returns them to a local repository for future usage.

This project has the purpose of illustrating a very basic example of web scraping for images and doesn't have a direct relation to the said websites, mainly google and instagram. One can change the code to whatever he or she suits him or her.

**PS** : The google scraper is much better than the instagram scraper because images are labeled efficiently on google comparing to instagram where images are simply labeled by users using hashtags.

## Dependencies
Main : 
* Requests (for HTTP requests)
* Selenium (for Javascript generated images)

Also :
* argparse
* shutil
* etc.

## Launch Scrapers
`scrapic` is a script that launchs both the GoogleScraper and InstaScraper in order to get an average of 150 pictures.

To use it, the attached peace of code serves to launch the scraping by creating a folder which is associated to the tag specified by the user.

    python3 scrapic.py --tag **tag** --google **state** --insta **state** --gsize **size**

The `--google` argument describes the scraper state to be used or not. Per default, it's set to 'yes' if None is given.
The same for the `--insta` argument but keep in mind that you may want to keep the GoogleScraper only due to the quality and coherence of images. 
Finally, `--gsize` is the google image size we want to scrape. We can use 's' for small, 'm' for medium and 'l' for large.

## Separated use of Scrapers
### Example in Python
in the current direcory, we can call the Google Scraper with the following example :

    >>> from GoogleScraper import GoogleScraper
    >>> scraper = GoogleScraper(query='paris', size='l')
    >>> scraper.get_urls()
    >>> scraper.parse_urls()
    >>> scraper.load_images()

**Note**: The functions are seperated and put in a class, so that you can different objects in case you want to scraper more than one query.

## Next Updates
Keep an eye on this repository by forking or giving a star because there will be some changes and improvements in the scripts. 

---
