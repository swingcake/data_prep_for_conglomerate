import os
import glob
import pandas as pd


path = r'C:\your\path\here'                    
all_files = glob.glob(os.path.join(path, "*.csv"))
# len(all_files)

df_from_each_file = (pd.read_csv(f, index_col=False, header=None) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
# concatenated_df

save_path = 'C:\\your\\save\\path\\here\\'
filename = save_path + 'combined_csv.csv'

concatenated_df.to_csv( filename, index=False, header=False, encoding='utf-8-sig')
print('Merging successfull.')