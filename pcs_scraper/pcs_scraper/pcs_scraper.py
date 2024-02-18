import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

from .constants import urls_2022

class PcsScraper:

    def __init__(self, start_year, end_year=datetime.datetime.now().year):
        # Generates a list of the years to be included in scraping
        self.years = list(range(start_year, end_year + 1))
        # Generates a list of the URLs to be scraped
        self.urls = [race.replace('2022', str(year))
                     for year in self.years
                     for race in urls_2022]

    # A method for generating a soup-object and a table from a url
    @staticmethod
    def gen_soup(url, table=True):
        # Creating the soup-object
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        # Running a number of checks to ensure that the url is scapeable
        if soup.find('h1').text == "Page not found":
            return None
        elif soup.select('tbody')[0].text == "\n":
            return None
        elif "(TTT)" in soup.select('title')[0].text:
            return None
        if table:
            return soup, soup.select('tbody')[0]
        else:
            return soup

    # A method that creates two lists containing soups and tables from all races
    def get_all_soups(self):
        raw = [self.gen_soup(url) for url in tqdm(self.urls, desc='Getting data')
               if self.gen_soup(url) is not None]
        soups = [soup[0] for soup in raw]
        tables = [soup[1] for soup in raw]
        return soups, tables

    # A method for generating startlist-related urls. It is able to generate only specified stages.
    @staticmethod
    def gen_startlist_urls(race, stages=None):
        if stages is None:
            stages = list(range(0, 22))
        race_dict = {
            'giro': [f'https://www.procyclingstats.com/race/giro-d-italia/{datetime.datetime.now().year}/stage-',
                     f'https://www.procyclingstats.com/race/giro-d-italia/{datetime.datetime.now().year}/startlist'],
            'tour':
                [f'https://www.procyclingstats.com/race/tour-de-france/{datetime.datetime.now().year}/stage-',
                 f'https://www.procyclingstats.com/race/tour-de-france/{datetime.datetime.now().year}/startlist'],
            'vuelta':
                [f'https://www.procyclingstats.com/race/vuelta-a-espana/{datetime.datetime.now().year}/stage-',
                 f'https://www.procyclingstats.com/race/vuelta-a-espana/{datetime.datetime.now().year}/startlist']
            }
        upcoming_urls = [race_dict[race][0] + str(num) for num in stages]
        startlist_url = race_dict[race][1]
        return upcoming_urls, startlist_url

    # A function that gets results and metadata from one stage
    @staticmethod
    def get_results(soup, table):
        # Creates a dictionary with all the relevant information
        out = {
            'placement': [num + 1 for num in range(len(table.select('tr')))],
            'team': [t.text for t in table.find_all('td', class_='cu600') if "bonis" not in str(t)],
            'id': [i['data-id'] for i in table.select('input')],
            'rider': [i['data-seo'] for i in table.select('input')],
            'time': [i.contents[0].text for i in table.find_all('td', {'class': 'time ar'})],
            'parcours': [soup.select('ul.infolist li')[7].select('span')[0]['class'][2]]*len(table.select('tr')),
            'date': [soup.select('ul.infolist li')[0].select('div')[1].text]*len(table.select('tr')),
            'distance': [float(soup.select('ul.infolist li')[4].select('div')[1].text[:-3])]*len(table.select('tr')),
            'points_scale': [soup.select('ul.infolist li')[5].select('div')[1].text]*len(table.select('tr')),
            'uci_scale': [soup.select('ul.infolist li')[6].select('div')[1].text]*len(table.select('tr')),
            'profile_score': [float(soup.select('ul.infolist li')[8].select('div')[1].text)]*len(table.select('tr')),
            'vertical_meters': [float(soup.select('ul.infolist li')[9].select('div')[1].text)]*len(table.select('tr')),
            'startlist_quality': [float(soup.select('ul.infolist li')[13].select('div')[1].text)]*len(table.select('tr')),
            'title': [soup.select('title')[0].text[:-8]]*len(table.select('tr'))
        }
        return out

    # A function that gets startlist and metadata from one upcoming stage
    @staticmethod
    def get_startlist(startlist_soup, stage_soup):
        soup = startlist_soup.find_all(class_="ridersCont")
        length = len([r.find("a")['href'][6::] for i in soup for r in i.find_all("li")])
        # Creates a dictionary with the relevant information
        out = {
            'startlist_old': [r.find("a")['href'][6::] for i in soup for r in i.find_all("li")],
            'startlist_new': [r.find("a").text for i in soup for r in i.find_all("li")],
            'parcours': [stage_soup.select('ul.infolist li')[7].select('span')[0]['class'][2]]*length,
            'date': [stage_soup.select('ul.infolist li')[0].select('div')[1].text]*length,
            'distance': [float(stage_soup.select('ul.infolist li')[4].select('div')[1].text[:-3])]*length,
            'points_scale': [stage_soup.select('ul.infolist li')[5].select('div')[1].text]*length,
            'uci_scale': [stage_soup.select('ul.infolist li')[6].select('div')[1].text]*length,
            'profile_score': [float(stage_soup.select('ul.infolist li')[8].select('div')[1].text)]*length,
            'vertical_meters': [float(stage_soup.select('ul.infolist li')[9].select('div')[1].text)]*length,
            'startlist_quality': [float(stage_soup.select('ul.infolist li')[13].select('div')[1].text)]*length,
            'title': [stage_soup.select('title')[0].text[:-8]]*length
        }
        return out

    # A function that brings it all together:
    # Based on the arguments it should generate all the urls and soups and then iterate through them
    # everything should be stored in lists. By the end a data-frame is to be created from these lists.
    def get_dataframe(self, race='tour', stages=None, results=True, startlist=True):

        if results:

            # Initially create an empty dictionary to store the results
            data_results = {
                'placement': [],
                'team': [],
                'id': [],
                'rider': [],
                'time': [],
                'parcours': [],
                'date': [],
                'distance': [],
                'points_scale': [],
                'uci_scale': [],
                'profile_score': [],
                'vertical_meters': [],
                'startlist_quality': [],
                'title': []
            }

            # Using a for-loop to extend the data-dictionary with results of all the races
            soups, tables = self.get_all_soups()
            for soup, table in tqdm(zip(soups, tables), desc="Processing data"):
                try:
                    temp_data = self.get_results(soup, table)
                    for key in data_results:
                        data_results[key].extend(temp_data[key])
                except ValueError:
                    print(f"Error in {soup.select('title')[0].text[:-8]}")

            # Finally converting to a dataframe, as this is most convenient to return
            data_results_df = pd.DataFrame(data_results)

        if startlist:

            data_startlists = {
                'startlist_old': [],
                'startlist_new': [],
                'parcours': [],
                'date': [],
                'distance': [],
                'points_scale': [],
                'uci_scale': [],
                'profile_score': [],
                'vertical_meters': [],
                'startlist_quality': [],
                'title': []
            }

            # Before looping the url's for startlists and race-metadata are generated. Necessary as these are not
            # static.
            upcoming_urls, startlist_url = self.gen_startlist_urls(race, stages)
            stage_soups = [self.gen_soup(url, table=False) for url in upcoming_urls]
            startlist_soup = self.gen_soup(startlist_url, table=False)

            # Finally looping over all the upcoming stages to generate startlists linked with metadata.
            for stage_soup in stage_soups:
                temp_data = self.get_startlist(startlist_soup, stage_soup)
                for key in data_startlists:
                    data_startlists[key].extend(temp_data[key])

            # Finally converting to a dataframe, as this is most convenient to return
            data_startlists_df = pd.DataFrame(data_startlists)

        # Finally the appropriate data frames are returned conditional on the arguments.
        if results and not startlist:
            return data_results_df
        elif startlist and not results:
            return data_startlists_df
        else:
            return data_results_df, data_startlists_df





