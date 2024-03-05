# This main script will update the .csv-file containing results from the current year
# The script can be run as-is

from pcs_scraper import PcsScraper
import datetime

if __name__ == "__main__":
    scraper = PcsScraper(datetime.datetime.now().year)
    df = scraper.get_dataframe(startlist=False)
    df.to_csv(f"data/{datetime.datetime.now().year}_results.csv")
