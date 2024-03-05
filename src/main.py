import os
import requests
import bs4
import pandas as pd
from random import randint
from time import sleep
import math
from datetime import datetime
import os


class ScrapeEvoSkis():
    def __init__(self, csv_location=None):
        # if csv_location is None, store in current directory. *** this needs to be updated to store in wherever it's called from
        if csv_location is None:
            # Get the directory of the current file (main.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Append the file name to the directory
            self.csv_location = os.path.join(current_dir, 'raw_data.csv')
        else:
            self.csv_location = csv_location
        # Store last scraped date
        self.last_scraped = None

    def scrape(self, url, count_total_skis=None, printURls=False):
        
        # hardcoded for now, should get by scraping
        if not count_total_skis:
            count_total_skis = 118

        # list of skis
        ski_list = []

        # skis to search for - will need to scrape to get a full list
        for page_num in range(1, math.ceil(count_total_skis / 40) + 1):

            # Expect 40 skis per page (except the last page)
            url = f'{url}/p_{page_num}'
            page = requests.get(url)
            soup = bs4.BeautifulSoup(page.content, 'html.parser')

            for ski_link in soup.find_all('div', class_='product-thumb-details'):
                try:
                    # now need to actually get the href from this tag
                    links = ski_link.find('a', href=True)['href']
                    ski_list.append(links)
                    countSkis += 1
                except:
                    # Need to print out error messages
                    continue

            # sleep to not overload Evo's servers
            sleep(randint(1, 6))

        # results
        hyper_link = []
        ski = []
        title = []
        description = []
        content = []

        # Get info for individual skis
        for ski_name in ski_list:

            url_individual_ski = f'https://www.evo.com{ski_name}'
            page = requests.get(url_individual_ski)
            if printURls:
                print(url_individual_ski) 

            soup = bs4.BeautifulSoup(page.content, 'html.parser')

            # Get the Content Description
            content_messy = str(soup.find('p',itemprop=True))

            content_messy_bs = bs4.BeautifulSoup(content_messy, features='lxml')

            for i in content_messy_bs.findAll('a'):
                i.replaceWithChildren()

            ski_content_desc = (str(content_messy_bs).replace('<html><body><p itemprop="description">','').replace('</p></body></html>',''))


            # Get the top detail section
            for detail in soup.find_all('div', class_='pdp-feature'):

                hyper_link.append(url_individual_ski)
                ski.append(ski_name.split('/')[-1])
                content.append(ski_content_desc)
                
                # these should be the column headers - note they aren't the same in all pages
                title.append('Detail - ' + str(detail.find('h5')).replace('<h5>','').replace('</h5>',''))
                
                #  multiple 'em' tags in an h5 - so need another for loop        
                individual_descriptions = []

                for data in detail.find_all('div', class_='pdp-feature-description'): 

                    individual_descriptions.append(str(detail.find('em')).replace('<em>','').replace('</em>','') + ' - ' + str(detail.find('span')).replace('<span>','').replace('</span>',''))

                # now join these items together
                description.append('; '.join(individual_descriptions))

            # bottom spec section - get titles
            titleCounter = 0
            for spec_title in soup.find_all('span', class_ = 'pdp-spec-list-title'):

                hyper_link.append(url_individual_ski)
                
                ski.append(ski_name.split('/')[-1])

                content.append(ski_content_desc)

                title.append('Spec - ' + str(spec_title.find('strong')).replace('<strong>', '').replace('</strong>', ''))

                titleCounter += 1
            
            # bottom spec section - get descriptions
            spec_counter = 0
            for spec_desc in soup.find_all('span', class_ = 'pdp-spec-list-description'):
                description.append(str(spec_desc).replace('<span class="pdp-spec-list-description">', '').replace('</span>', ''))

                # As the above Titles and Descriptions are broken into 2 loops, adding checks to confirm they're the same length
                if titleCounter == spec_counter:
                    break 

            # now accounting for scenarios where titleCounter > specDesc
            while len(title) > len(description):
                hyper_link.pop()
                ski.pop()
                title.pop()
                content.pop()

            # sleep
            sleep(randint(2, 10))

        # check lengths of lists
        # print(len(hyper_link), len(ski), len(content), len(title), len(description))   

        # put it in a dataframe
        df_raw = pd.DataFrame({
            'Hyperlink': hyper_link, 'Ski': ski, 'Full Description': content, 'Section Title': title, 'Description': description
        })

        # Make sure everything's a string
        df_raw= df_raw.astype(str)

        # will need to join on HyperLink to get ski in here
        pivoted_df = df_raw[['Hyperlink', 'Section Title', 'Description']].pivot_table(index = 'Hyperlink', columns= 'Section Title', values = 'Description', aggfunc = lambda x: ' ;'.join(x))

        skiHyperlink = df_raw[['Hyperlink', 'Ski', 'Full Description']].drop_duplicates()
        final_df = skiHyperlink.join(pivoted_df, on = 'Hyperlink', how = 'inner')
        
        # save to csv
        final_df.to_csv(self.csv_location, index=False)
        
        # update last scraped date if successful
        self.last_scraped = datetime.now()
        
    # def scrape_threads(self, url, count_total_skis, printURls=False):
    #     pass
    
    # Internal method to check if csv exists and has data before searching or organizing it
    def _check_for_csv(self):
        if not self.last_scraped:
            return 'Scrape and populate data before searching it'
        
        # check if csv exists and has data
        if os.path.exists(self.csv_location):
            # check if it has data
            df = pd.read_csv(self.csv_location)
            if len(df) == 0:
                return 'Scrape and populate data before searching it'
                
        else:
            return 'Scrape and populate data before searching it'
        
    def organize_data(self):
        # check if csv exists and has data
        if os.path.exists(self.csv_location):
            # check if it has data
            df = pd.read_csv(self.csv_location)
            if len(df) == 0:
                return 'Scrape and populate data before organizing it'
            else:
                # use ml to organize columns by similarity
                # Look into spaCy and other NLP libraries
                # Store new results in a csv in location next to the original csv
                pass
                
        else:
            return 'Scrape and populate data before organizing it'
        
    def search(self):
        self._check_for_csv()