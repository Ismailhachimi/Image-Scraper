import argparse
import GoogleScraper
import InstaScraper


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", help="the tag which the scraper will search for")
    parser.add_argument("--google", help="boolean, Yes to execute GoogleScraper, otherwise No")
    parser.add_argument("--insta", help="boolean, Yes to execute InstaScraper, otherwise No")
    parser.add_argument("--gsize", help="the google image's size in ['s', 'm', 'l']")

    inputs = vars(parser.parse_args())

    if inputs["tag"] is None:
        print("The 'tag' argument is missing !")
    else:
        size_google = inputs["gsize"]
        if size_google is None:
            size_google = 'l'

        query_tag = inputs["tag"]

        google_state = "yes" if inputs["google"] is None else inputs["google"]
        insta_state = "yes" if inputs["insta"] is None else inputs["insta"]

        accepted_states = ['yes', 'no']

        # The scrapers are lunched if their states are set to 'Yes' or not specified (None)

        if (google_state.lower() in accepted_states) and (insta_state.lower() in accepted_states):
            if google_state.lower() == 'yes':
                print('\n----------------------- Load Google images ------------------------\n')
                google_scraper = GoogleScraper.GoogleScraper(query=query_tag, size=size_google)
                google_scraper.get_urls()
                google_scraper.parse_urls()
                google_scraper.load_images()
            else:
                print("\nGoogleScraper has been ignored.\n")

            if insta_state.lower() == 'yes':
                print('\n------------------------ Load Insta images ------------------------\n')
                insta_scraper = InstaScraper.InstaScraper(tag=query_tag)
                insta_scraper.get_urls()
                insta_scraper.load_images()
            else:
                print("\nInstaScraper has been ignored.\n")
        else:
            print("The scraping states aren't correct. " +
                  "\nPlease make sure that each of two states is equal to 'Yes' or 'No'" +
                  "\nYou can leave them empty (It's the 'Yes' option).")
