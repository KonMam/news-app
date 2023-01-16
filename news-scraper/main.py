from scraper import DelfiScraper, MinutesScraper, VZScraper

# if from '/' directory
file_path = '/app/news.db'


def main():

    print(file_path)

    scraper = MinutesScraper()
    results = scraper.get_results()
    results.write_to_db(file_path)

    scraper = VZScraper()
    results = scraper.get_results()
    results.write_to_db(file_path)

    scraper = DelfiScraper()
    results = scraper.get_results()
    results.write_to_db(file_path)


if __name__ == "__main__":
    main()
