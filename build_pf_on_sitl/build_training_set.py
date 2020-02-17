from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from aidapy import load_data


sitl_df = pd.read_pickle("DATA/df_sitl.pkl")
blabla = sitl_df.sort_values(by='START TIME')
blabla = blabla.reset_index()
blabla = blabla.drop(columns='index')

blabla['time_diff'] = blabla['END TIME'] - blabla['START TIME']
blabla['time_diff'].plot()
print(blabla['time_diff'].describe())
plt.show()
print(blabla)

# Convert the different string to float values
sitl_df.loc[sitl_df['LOCATION'] == 'nothing', 'location'] = 0
sitl_df.loc[sitl_df['LOCATION'] == 'mp', 'location'] = 1
sitl_df.loc[sitl_df['LOCATION'] == 'ms', 'location'] = 2
sitl_df.loc[sitl_df['LOCATION'] == 'tail', 'location'] = 3
sitl_df.loc[sitl_df['LOCATION'] == 'bs', 'location'] = 4
sitl_df.loc[sitl_df['LOCATION'] == 'sw', 'location'] = 5
sitl_df.loc[sitl_df['LOCATION'] == 'fs', 'location'] = 6
# Convert all the other string into NaN
sitl_df['location'] = pd.to_numeric(sitl_df['location'], errors='coerce')

# Create data frame 
start_time = pd.DataFrame() 
start_time['time'] = sitl_df['START TIME']
start_time['location'] = sitl_df['location']
start_time = start_time.set_index(start_time['time']) 
start_time.drop(['time'], axis=1, inplace=True)
start_time['origin'] = 'start'

# Create data frame 
end_time = pd.DataFrame()
end_time['time'] = sitl_df['END TIME']
end_time['location'] = sitl_df['location']
end_time = end_time.set_index(end_time['time'])
end_time.drop(['time'], axis=1, inplace=True)
end_time['origin'] = 'end'

# Remove rows when start time and end time are identical
blabla = pd.concat([start_time, end_time]).sort_index()
blabla = blabla.loc[~blabla.index.duplicated(keep=False)]

# Extract start time and end time
new_start = blabla.loc[blabla['origin'] == 'start']
new_start = new_start.drop(['origin'], axis=1)#, inplace=True)

#new_end = blabla.loc[blabla.loc[:, ('origin')] == 'end']
new_end = blabla.loc[blabla['origin'] == 'end']
new_end = new_end.drop(['origin'], axis=1)#, inplace=True)


# Add NaN before all start_time and after all end_time
toto_start = new_start.shift(-1, freq='ms')
toto_start['location'] = np.nan
toto_end = new_end.shift(1, freq='ms')
toto_end['location'] = np.nan

test = pd.concat([new_start, toto_start, new_end, toto_end])
test = test.sort_index()
test = test.loc['2017-08-20':'2017-9-15']


## MMS data
mms_df  = pd.read_pickle("df_mms.pkl")
mms_df = mms_df.reset_index(level=['mms1_fgm_b_gse_brst_l2'])

bx = mms_df.loc[mms_df['mms1_fgm_b_gse_brst_l2'] == 'x']
by = mms_df.loc[mms_df['mms1_fgm_b_gse_brst_l2'] == 'y']
bz = mms_df.loc[mms_df['mms1_fgm_b_gse_brst_l2'] == 'z']
btot = mms_df.loc[mms_df['mms1_fgm_b_gse_brst_l2'] == 'tot']

b_field = pd.DataFrame()
b_field['time'] = bx.index
b_field['Bx'] = bx['dc_mag1'].values
b_field['By'] = by['dc_mag1'].values
b_field['Bz'] = bz['dc_mag1'].values
b_field['B_tot'] = btot['dc_mag1'].values

b_field = b_field.set_index(b_field['time'])
b_field.drop(['time'], axis=1, inplace=True)

#investigation = test.loc['2017-08-20 01:30:00': '2017-08-20 01:50:00']

final = test.reindex(b_field.index, method='nearest')
final = pd.concat([final, b_field], axis=1)
final = final.resample('50ms').nearest(limit=1)

#dtype = pd.SparseDtype(float, fill_value=np.nan)
#sparse = final['location'].astype(dtype)

#events = np.split(sparse, np.where(np.isnan(sparse.to_numpy()))[0])
## removing NaN entries
#events = [ev[~np.isnan(ev.value)] for ev in events if not isinstance(ev, np.ndarray)]
## removing empty DataFrames
#events = [ev for ev in events if not ev.empty]

sparse = final['location'].to_sparse()


block_loc = zip(sparse.sp_index.blocs, sparse.sp_index.blengths)
blocks = [final.iloc[start:(start + length - 1)] for (start, length) in block_loc]


#print(blocks)

'''
for toto in blocks:#[:10]:
    vc = toto['location'].value_counts()
    #print(toto)
    print(vc)
    #toto.plot()

#plt.show()
'''
final = final.dropna(how='any')

value_counts = final['location'].value_counts()
#print(value_counts)

