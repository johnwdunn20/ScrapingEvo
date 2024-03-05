# execute with python3 -m examples.example 
from main import ScrapeEvoSkis

twin_tip = ScrapeEvoSkis()

# setting count_total_skis to 40 for testing purposes - will only get the first page
# twin_tip.scrape(url='https://www.evo.com/shop/ski/skis/twin-tip', count_total_skis=40, printURls=True)

# search csv for skis
twin_tip.search(keywords=['RMU'])