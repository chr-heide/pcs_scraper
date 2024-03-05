<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT -->
## About

This repo contains python tools for scraping cycling results from procyclingstats.com. The main functionality is contained in the single class: `PcsScraper`.

The project has been created for personal use. However feel free to open an issue if you have any questions, ideas or suggestions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Installation

Getting going with the project is straigt-forward - simply follow these two steps.

1. Clone the repo
   ```sh
   git clone https://github.com/chr-heide/pcs_scraper.git
   ```
3. Set up a virtual environment (optional but recommended) and install the requirements. If you're using pip:
   ```python
   pip install -r requirements.txt
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage



### Results

As the first thing make sure to import the scraper:

```python
from pcs_scraper import PcsScraper
```

The most straight-forward use is to scrape all results from one or more use. This is easily done using the `.get_dataframe` method. For instance, the following will scrape all results from 2022 and onwards:

```python
# Initialise the class
scraper = PcsScraper(start_year=2022)
# Save results to data frame
df = scraper.get_dataframe(startlist=False)
```

The resulting dataframe will contain all results from 2022 up to the current year - both included. By default `end_year` is set to the current year, but this can be overwritten.

When specifying `startlist=False` the method will only return one data frame. Had it been set to True, instead a tuple would have been returned with the structure `(results_df, startlist_df)`.

It is also possible to scrape results of individual races instead of full years. To do this you'll need to first create a soup and table object and then pass these to the `get_results` method. Notice that it is not necessary to instantiate the class for this. As an example the following code will get the results of the second stage of Paris-Nice 2024.

```python
# Generate soup and table
soup, table = PcsScraper.gen_soup("https://www.procyclingstats.com/race/paris-nice/2024/stage-2")
# Scrape reulsts.
results_dict = PcsScraper.get_results(soup, table)
```
This returns a dictionary with the results. The dictionary can readily be converted to a pandas data frame or whichever format is preferred.

### Startlists

The package also contains functionality for getting startlists along with the same race metadata as for the results. Some of this functionality is built into the `.get_dataframe` method:

```python
# Initialise the class
scraper = PcsScraper(start_year=2024)
# Save startlist
df = scraper.get_dataframe(race = 'tour', results=False)
```

The above will generate a data frame containing startlists for all 21 stages for the upcoming Tour de France. Currently it is only possible to generate startlists for the 3 grand tours using the `.get_dataframe` method. For the other two grand tours, change `race` to either `vuelta` or `giro`. To only scrape startlists of certain stages, pass a list with the relevant stage numbers as the `stages` argument.

It is also possible to get startlist for a single race that is not a grand tour stage (although this alternative method also works fine for grand tour stages). Simply pick a URL from procyclingstats.com and do as below:

```python
# Create soups
startlist_soup = PcsScraper.gen_soup("https://www.procyclingstats.com/race/paris-nice/2024/startlist", table=False)
stage_soup = PcsScraper.gen_soup("https://www.procyclingstats.com/race/paris-nice/2024/stage-2", table=False)
# Get the startlist
startlist_dict = PcsScraper.get_startlist(startlist_soup, stage_soup)
```

This returns a startlist as a dictionary that can readily be converted to a pandas dataframe or whichever format might be preferred.

<p align="right">(<a href="#readme-top">back to top</a>)</p>