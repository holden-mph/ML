import requests, time, datetime, pandas as pd
from bs4 import BeautifulSoup

df = pd.read_excel("IMDB_Scraper_Input.xlsx", sheetname = 'Titles')
url_start = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
url_end = "&s=tt"
local_title_names = list(df['Original Title'])
url_list, soup_list, en_title_names = [], [], []
for i in range(0,len(local_title_names)):
    url_list.append(url_start + str(local_title_names[i]) + url_end)
search_interval = 3

for j in range(0,len(url_list)):
    if (requests.get(url_list[j])):
        query_soup = BeautifulSoup((requests.get(url_list[j])).text, 'lxml')
        time.sleep(search_interval)
        try:
            title_url_id = query_soup.find('td', {'class': 'result_text'}).find('a')['href']
            title_url = "http://www.imdb.com/" + title_url_id
            if (requests.get(title_url)):
                title_soup = BeautifulSoup((requests.get(title_url)).text, 'lxml')
                time.sleep(search_interval)
                title_name = title_soup.find('meta', {'property': 'og:title'}).attrs.get('content')
                en_title_names.append(title_name)
            else:
                en_title_names.append('Error using title ID')
        except:
            en_title_names.append('No results')
    else:
        print('Connection error.')
        en_title_names.append('Connection Error.')
    progress = round((j/len(url_list))*100,2)
    print("\r", "%.2f" % progress, "% complete", end = '', sep = '')
print("\r", "100% complete  ", end = '', sep = '')

df['IMDB Title Names'] = en_title_names
rearr_cols = list(df.columns)
rearr_cols.append('Placeholder')

for k in range(-1,-11,-1):
    rearr_cols[k] = rearr_cols[k-1]
    
rearr_cols[-11] = 'IMDB Title Names'
del rearr_cols[-1]
df = pd.DataFrame(df, columns=rearr_cols)

df.set_index('Extended NAV Code', inplace = True)

filename = 'IMDB_Scraper_Output_'+str(datetime.datetime.now().strftime("%m-%d-%Y"))+'.csv'
df.to_csv(filename, encoding='utf-8')
print('\nCSV exported to folder.')