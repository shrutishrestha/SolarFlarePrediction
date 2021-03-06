import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np

def map_goes_NOAA_ARR_with_HARPNUM():

    #Load Original source for Goes Flare X-ray Flux 
    data = pd.read_csv (r'../label_source/goes_flares_integrated.csv')

    #Load NOAA_AR to HARPNUM MAP   
    harp = pd.read_csv (r'../label_source/allharp2noaa2.csv') 

    #Load timestamps for harp
    time = pd.read_csv(r'../label_source/harp_min_max.csv')
    time_df = pd.DataFrame(time, columns= ['DEF_HARPNUM','Maximum', 'Minimum'], index=range(3550))

    #Create Dataframe
    dataframe = pd.DataFrame(data, columns= ['start_time','goes_class', 'NOAA_ARS'])
    df = pd.DataFrame(harp, columns= ['DEF_HARPNUM','NOAA_ARS'], index=range(3550))

    #String to list for NOAA_ARS
    df['NOAA_ARS'] = df['NOAA_ARS'].str.strip('""').str.split(',')


    #Unstack NOAA_ARS per HARPNUM
    harpdf = df.explode('NOAA_ARS')
    # print(len(harpdf))
    harpdf = harpdf.drop_duplicates() 
    # print(len(harpdf))

    #DROP ROWS with nan for NOAA_ARS
    dataframe = dataframe[dataframe['NOAA_ARS'].notna()]
    harpdf = harpdf[harpdf['NOAA_ARS'].notna()]
    # print(len(harpdf))

    #Convert Datatype for NOAA_ARS to int
    dataframe['NOAA_ARS']=dataframe['NOAA_ARS'].astype(int)
    harpdf['NOAA_ARS']=harpdf['NOAA_ARS'].astype(int)

    #Merge GOES file and NOAA_ARS to HARPNUM file on NOAA_ARS
    df3 = dataframe.merge(harpdf, on=['NOAA_ARS'], how='inner')
    df4 = df3.merge(time_df, on='DEF_HARPNUM', how='left')

    #Sort DF based on HARPNUM
    final_df = df4.sort_values(by=['DEF_HARPNUM'])
    final_df = final_df.dropna()
    final_df['DEF_HARPNUM']=final_df['DEF_HARPNUM'].astype(int)
    print(len(final_df), len(harpdf), len(dataframe))

    #Dump final_df to csv
    final_df.to_csv(r'../label_source/harp2noaaar2goesclass_update.csv', index=False, header=True, columns=['DEF_HARPNUM', 'NOAA_ARS', 'start_time', 'goes_class', 'Maximum', 'Minimum'])

def main():
    map_goes_NOAA_ARR_with_HARPNUM()

if __name__ == "__main__":
    main()