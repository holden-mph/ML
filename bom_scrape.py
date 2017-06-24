# Box Office Mojo Scraper
from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import time

def main():

    start = time.time()
    url_start = "http://www.boxofficemojo.com"
    header = {'User-agent': 'Mozilla/5.0'}
    
    studio_urls = ["http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=buenavista.htm",
                   "http://www.boxofficemojo.com/studio/chart/?view=majorstudio&view2=&yr=2017&timeframe=yty&sort=&order=&studio=universal.htm",
                   "http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=wb-newline.htm",
                   "http://www.boxofficemojo.com/studio/chart/?view=majorstudio&view2=calendar&yr=2017&timeframe=yty&sort=&order=&studio=fox.htm",
                   "http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=paramount.htm",
                   "http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=pantelion.htm",
                   "http://www.boxofficemojo.com/studio/chart/?view=company&view2=&yr=2017&timeframe=yty&sort=&order=&studio=tristar.htm"]
    
    studios = ['Disney', 'Universal', 'Warner Bros.', 'Fox', 'Paramount', 'Lionsgate', 'Sony Pictures']
    
    summary_df = pd.DataFrame()
    ft_df = pd.DataFrame()
    interval = 3
    n_cols = 8
    
    for i in range(len(studio_urls)):
        query = BeautifulSoup((requests.get(studio_urls[i],headers=header)).text, 'lxml')
        n_rows = len(query.find('table', {'bgcolor': '#ffffff'})) - 4
        table, ft = [], []
        time.sleep(interval)
        print("\r","Preparing to scrape",studios[i]+" content...", end = '\r', sep = ' ', flush = True)
        
        for j in range(1, n_rows):
            rows_main = [query.find('table', {'bgcolor': '#ffffff'}).findAll('tr')[j].findAll('td')[k].text for k in range(n_cols)]
            mov_url = url_start + query.find('table', {'bgcolor': '#ffffff'}).findAll('tr')[j].find('a')['href']
            mov_query = BeautifulSoup((requests.get(mov_url,headers=header)).text, 'lxml')
            time.sleep(interval)
            opening_wknd = mov_query.findAll('div', {'class': 'mp_box_content'})[1].find('tr').findAll('td')[-1].text
            tot_gross = mov_query.find('div', {'class': 'mp_box_content'}).find('td', {'align': 'right', 'width': '35%'}).text
            f_url = mov_url.replace('?','?page=intl&')
            f_query = BeautifulSoup((requests.get(f_url,headers=header)).text, 'lxml')
            time.sleep(interval)
            rows_main.append(studios[i])
            table.append(rows_main)
            
            if len(f_query.find('table', {'border': '3'}).findAll('tr')) > 4:   
                
                for x in range(3, len(f_query.find('table', {'border': '3'}).findAll('tr'))-1):
                    try:
                        rows_ft = [f_query.find('table', {'border': '0', 'cellspacing': '1', 'cellpadding': '3'}).findAll('tr')[x].findAll('td')[y].text for y in range(7)]
                        rows_ft.append(studios[i])
                        rows_ft.append(f_query.findAll('font', {'face': 'Verdana'})[1].text)
                        ft.append(rows_ft)
                    except:
                        rows_ft.append([''])
                        ft.append([''])
                                  
                ft.append(['United States', '', '', opening_wknd, '', tot_gross, ''
                                      ,studios[i], f_query.findAll('font', {'face': 'Verdana'})[1].text])
    
                progress = round((j/n_rows)*100,0)
                print("\r",studios[i]+":","%.0f"% progress+"% complete                                      ", end = '\r', sep = ' ', flush=True)
        
        time.sleep(1)
        print("\r",studios[i]+":","100% complete", end = '\r', sep = ' ', flush = True)
                    
        table = pd.DataFrame(table)
        ft = pd.DataFrame(ft)
        ft = ft.iloc[:,:9]
        summary_df = pd.concat([summary_df, table], axis = 0)
        ft_df = pd.concat([ft_df, ft], axis = 0)
    
    summary_df.columns = ['Rank', 'Movie Title', 'Studio', 'Gross', 'Theaters', 'Total Gross', '% of Total', 'Open', 'Provider']
    ft_df.columns = ['Country', 'Dist.', 'Release Date', 'Opening Wknd', '% of Total', 'Total Gross', 'As Of', 'Provider','Movie Title']
    
    ft_df = ft_df.dropna()
    
    def unformat(col):  
        remove = ',$' 
        for char in remove:
            col = col.replace(char, "")
        return col
    
    summary_df['Gross'] = summary_df['Gross'].apply(unformat)
    summary_df['Total Gross'] = summary_df['Total Gross'].apply(unformat)
    ft_df['Opening Wknd'] = ft_df['Opening Wknd'].apply(unformat)
    ft_df['Total Gross'] = ft_df['Total Gross'].apply(unformat)
        
    writer = pd.ExcelWriter('bom_scrape_' + datetime.datetime.now().strftime("%m.%d.%Y") + '.xlsx')
    summary_df.to_excel(writer, 'Provider Summary', index=False)
    ft_df.to_excel(writer, 'By Country and Title', index=False)
    writer.save()
    end = time.time()
    print('\r.xlsx file exported to enclosing folder. (time elapsed: {}'.format(round((end-start)/60,1)) + " minutes)", sep=' ', end = '\r', flush=True)
    
if __name__ == '__main__':
    main()
