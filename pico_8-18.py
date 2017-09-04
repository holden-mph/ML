# PICO Version 2.01
import pandas as pd
import numpy as np
import datetime

def main():
    
    ################## RULES ##################   
    europe = ['France', 'Germany', 'Italy', 'Spain']
    kroner = ['Norway', 'Sweden', 'Denmark']
    
    def get_RP(territory, WSP, CRP, VAT, is_split, margin): 
        try:
            if is_split == True:
                NRP = round(CRP*0.8) - 0.01
            elif territory in europe and WSP <= 2:
                NRP = round((VAT*WSP) / (1 - margin)*2)/2 - 0.01
            elif territory == 'UK':
                NRP = round((VAT*WSP) / (1 - margin)*2)/2 - 0.01
            elif territory in kroner:
                NRP = round((VAT*WSP) / (1 - margin),-1) - 1.0
            elif territory == 'Brazil':
                NRP = round((VAT*WSP) / (1 - margin)) - 0.10
            else:
                NRP = round((VAT*WSP) / (1 - margin)) - 0.01
        except:
            return 'Missing Info'
        return NRP
    
    def good_discount_good_margin(NRP, territory, WSP, CRP, VAT, is_split, is_top_25, margin):
        if np.isnan(WSP):
            return NRP
        else:
            threshold = -0.5
            if (NRP / CRP - 1 <= threshold) and (is_top_25 == False) and (is_split == False):
                margin = 0.26
                NRP = get_RP(territory, WSP, CRP, VAT, is_split, margin)
            return NRP
    
    def top_25(NRP, is_top_25, territory, WSP, CRP, VAT, is_split, margin):
        if np.isnan(WSP):
            return NRP
        else:
            if (is_top_25 == True) and (is_split == False):
                margin = 0.12
                NRP = get_RP(territory, WSP, CRP, VAT, is_split, margin)
            return NRP
    
    def hddwsp_equals_sdrwsp(hddwsp_bool, SD_CRP, NRP, is_split):
        if (hddwsp_bool == True) and (is_split == False):
            return SD_CRP
        else:
            return NRP
    
    def sdwsp_equals_hdwsp(SD_WSP, SD_NRP, HD_WSP, HD_NRP, is_split):
        if (SD_WSP == HD_WSP) and (SD_NRP != HD_NRP) and (is_split == False):
            return HD_NRP
        else:
            return SD_NRP
    
    def hdwsp_greater_sdwsp(territory, SD_WSP, SD_NRP, HD_WSP, HD_NRP, is_split):
        if (HD_WSP > SD_WSP) and (HD_NRP <= SD_NRP) and (is_split == False):
            if territory in europe or territory == 'UK':
                return HD_NRP + 0.5
            else:
                return HD_NRP + 1.0
        else:
            return HD_NRP
              
    ################## MAIN ##################
    
    print('Loading Excel File...')
    df = pd.read_excel('PICO_Input.xlsx', sheetname='Input')
    df = df.iloc[:,:-1]
    df = pd.concat([df, pd.DataFrame(np.zeros((df.shape[0], 2)))], axis = 1)
    cols = list(df.columns)
    cols[-2:] = ['SD Discounted RPs', 'HD Discounted RPs']
    df = df.as_matrix()
    
    def low_margin(NRP, territory, WSP):
        if (territory in europe and WSP <= 2) or territory == 'UK':
            return NRP + 0.5
        elif territory in kroner:
            return NRP + 10
        else:
            return NRP + 1
    
    def insufficient_discount(NRP, CRP):
        if NRP == CRP:
            return 'Insufficient discount'
        else:
            return NRP
        
    def get_margin(VAT,WSP,NRP):
        try:
            return (1 - ((VAT*WSP)/NRP))
        except:
            pass
        
    #Main Loop
    for i in range(len(df)):
        margin = 0.175
        territory = df[i,0]
        SD_WSP = df[i,5]
        HD_WSP = df[i,6]
        SD_CRP = df[i,7]
        HD_CRP = df[i,8]
        VAT = df[i,12]
        is_split = df[i,10]
        is_top_25 = df[i,9]
        hddwsp_bool = df[i,11]
    
        df[i,-2] = get_RP(territory, SD_WSP, SD_CRP, VAT, is_split, margin)
        df[i,-1] = get_RP(territory, HD_WSP, HD_CRP, VAT, is_split, margin)
        
        if is_split == False:
            try:
                df[i,-2] = good_discount_good_margin(df[i,-2], territory, SD_WSP, SD_CRP, VAT, is_split, is_top_25, margin)
                df[i,-1] = good_discount_good_margin(df[i,-1], territory, HD_WSP, HD_CRP, VAT, is_split, is_top_25, margin)
                
                df[i,-2] = top_25(df[i,-2], is_top_25, territory, SD_WSP, SD_CRP, VAT, is_split, margin)
                df[i,-1] = top_25(df[i,-1], is_top_25, territory, HD_WSP, HD_CRP, VAT, is_split, margin)
                
                df[i,-1] = hddwsp_equals_sdrwsp(hddwsp_bool, SD_CRP, df[i,-1], is_split)
                 
                df[i,-2] = sdwsp_equals_hdwsp(SD_WSP, df[i,-2], HD_WSP, df[i,-1], is_split)
                df[i,-1] = hdwsp_greater_sdwsp(territory, SD_WSP, df[i,-2], HD_WSP, df[i,-1], is_split)
                
                if (is_split == False) and (hddwsp_bool == False):
                    sd_margin = get_margin(VAT, SD_WSP, df[i,-2])
                    hd_margin = get_margin(VAT, HD_WSP, df[i,-1])
                    if is_top_25 == False:
                        if sd_margin == None:
                            pass
                        elif sd_margin < 0.14:
                            df[i,-2] = low_margin(df[i,-2], territory, SD_WSP)
                        if hd_margin == None:
                            pass
                        elif hd_margin < 0.14:
                            df[i,-1] = low_margin(df[i,-1], territory, HD_WSP)
                    elif is_top_25 == True:
                        if sd_margin == None:
                            pass
                        elif sd_margin < 0.075:
                            df[i,-2] = low_margin(df[i,-2], territory, SD_WSP)
                        if hd_margin == None:
                            pass
                        elif hd_margin < 0.075:
                            df[i,-1] = low_margin(df[i,-1], territory, HD_WSP)
        
                df[i,-2] = insufficient_discount(df[i,-2], SD_CRP)
                df[i,-1] = insufficient_discount(df[i,-1], HD_CRP)       
                        
                if np.isnan(SD_CRP):
                    df[i,-2] = 'Missing Info'
                if np.isnan(HD_CRP):
                    df[i,-1] = 'Missing Info'
            
            except:
                df[i,-2] = 'Error'
                df[i,-1] = 'Error'
        else:
            pass
          
    df = pd.DataFrame(df)
    df.columns = cols
    
    filename = 'PICO_Output_'+str(datetime.datetime.now().strftime("%m-%d-%Y"))+'.csv'
    df.to_csv(filename, encoding='utf-8', index=False)
    print('Output file exported to enclosing folder.')
     
if __name__ == '__main__':
    main()
