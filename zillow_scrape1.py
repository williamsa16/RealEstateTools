from urllib import response
from wsgiref import headers
import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import pandas as pd
import time
import regex as re
import lxml
from lxml.html.soupparser import fromstring
import numbers
import json
import csv




class Zillow_Scraper():
    results = []
    req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.2.388816087.1650497094; zjs_user_id=null; zg_anonymous_id=%220b7d0ed3-b758-4ad4-a1f0-4737ad390749%22; zjs_anonymous_id=%22ce604ae6-6e52-4eb9-a900-dc87730c6dbc%22; _pxvid=15bc7fb4-c101-11ec-8293-575354575075; _gcl_au=1.1.2079628194.1650497095; __pdst=61267fd3656141e2a40bc208040dd569; _cs_c=0; _fbp=fb.1.1650497094912.900739542; _pin_unauth=dWlkPVltTXhNMlZqWkRjdFlqaGtPUzAwTXpSaExXSmpabVl0WkdReU1UWTRZMkkxWm1Jeg; __gads=ID=6ac1f2a1685b549b:T=1650497110:S=ALNI_MZazlPgxusxIZEdwutYYzPMz6ydGg; zgsession=1|62a035c7-cd05-4a56-970a-574f4c6b8958; _gac_UA-21174015-56=1.1652922677.Cj0KCQjwspKUBhCvARIsAB2IYusRAbH6bxd1aytFGOExQwo2xznAmUvZQAQTf3P7WGBHVUNnWgykKPgaAnMQEALw_wcB; pxcts=95e85546-d710-11ec-9cb2-566f4e567153; _gcl_aw=GCL.1652922678.Cj0KCQjwspKUBhCvARIsAB2IYusRAbH6bxd1aytFGOExQwo2xznAmUvZQAQTf3P7WGBHVUNnWgykKPgaAnMQEALw_wcB; DoubleClickSession=true; gclid=Cj0KCQjwspKUBhCvARIsAB2IYusRAbH6bxd1aytFGOExQwo2xznAmUvZQAQTf3P7WGBHVUNnWgykKPgaAnMQEALw_wcB; zguid=24|%24ce604ae6-6e52-4eb9-a900-dc87730c6dbc; _gid=GA1.2.415141418.1654742375; KruxPixel=true; KruxAddition=true; g_state={"i_p":1654883669904,"i_l":2}; _clck=1j36ocb|1|f27|0; G_ENABLED_IDPS=google; JSESSIONID=EC9B5B9B5F61DD14CC411FAA13B3E150; utag_main=v_id:0180494b04a0001ccf7204bf50250507a00f907200942$_sn:6$_se:1$_ss:1$_st:1654880952102$dc_visit:5$ses_id:1654879152102%3Bexp-session$_pn:1%3Bexp-session; __gpi=UID=0000049f41e587b6:T=1650497110:RT=1654879204:S=ALNI_Ma0qo8EuQmEt3-pi-axTjFvxIeMVg; _hp2_ses_props.1215457233=%7B%22ts%22%3A1654882118192%2C%22d%22%3A%22www.zillow.com%22%2C%22h%22%3A%22%2F%22%7D; _hp2_id.1215457233=%7B%22userId%22%3A%227133509907332950%22%2C%22pageviewId%22%3A%226608235712755112%22%2C%22sessionId%22%3A%223812951689897794%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _cs_id=386f87e5-66bc-ab7e-e7f1-2ae9848ff828.1650497095.11.1654882163.1654882118.1.1684661095162; _cs_s=2.5.0.1654883963603; _gat=1; _pxff_bsco=1; _px3=379bf24b7a8b85e6c60f8e5eb556fe0276136ea2f1427ff0407b21bee9e166a1:mCDKL0KAYajCqx9/pqrpikV21gCV9QW7C8ZxsTZ9yldvEEzjshqqPE25vDmwxgmKlOhDa3edDHEKFWCtIeLIbQ==:1000:a3b5HDrqSmSGpUlKZdhvGvQgf2l7PP8abmDKWVObA/jrpTGCrZOd2jP3V/WM8OR7pPeICuilJrArWrwFPf2/GIVCU0bMyk7mK8DCRXHivcYhUuLnLu/GzeSRbUhAJMBD8IBePNzXnUB1j3SSVpC9j5ToTGw+ZBG+7wc7Fr2NTUhat1SpLPIPB/pG/NJR5ZfbRZ07s0uw9xRt3oiwBc+OcA==; _uetsid=666a9270e79d11ecba0e034d9cbd8e47; _uetvid=9d629bb0df8111eb8a892d62be682472; _derived_epik=dj0yJnU9VE1ibnRUQnhKVWV0alFBQ3hKSDdxVDBjOHFDcWo0cUcmbj1Ic3o0cUMySy1qVS1nNk5zRDdzcXhRJm09MSZ0PUFBQUFBR0tqaFZzJnJtPTEmcnQ9QUFBQUFHS2poVnM; _clsk=1e4vpjk|1654883685714|18|0|b.clarity.ms/collect; AWSALB=i8blC5nsjhCZjHv8jNmeGsyBH/W5/b0bqIop7e2HQLvXBwAOM6z+ARmyOzcBT5xVy6meYrCmQy5nMi3sYlrReVdv3B+T8+qv26utv95LKqeZjI9Rir3MRsYRNrhh; AWSALBCORS=i8blC5nsjhCZjHv8jNmeGsyBH/W5/b0bqIop7e2HQLvXBwAOM6z+ARmyOzcBT5xVy6meYrCmQy5nMi3sYlrReVdv3B+T8+qv26utv95LKqeZjI9Rir3MRsYRNrhh; search=6|1657475685673%7Crect%3D30.49982264764479%252C-81.21516759960937%252C30.185751774417888%252C-82.16273840039062%26rid%3D25290%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%0925290%09%09%09%09%09%09',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform':'"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}
    def fetch(self, url, params):
        response = requests.get(url, headers=self.req_headers, params=params)
        print(response.status_code)
        return response

    def parse(self, response):
        content = BeautifulSoup(response, 'lxml')
        deck = content.find('ul', {'class':'photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution'})
        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])
                
                self.results.append({
                    'name': script_json['name'],
                    'latitude': script_json['geo']['latitude'],
                    'longitude': script_json['geo']['longitude'],
                    'floorSize': script_json['floorSize']['value'],
                    'url': script_json['url'],
                    'price': card.find('div', {'class': 'list-card-price'}).text
                })
        

    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys()) 
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)  
           

    def run(self):
        url = "https://www.zillow.com/jacksonville-fl/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Jacksonville%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-83.5840946015625%2C%22east%22%3A-79.7938113984375%2C%22south%22%3A28.70349560025298%2C%22north%22%3A31.955326288365132%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A25290%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A8%7D" 
        
        for page in range(1, 20):
            params = {
                'searchQueryState': '{"pagination":{"currentPage": %s},"usersSearchTerm":"Jacksonville, FL","mapBounds":{"west":-82.16273840039062,"east":-81.21516759960937,"south":30.185751774417888,"north":30.49982264764479},"regionSelection":[{"regionId":25290,"regionType":6}],"isMapVisible":true,"filterState":{"sort":{"value":"globalrelevanceex"},"ah":{"value":true}},"isListVisible":true}' %page
            }
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()


if __name__ == "__main__":
    scraper = Zillow_Scraper()
    scraper.run()



