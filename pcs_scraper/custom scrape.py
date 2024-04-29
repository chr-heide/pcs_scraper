# Example use scraping 2019-results.

from pcs_scraper import PcsScraper

scraper = PcsScraper(start_year=2024, end_year=2024)
df = scraper.get_dataframe(startlist=False)
df.to_csv(f"data/2024_results.csv")
