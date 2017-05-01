import pandas as pd, numpy as np
 
def get_dummies(df, feature_list, drop_first=True):
    
    df = df[feature_list]
    df_list = []
    
    for i in range(df[feature_list].shape[1]):
        vec = df[feature_list].ix[:,i].as_matrix()
        vec_name = df[feature_list].ix[:,i].name
    
        in_vec = list(set(vec))
        dummies = np.zeros((len(vec), len(in_vec)))
    
        for i in range(len(vec)):
            for j in range(len(in_vec)):
                if vec[i] == in_vec[j]:
                    dummies[i,j] = 1
                
        d_df = pd.DataFrame(dummies)
        d_df.columns = [(str(vec_name) + '_' + str(ele)) for ele in in_vec]
    
        if drop_first == True:
            if len(in_vec) > 2:
                d_df = d_df.ix[:,1:]
            else:
                d_df = d_df.ix[:,1]
        
        df_list.append(d_df)

    df_output = pd.DataFrame()
    
    for i in range(0, len(df_list)):
        df_output = pd.concat([df_output, df_list[i]],axis=1)
        
    return df_output

