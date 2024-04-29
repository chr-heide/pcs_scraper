# Scraping startlist for 2024 giro

from pcs_scraper import PcsScraper

scraper = PcsScraper(start_year=2024)
# Save startlist
df = scraper.get_dataframe(race = 'giro', results=False)
df.to_csv(f"data/giro2024_startlist.csv")