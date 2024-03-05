from src.main import ScrapeEvoSkis

twin_tip = ScrapeEvoSkis(url='https://www.evo.com/shop/ski/skis/twin-tip', count_total_skis=10, printURls=True)

twin_tip.scrape()