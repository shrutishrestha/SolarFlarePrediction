import pandas as pd
import numpy as np

def count_class(dataf):
    df = dataf.copy()
    df.replace(np.nan, str(0), inplace=True)
    df.replace('', str(0), inplace=True)
    df['class'] = df['goes_class'].astype('str').apply (lambda row: row[0:1])
    search_list = [['A', 'B', '0'], ['C'], ['M'], ['X']]
    for i in range(4):
        search_for = search_list[i]
        mask = df['class'].apply(lambda row: row).str.contains('|'.join(search_for))
        present = df[mask]
        print(present['class'].value_counts())

#This is to binarize the labels into 0 and 1 class where 0 is Non-Flare and 1 is Flare
#modes='M' is used for greater than or equal to M1.0 class flares
#modes= 'C' is used for greater than or equal to C1.0 class flares
def binarize(df, modes):
    #Empty space and nan values are filled with 0 in the goes_class column
    df.replace(np.nan, str(0), inplace=True)
    df.replace('', str(0), inplace=True)

    #Replacing X and M class flare with 1 and rest with 0 in goes_class column
    if(modes=='M'):
        for i in range(len(df)):
            if (df.goes_class[i][0] == 'X' or  df.goes_class[i][0] == 'M'):
                df.goes_class[i] = 1
            else:
                df.goes_class[i] = 0
    else:
        for i in range(len(df)):
            if (df.goes_class[i][0] == 'X' or  df.goes_class[i][0] == 'M' or df.goes_class[i][0] == 'C'):
                df.goes_class[i] = 1
            else:
                df.goes_class[i] = 0
    return df

#This function is used to convert the timestamps to name of images that we use in this research
def date_to_filename(dataf):
    df = dataf.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

    #Renaming label(Date) to this format of file hmi.sharp_cea_720s.1.20100501_000000_TAI.magnetogram.fits
    df['filename'] = 'hmi.sharp_cea_720s.'+ df.harpnum.astype(str)+ '.' \
        + df.timestamp.dt.year.astype(str) + \
        + df.timestamp.dt.month.map("{:02}".format).astype(str) \
        + df.timestamp.dt.day.map("{:02}".format).astype(str) + '_' \
        + df.timestamp.dt.hour.map("{:02}".format).astype(str) \
        + df.timestamp.dt.minute.map("{:02}".format).astype(str) \
        + df.timestamp.dt.second.map("{:02}".format).astype(str) + '_TAI.magnetogram.fits'
    
    return df

#Creating time-segmented 4-Fold CV Dataset, where 9 months of data is used for training and rest 3 for validation
def create_CVDataset(df):
    search_list = [['01', '02', '03'], ['04', '05', '06'], ['07', '08', '09'], ['10', '11', '12']]
    for i in range(4):
        search_for = search_list[i]
        mask = df['timestamp'].astype(str).apply(lambda row: row[5:7]).str.contains('|'.join(search_for))
        train = df[~mask]
        val = df[mask]
        train = date_to_filename(train)
        val = date_to_filename(val)
        print(train['goes_class'].value_counts())
        print(val['goes_class'].value_counts())
        # Dumping the dataframe into CSV with label as Date and goes_class as intensity
        train.to_csv(r'../harp_label/M_Bin_Fold_update{i}_train.csv'.format(i=i+1), index=False, header=True, columns=['filename', 'goes_class'])
        val.to_csv(r'../harp_label/M_Bin_Fold_update{i}_val.csv'.format(i=i+1), index=False, header=True, columns=['filename', 'goes_class'])

#Load Harp-to-active region associated source for Goes Flare X-ray Flux 
data = pd.read_csv (r'../harp_label/bi_daily_label_update.csv')
df = pd.DataFrame(data, columns= ['harpnum','timestamp', 'goes_class'])
count_class(df)
temp_df = binarize(df, 'M')
label_df = date_to_filename(temp_df)
create_CVDataset(temp_df)
print(label_df['goes_class'].value_counts())
label_df.to_csv(r'../harp_label/final_label_update.csv', index=False, header=True, columns=['harpnum', 'timestamp', 'filename', 'goes_class'])