import requests
import bs4
import pandas as pd
from random import randint
from time import sleep

# list of skis to search
skiList = []

# skis to search for - will need to scrape to get a full list
for pageNum in range(1, 2):  # let's just try 2 pages for now - if it works do more
    url = f'https://www.evo.com/shop/ski/skis/p_{pageNum}'
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    for skiLink in soup.find_all('div', class_='product-thumb-details'):

        # now need to actually get the href from this tag
        links = skiLink.find('a', href=True)['href']

        skiList.append(links)

    # need a sleep
    # sleep(randint(2, 10))


#

# results
ski = []
title = []
description = []

for skiName in skiList:

    url = f'https://www.evo.com{skiName}'
    page = requests.get(url)
    print(url) 

    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    # top detail section
    for detail in soup.find_all('div', class_='pdp-feature'):

        ski.append(skiName)
        title.append(detail.find('h5'))
        description.append(detail.find('em'))

    # bottom spec section
    # for spec in soup.find('')
    # commenting out for now as I think most info is contained in the above section

    # need a sleep
    sleep(randint(2, 10))

# put it in a dataframe
df = pd.DataFrame({
    'Ski': ski, 'Section Title': title, 'Description': description
})

print(df)
df.to_excel('/Users/JohnDunn/Documents/Python_Docs/Web Scraper/Test2.xlsx')


# then I'll need to cache / store my dataframe so I don't need to scrape again every time I want to change my search criteria
