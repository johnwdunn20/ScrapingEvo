import requests
import bs4
import pandas as pd
from random import randint
from time import sleep
import math


# We can utilize Evo's current Search functionality to narrow down our results
# That way we can scrape fewer results
# Search how you'd like, then enter your URL here:

myUrl = 'https://www.evo.com/shop/ski/skis/mens' # https://www.evo.com/shop/ski/skis/mens

# After you've filtered, look for the number of results in the top left corner on Evo
# Enter that number here:

countSkis = 1 # 118

# Enter the pathway where you want to save your file, ie "desktop/results.xlsx"
# Make sure to update your pathway if you want to run this with different intial search criteria and don't want to overwrite your intiial results

myPathway = '/Users/johndunn/Documents/Coding/projects/scrapingevo/' # ie, users/YourName/Desktop/


##################################################################################################

# list of skis
skiList = []

# skis to search for - will need to scrape to get a full list
for pageNum in range(1, math.ceil(countSkis / 40) + 1):

    # I expect 40 skis per page (except the last page)

    url = f'{myUrl}/p_{pageNum}'
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    for skiLink in soup.find_all('div', class_='product-thumb-details'):
        try:
            # now need to actually get the href from this tag
            links = skiLink.find('a', href=True)['href']

            skiList.append(links)

            countSkis += 1
        except:
            continue
            # adding continue, not break in the off chance we want to get other info ?? idk 

    # sleep
    sleep(randint(1, 6))

# results
hyperlink = []
ski = []
title = []
description = []
content = []

# Get info for individual skis

# (should throw some try except blocks in here)
for skiName in skiList:

    url = f'https://www.evo.com{skiName}'
    page = requests.get(url)
    print(url) 

    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    # Get the Content Description
    
    # *** This section is probably causing errors. Need to actually append to the lists down below

    ContentMessy = str(soup.find('p',itemprop=True))

    ContentMessyBS = bs4.BeautifulSoup(ContentMessy, features='lxml')

    for i in ContentMessyBS.findAll('a'):
        i.replaceWithChildren()

    skiContentDesc = (str(ContentMessyBS).replace('<html><body><p itemprop="description">','').replace('</p></body></html>',''))


    # top detail section
    for detail in soup.find_all('div', class_='pdp-feature'):

        hyperlink.append(url)
        
        ski.append(skiName.split('/')[-1])

        content.append(skiContentDesc)

        # these should be the column headers - note they aren't the same in all pages
        title.append('Detail - ' + str(detail.find('h5')).replace('<h5>','').replace('</h5>',''))


        #  multiple 'em' tags in an h5 - so need another for loop        
        individualDescriptions = []

        for data in detail.find_all('div', class_='pdp-feature-description'): 

            individualDescriptions.append(str(detail.find('em')).replace('<em>','').replace('</em>','') + ' - ' + str(detail.find('span')).replace('<span>','').replace('</span>',''))

        # now join these items together
        description.append('; '.join(individualDescriptions))

    # bottom spec section - get titles
    titleCounter = 0
    for specTitle in soup.find_all('span', class_ = 'pdp-spec-list-title'):

        hyperlink.append(url)
        
        ski.append(skiName.split('/')[-1])

        content.append(skiContentDesc)

        title.append('Spec - ' + str(specTitle.find('strong')).replace('<strong>', '').replace('</strong>', ''))

        titleCounter += 1
    
    # bottom spec section - get descriptions
    specCounter = 0
    for specDesc in soup.find_all('span', class_ = 'pdp-spec-list-description'):
        description.append(str(specDesc).replace('<span class="pdp-spec-list-description">', '').replace('</span>', ''))

        # As the above Titles and Descriptions are broken into 2 loops, adding checks to confirm they're the same length
        if titleCounter == specCounter:
            break 

    # now accounting for scenarios where titleCounter > specDesc
    while len(title) > len(description):
        hyperlink.pop()
        ski.pop()
        title.pop()
        content.pop()

    # sleep
    sleep(randint(2, 10))

# check lengths of lists
print(len(hyperlink), len(ski), len(content), len(title), len(description))   

# put it in a dataframe
dfResults = pd.DataFrame({
    'Hyperlink': hyperlink, 'Ski': ski, 'Full Description': content, 'Section Title': title, 'Description': description
})

# now manipulate it a bit to be easier to read

# Make sure everything's a string
dfResults= dfResults.astype(str)

# will need to join on HyperLink to get ski in here
ResultsPivoted = dfResults[['Hyperlink', 'Section Title', 'Description']].pivot_table(index = 'Hyperlink', columns= 'Section Title', values = 'Description', aggfunc = lambda x: ' ;'.join(x))

skiHyperlink = dfResults[['Hyperlink', 'Ski', 'Full Description']].drop_duplicates()
finalResults = skiHyperlink.join(ResultsPivoted, on = 'Hyperlink', how = 'inner')


# not sure we need to set the index, but doing it anyway
finalResults.set_index('Ski')

finalResults.to_excel(myPathway)

print(len(skiList))    # check equals countSkis
