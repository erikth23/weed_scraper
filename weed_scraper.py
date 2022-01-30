import time
from datetime import date
from c21_scraper import c21_scraper
from file_writer import file_writer

base_url = "https://dutchie.com/embedded-menu/%s/products/%s?page=%s"
base_file_path = "/Users/erikth/Projects/weed_scraper/data_ingestion/%s.xlsx"
categories = ["flower", "pre-rolls", "vaporizers", "concentrates", "edibles", "tinctures", "topicals"]
stores = ["cannabis-21", "have-a-heart-belltown", "zips-sodo", "kush-21"]


def main():

    today = date.today()
    file_path = base_file_path % (today.strftime("%m_%d_%y"))

    writer = file_writer(file_path)
    scraper = c21_scraper(writer)

    page = 1
    disabled = False

    for store in stores:
        for c in categories:
            sheet_name = store + "-" + c
            writer.change_sheet(sheet_name)
            while not disabled:
                url = base_url % (store, c, str(page))
                (new_products, disabled) = scraper.extract_products(url)

                page += 1

            disabled = False
            page = 1

            print('Got category %s for store %s' % (c, store))

        print('Got store: %s' % (store))
        

    scraper.cleanup()


if __name__ == '__main__':
    main()
