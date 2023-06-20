from asyncore import read
from re import search
import requests
from bs4 import BeautifulSoup
import os
import time
import lxml
import json
import regex as re
import csv
import pandas as pd
import random

results = []

req_headers = {'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_ga=GA1.2.388816087.1650497094; zjs_user_id=null; zg_anonymous_id=%220b7d0ed3-b758-4ad4-a1f0-4737ad390749%22; zjs_anonymous_id=%22ce604ae6-6e52-4eb9-a900-dc87730c6dbc%22; _pxvid=15bc7fb4-c101-11ec-8293-575354575075; _gcl_au=1.1.2079628194.1650497095; __pdst=61267fd3656141e2a40bc208040dd569; _cs_c=0; _fbp=fb.1.1650497094912.900739542; _pin_unauth=dWlkPVltTXhNMlZqWkRjdFlqaGtPUzAwTXpSaExXSmpabVl0WkdReU1UWTRZMkkxWm1Jeg; __gads=ID=6ac1f2a1685b549b:T=1650497110:S=ALNI_MZazlPgxusxIZEdwutYYzPMz6ydGg; zgsession=1|62a035c7-cd05-4a56-970a-574f4c6b8958; _gac_UA-21174015-56=1.1652922677.Cj0KCQjwspKUBhCvARIsAB2IYusRAbH6bxd1aytFGOExQwo2xznAmUvZQAQTf3P7WGBHVUNnWgykKPgaAnMQEALw_wcB; pxcts=95e85546-d710-11ec-9cb2-566f4e567153; _gcl_aw=GCL.1652922678.Cj0KCQjwspKUBhCvARIsAB2IYusRAbH6bxd1aytFGOExQwo2xznAmUvZQAQTf3P7WGBHVUNnWgykKPgaAnMQEALw_wcB; DoubleClickSession=true; gclid=Cj0KCQjwspKUBhCvARIsAB2IYusRAbH6bxd1aytFGOExQwo2xznAmUvZQAQTf3P7WGBHVUNnWgykKPgaAnMQEALw_wcB; zguid=24|%24ce604ae6-6e52-4eb9-a900-dc87730c6dbc; _gid=GA1.2.415141418.1654742375; KruxPixel=true; KruxAddition=true; g_state={"i_p":1654883669904,"i_l":2}; G_ENABLED_IDPS=google; utag_main=v_id:0180494b04a0001ccf7204bf50250507a00f907200942$_sn:6$_se:1$_ss:1$_st:1654880952102$dc_visit:5$ses_id:1654879152102%3Bexp-session$_pn:1%3Bexp-session; __gpi=UID=0000049f41e587b6:T=1650497110:RT=1654879204:S=ALNI_Ma0qo8EuQmEt3-pi-axTjFvxIeMVg; _hp2_id.1215457233=%7B%22userId%22%3A%227133509907332950%22%2C%22pageviewId%22%3A%226608235712755112%22%2C%22sessionId%22%3A%223812951689897794%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _cs_id=386f87e5-66bc-ab7e-e7f1-2ae9848ff828.1650497095.11.1654882163.1654882118.1.1684661095162; _derived_epik=dj0yJnU9VE1ibnRUQnhKVWV0alFBQ3hKSDdxVDBjOHFDcWo0cUcmbj1Ic3o0cUMySy1qVS1nNk5zRDdzcXhRJm09MSZ0PUFBQUFBR0tqaFZzJnJtPTEmcnQ9QUFBQUFHS2poVnM; _uetsid=666a9270e79d11ecba0e034d9cbd8e47; _uetvid=9d629bb0df8111eb8a892d62be682472; _px3=f1706a8faf711ac315a642e150d6bcce7a0b45ba0af24fce7178f121be8392f6:VO9rpKUUq84Sdsbb5xsbBX20RLVshhNvjWUhktM6OsoNoZTSMQGYagUPAuSxALLCaItYlQAhrfM5d77tmJJErg==:1000:EB5JLD1V0g9W6yGexenzu5ixqREk+N3n3CFRZ13yRDOieu7ER8JA6RaR7q8gasGlGI3W95emrIrrIfUFpvxbLCgVtpkjVVq8NtyjLvgEjhIfz2pAH9kCSUwl31KUulGl7o8E/CwG/Lm9Nfn/e7iywr0ikd9aNFRN5Bh+odexkDsHjLLh2kNIeOKuV4K67m/umwwLOEXQILBHt4Z31Hn7Hg==; _clck=1j36ocb|1|f28|0; _clsk=qhbb1p|1654906702013|1|0|b.clarity.ms/collect; JSESSIONID=A3B4066BCF56E00BAF561C7F19F32BB7; search=6|1657498847950%7Crb%3D10184-Indian-Princess-Rd-W-Jacksonville%252C-FL-32257%26zpid%3D44554412%26disp%3Dmap%26mdm%3Dauto%26sort%3Dpriorityscore%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%263dhome%3D0%09%0925290%09%09%09%09%09%09; AWSALB=P7sKeM4mIURhxeGq+1VAq9YU/mw4jgeoG7g5PLoa4V8RcxQJwhhPjjIYdKzwGV/8JI0nrhRej+5Ofp8mVW9ynvchY8SrriDNXko5clQjLt4h1sVfkSnwb1hJjzVb; AWSALBCORS=P7sKeM4mIURhxeGq+1VAq9YU/mw4jgeoG7g5PLoa4V8RcxQJwhhPjjIYdKzwGV/8JI0nrhRej+5Ofp8mVW9ynvchY8SrriDNXko5clQjLt4h1sVfkSnwb1hJjzVb; _pxff_bsco=1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
    }


