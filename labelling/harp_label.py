import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None 

def bi_daily_obs(df, pws, pwe):
    #Datetime 
    df['start'] = pd.to_datetime(df['start_time'], format='%Y-%m-%d %H:%M:%S')
    stop = pd.to_datetime(df['start_time'], format='%Y-%m-%d %H:%M:%S').max().normalize() + pd.Timedelta(hours=24)

    #New Empty DF
    emp = pd.DataFrame()

    #List to store intermediate results
    lis = []
    cols = ['harpnum', 'timestamp', 'goes_class']

    #Loop to check max from midnight to midnight and noon to noon
    for i in range(len(df)):
        #Date with max intensity of flare with in the 24 hour window
        emp = df[ (df.start >= pws) & (df.start <= pwe) ].sort_values('goes_class', ascending=False).head(1).squeeze(axis=0)
        if pd.Series(emp.goes_class).empty:
            ins = ''
        else:
            ins = emp.goes_class
        lis.append([df['DEF_HARPNUM'].iloc[0], pws, ins])
        pws = pws + pd.Timedelta(hours=12)
        pwe = pwe + pd.Timedelta(hours=12)
        if pwe > stop:
            break

    df_result = pd.DataFrame(lis, columns=cols)
    # print(df.head(5))
    # print('Completed!')
    return df_result


#Load Harp-to-active region associated source for Goes Flare X-ray Flux 
data = pd.read_csv (r'../label_source/harp2noaaar2goesclass.csv')
df = pd.DataFrame(data, columns= ['DEF_HARPNUM','NOAA_ARS', 'start_time', 'goes_class'])

#Get all harpnum
harp_num = df['DEF_HARPNUM'].unique()

#Subsetting dataframe based on harpnum
output_dfs = {harp: df[df['DEF_HARPNUM'] == harp] for harp in harp_num}

c=0
emp = pd.DataFrame(columns=['harpnum', 'timestamp', 'goes_class'])
for p in output_dfs:
    sub_df = None
    sub_df = output_dfs[p]
    pws = pd.to_datetime(sub_df['start_time'], format='%Y-%m-%d').min().normalize()
    pwe = pws + pd.Timedelta(hours=24) - pd.Timedelta(seconds=1)
    # print(pws, pwe)
    out_df = None
    out_df = bi_daily_obs(sub_df, pws, pwe)
    emp = pd.concat([emp, out_df], ignore_index=True)

# print(emp.head(100))
emp.to_csv(r'../harp_label/bi_daily_label.csv', index=False, header=True, columns=['harpnum', 'timestamp', 'goes_class'])