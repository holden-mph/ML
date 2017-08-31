from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import datetime
import time

ifilename = 'Itunes ALL Territories _ New Release Title Competitive Price Match Initiative (Global).xlsx'
sheetnames = ['de_DE','en_GB','en_US']
df_list = [pd.read_excel(ifilename, sheetname=sheetnames[i]) for i in range(len(sheetnames))]

territory_domains = ['de','co.uk','com']
url_path = '/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='
url_bases = ['https://www.amazon.' + dom + url_path for dom in territory_domains]

df_dict = {'de_DE': pd.DataFrame(), 'en_GB': pd.DataFrame(), 'en_US': pd.DataFrame()}

for t_idx in range(len(sheetnames)):

    df = df_list[t_idx]
    df = df.iloc[0:3,:] # shortening the df while testing

    territory = sheetnames[t_idx]

    title_names = df.iloc[:,0]

    placeholder = np.zeros((title_names.shape[0], 4))

    sd_vod = placeholder[:,0].reshape(title_names.shape[0],1)
    hd_vod = placeholder[:,1].reshape(title_names.shape[0],1)
    sd_est = placeholder[:,2].reshape(title_names.shape[0],1)
    hd_est = placeholder[:,3].reshape(title_names.shape[0],1)

    queries = [url_bases[t_idx] + title + ' Amazon Video' for title in title_names]

    pdp_list = []

    for i in range(len(queries)):
        try:
            header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"}
            query = BeautifulSoup((requests.get(queries[i],headers=header)).text, 'lxml')
            time.sleep(np.random.randint(4,8) * (np.random.rand(1,1) + 0.5))
            pdp_href = query.find('li', {'id': 'result_0', 'class': 's-result-item celwidget '}).find('a')['href']
            pdp_href = pdp_href.split('ref')[0]
            header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            pdp_query = BeautifulSoup((requests.get(pdp_href,headers=header)).text, 'lxml') #Opens the pdp link obtained above
            po_link = pdp_query.find('div', {'id': 'a-popover-more-purchase-options'}) #Finds html related to pop up box
            #Finds everything that shows up once you click more purchase options
            po_open = po_link.find_all('span', 
               {'class': 'oneclick dv-action-dark dv-action-purchase-button js-purchase-button dv-oneclick'})  

            popup_info = []

            print('i = ', i, '. Collecting popup_info.')

            for j in range(len(po_open)):
                popup_info.append(po_open[j].text)

            print('Sorting through popup_info to populate np array.')

            for k in range(len(popup_info)):
                split = popup_info[k].split()
                if ('Ausleihen' in split) or ('Rent' in split):
                    if 'SD' in split:
                        try:
                            sd_vod[i] = float(split[-2].replace(',','.'))
                        except:
                            sd_vod[i] = float(split[-1].replace('£','').replace('$',''))
                    elif 'HD' in split:
                        try:
                            hd_vod[i] = float(split[-2].replace(',','.'))
                        except:
                            hd_vod[i] = float(split[-1].replace('£','').replace('$',''))
                elif ('Kaufen' in split) or ('Buy' in split):
                    if 'SD' in split:
                        try:
                            sd_est[i] = float(split[-2].replace(',','.'))
                        except:
                            sd_est[i] = float(split[-1].replace('£','').replace('$',''))
                    elif 'HD' in split:
                        try:
                            hd_est[i] = float(split[-2].replace(',','.'))
                        except:
                            hd_est[i] = float(split[-1].replace('£','').replace('$',''))

            pdp_list.append(pdp_href)
            time.sleep(np.random.randint(4,8) * (np.random.rand(1,1) + 0.5))

            print('i = ', i,' was a success.')

        except:
            pdp_list.append('Error')
            print('i = ', i,' was a failure.')

    prices = pd.DataFrame(np.concatenate((sd_vod, hd_vod, sd_est, hd_est), axis=1), 
                      columns = ['SD VOD', 'HD VOD', 'SD EST', 'HD EST'])

    df_dict[territory] = pd.concat([df,prices], axis=1)
    print('df created, moving onto next territory')
