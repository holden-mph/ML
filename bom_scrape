# Box Office Mojo Web Scraper
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

url_start = "http://www.boxofficemojo.com"

studio_urls = ["http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=buenavista.htm",
               "http://www.boxofficemojo.com/studio/chart/?view=majorstudio&view2=&yr=2017&timeframe=yty&sort=&order=&studio=universal.htm",
               "http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=wb-newline.htm",
               "http://www.boxofficemojo.com/studio/chart/?view=majorstudio&view2=calendar&yr=2017&timeframe=yty&sort=&order=&studio=fox.htm",
               "http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=paramount.htm",
               "http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=pantelion.htm"]

studios = ['Disney', 'Universal', 'Warner Bros.', 'Fox', 'Paramount', 'Lionsgate']

summary_df = pd.DataFrame()
foreign_tab_df = pd.DataFrame()

interval = 3
n_cols = 8

for i in range(len(studio_urls)):
    query = BeautifulSoup((requests.get(studio_urls[i])).text, 'lxml')
    n_rows = len(query.find('table', {'bgcolor': '#ffffff'})) - 4
    table, foreign_table = [], []
    time.sleep(interval)
    
    for j in range(1, n_rows):
        row_data = [query.find('table', {'bgcolor': '#ffffff'}).findAll('tr')[j].findAll('td')[k].text for k in range(n_cols)]
        mov_url = url_start + query.find('table', {'bgcolor': '#ffffff'}).findAll('tr')[j].find('a')['href']
        mov_query = BeautifulSoup((requests.get(mov_url)).text, 'lxml')
        time.sleep(interval)
        opening_wknd = mov_query.findAll('div', {'class': 'mp_box_content'})[1].find('tr').findAll('td')[-1].text
        foreign_url = mov_url.replace('?','?page=intl&')
        foreign_query = BeautifulSoup((requests.get(foreign_url)).text, 'lxml')
        time.sleep(interval)
        row_data.append(studios[i])
        table.append(row_data)
        print("j = {}".format(j))
        
        for x in range(3, len(foreign_query.find('table', {'border': '3'}).findAll('tr'))-1):
            try:
                row_data_foreign = [foreign_query.find('table', {'border': '0', 'cellspacing': '1', 'cellpadding': '3'}).findAll('tr')[x].findAll('td')[y].text for y in range(7)]
                row_data_foreign.append(studios[i])
                row_data_foreign.append(foreign_query.findAll('font', {'face': 'Verdana'})[1].text)
                foreign_table.append(row_data_foreign)
            except:
                row_data_foreign.append([''])
                foreign_table.append(['']) 
            print("x = {}".format(x))       
            
        foreign_table.append(['United States', '', '', opening_wknd, '', '', ''])
                
    table = pd.DataFrame(table)
    foreign_table = pd.DataFrame(foreign_table)
    summary_df = pd.concat([summary_df, table], axis = 0)
    foreign_tab_df = pd.concat([foreign_tab_df, foreign_table], axis = 0)

foreign_tab_df = foreign_tab_df.iloc[:,:-2]
summary_df.columns = ['Rank', 'Movie Title', 'Studio', 'Gross', 'Theaters', 'Total Gross', '% of Total', 'Open', 'Provider']
foreign_tab_df.columns = ['Country', 'Dist.', 'Release Date', 'Opening Wknd', '% of Total', 'Total Gross', 'As Of', 'Provider','Movie Title']

for i in range(len(foreign_tab_df)):
    if foreign_tab_df.iloc[i,7] == None:
        foreign_tab_df.iloc[i,7] = foreign_tab_df.iloc[i-1,7]
        foreign_tab_df.iloc[i,8] = foreign_tab_df.iloc[i-1,8]
    
writer = pd.ExcelWriter('BOM_Scrape.xlsx') #add date to this
summary_df.to_excel(writer, 'Summary by Provider', index=False)
foreign_tab_df.to_excel(writer, 'By Title and Country', index=False)
writer.save()    

