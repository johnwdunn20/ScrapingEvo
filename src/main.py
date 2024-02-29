import os
import requests
import bs4
import pandas as pd
from random import randint
from time import sleep
import math
from datetime import datetime


class ScrapeEvoSkis():
    def __init__(self, csv_location=None):
        # if csv_location is None, store in current directory
        if csv_location is None:
            self.csv_location = os.getcwd() + '/raw_data.csv'
        else:
            self.csv_location = csv_location
        # Store last scraped date
        self.last_scraped = None

    def scrape(self, url, count_total_skis, printURls=False):
        print("Scraping Evo Skis")
        # add logic from ScrapeEvoSkis.py
        
        # update last scraped date if successful
        self.last_scraped = datetime.now()
        
    def scrape_threads(self, url, count_total_skis, printURls=False):
        pass
    
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
        pass