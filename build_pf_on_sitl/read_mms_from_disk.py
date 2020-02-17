import pandas as pd

## MMS data
mms_df  = pd.read_pickle("DATA/MMS/df_mms1_dcmag_2017.pkl")

#mms_df.to_hdf('DATA/MMS/df_mms1_dcmag_2017.h5', key='df', mode='w')
#mms_df = mms_df.reset_index(level=['mms1_fgm_b_gse_brst_l2'])

#toto = mms_df.resample('1S').pad()
#print(toto)
print(stop)

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

