import scrapy
import numpy as np

leagues= {'premier-league': 'GB1',
          'bundesliga': 'LB1',
          'laliga': 'ES1',
          'serie-a': 'IT1',
          'ligue-1': 'FR1',
          'super-lig': 'TR1',
          'campeonato-brasileiro-serie-a':'BRA1'}

class SquadValuesSpider(scrapy.Spider):
    name = "squad_values"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = ["https://www.transfermarkt.com/super-lig/startseite/wettbewerb/TR1/plus/?saison_id=2004"]

    def parse(self, response):
        table_rows = response.css('div#yw1 table.items tbody tr')

        for row in table_rows:
            season = response.css('h2.content-box-headline::text').getall()[1].strip()[-5:]
            club_name = row.css('td.hauptlink a::text').get()
            squad_val = row.css('td.rechts a::text').get()
            num_foreigners = row.css('td.zentriert::text').get()
            # get the 6th td (player mean value) for THIS club only
            player_mean_val = row.css('td:nth-child(6) ::text').get()

            yield {
                'season': season,
                'club': club_name,
                'foreigners': num_foreigners,
                'squad_total_val': squad_val,
                'player_mean_value': player_mean_val
            }

        base = self.start_urls[0][:-4]
        next_pages =   np.arange(2005,2026,1)

        for season in next_pages:
            yield response.follow(f"{base}{season}", callback=self.parse)
