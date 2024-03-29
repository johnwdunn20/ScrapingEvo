# ScrapingEvo
Scrapes Evo to search ski specifications.

Evo's website contains a wide range of skis and each individual ski has numerous critieria. Unfortunately, the majority of this ski criteria is not searchable with Evo's built-in search functionality. Additionally, different skis have different sets of criteria.

This program will scrape each ski on Evo's website and return a horizontal table exported to Excel. You can then query/search for your desired criteria. I used SQLite in Python to query the table.

# Set Up
1. Set up virtual environment with `virtualenv venv` and activate it `source venv/bin/activate`
  a. Note: Windows commands are slightly different
2. In the virtual environment shell, run `pip install -r requirements.txt`

# Instructions
1. Use Evo's built in search functionality to limit your results set (I filtered to all Men's skis) in order to limit the number of skis you need to scrape and eventually query. Copy this link and assign _myUrl_ to it
2. Assign the number of search results to _countSkis_. This number if available in the top left corner of your search results.
3. Assign the pathway where you want to create your Excel to _myPathway_.
4. You can then query this dataset with whatever criteria you'd like.


