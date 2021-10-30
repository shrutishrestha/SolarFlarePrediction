import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np

def map_goes_NOAA_ARR_with_HARPNUM():

    #Load Original source for Goes Flare X-ray Flux 
    data = pd.read_csv (r'../label_source/goes_flares_integrated.csv')

    #Load NOAA_AR to HARPNUM MAP   
    harp = pd.read_csv (r'../label_source/allharp2noaa2.csv') 

    #Create Dataframe
    dataframe = pd.DataFrame(data, columns= ['start_time','goes_class', 'NOAA_ARS'])
    df = pd.DataFrame(harp, columns= ['DEF_HARPNUM','NOAA_ARS'], index=range(3550))

    #String to list for NOAA_ARS
    df['NOAA_ARS'] = df['NOAA_ARS'].str.strip('""').str.split(',')


    #Unstack NOAA_ARS per HARPNUM
    harpdf = df.explode('NOAA_ARS')

    #DROP ROWS with nan for NOAA_ARS
    dataframe = dataframe[dataframe['NOAA_ARS'].notna()]
    harpdf = harpdf[harpdf['NOAA_ARS'].notna()]

    #Convert Datatype for NOAA_ARS to int
    dataframe['NOAA_ARS']=dataframe['NOAA_ARS'].astype(int)
    harpdf['NOAA_ARS']=harpdf['NOAA_ARS'].astype(int)

    #Merge GOES file and NOAA_ARS to HARPNUM file on NOAA_ARS
    df3 = dataframe.merge(harpdf, on=['NOAA_ARS'])

    #Sort DF based on HARPNUM
    final_df = df3.sort_values(by=['DEF_HARPNUM'])
    final_df['DEF_HARPNUM']=final_df['DEF_HARPNUM'].astype(int)
    # print(df3.head)

    #Dump final_df to csv
    final_df.to_csv(r'../label_source/new_label_source.csv', index=False, header=True, columns=['DEF_HARPNUM', 'NOAA_ARS', 'start_time', 'goes_class'])

def main():
    map_goes_NOAA_ARR_with_HARPNUM()

if __name__ == "__main__":
    main()