search_term = '10184 Indian Princess Rd W, Jacksonville, FL 32257'

url = 'https://www.zillow.com/homes/' 
url = url + search_term.replace(", ",".dash.").replace(" ", ".dash.").replace("/", ".dash.").replace("#", ".num.").replace("-", ".dash.") + '_rb'

response = requests.get(url, headers=req_headers)
content = BeautifulSoup(response.text, 'lxml')


# if made this app would need the user to be able to drop their file in as excel or CSV
data = pd.read_excel(r'/Users/austinwilliams/CRM 2021.xlsx')
df = pd.DataFrame(data, columns=['Property Address'])
df = df.dropna()

addresses = df['Property Address'].tolist()


for i in range (0, len(addresses)):
    url = 'https://www.zillow.com/homes/' 
    link = str(addresses[i].replace(", ",".dash.").replace(" ", ".dash.").replace("/", ".dash.").replace("#", ".num.").replace("-", ".dash."))
    url = url + link + '_rb'

    response = requests.get(url, headers=req_headers)
    content = BeautifulSoup(response.text, 'lxml')
    const = content.select("[type = 'application/json']")

    firstValue = str(const[3]).index('{')
    lastValue = len(str(const[3])) - str(const[3])[::-1].index('}')

    json_script = str(const[3])[firstValue:lastValue]
    json_script = json.loads(json_script)

    try:
        for i in json.loads(json_script['apiCache']):
            data = (json.loads(json_script['apiCache'])[i])
    except KeyError:
        print('No data found')

    

    results.append({
        'address': data['property']['streetAddress'],
        'zipcode': data['property']['zipcode'],
        'city': data['property']['city'],
        'state': data['property']['state'],
        'zpid': data['property']['zpid'],
        'latitude': data['property']['latitude'],
        'longitude': data['property']['longitude'],
        'price': data['property']['price'],
        'year built': data['property']['yearBuilt'],
        'lot size (sqft)': data['property']['lotSize'],
        'home status': data['property']['homeStatus'],
        'living area (sqft)': data['property']['livingAreaValue'],
        'bathrooms': data['property']['bathrooms'],
        'bedrooms': data['property']['bedrooms'],
        'zestimate': data['property']['zestimate'],
        'url': url,
        'county ID': data['property']['countyFIPS'],
        'parcel ID': data['property']['parcelId'],     
        })
    
# this appears to work by indexing the list then the dictionary
    county_ID = results[0]['county ID']
    parcel_ID = results[0]['parcel ID']

    req_headers2 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.1055711301.1653514855; ASP.NET_SessionId=bvfcn55z0gif0xppl2h0ddjv; BIGipServerpaopropertysearch.coj.net=101433354.20480.0000',
    'Host': 'paopropertysearch.coj.net',
    'Referer': 'https://www.zillow.com/homes/10184-Indian-Princess-Rd-W-Jacksonville,-FL-32257_rb/44554412_zpid/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
# pulling tax data 
    url2 = 'https://paopropertysearch.coj.net/Basic/Detail.aspx?RE=' + parcel_ID

    response2 = requests.get(url2, headers=req_headers2)
    content2 = BeautifulSoup(response2.text, 'lxml')

# this is not working need to find how to properly pull the tax data form the duval site currenyl coming out as nonetype
    owner = content2.find('span',{'class': 'longTip'}).text
    mailing = content2.find('span',{'class': 'shortTip'}).text
    mailing2 = content2.find('span', {'id': 'ctl00_cphBody_repeaterOwnerInformation_ctl00_lblMailingAddressLine3'}).text


    results.append({
        'Owner': owner,
        'Owner Mailing Addr': mailing + ', '+ mailing2
    })

    with open('house_data.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=results[0].keys()) 
        writer.writeheader()

        for row in results:
            writer.writerow(row) 


    time.sleep(random.randint(5,20))

print('Done')