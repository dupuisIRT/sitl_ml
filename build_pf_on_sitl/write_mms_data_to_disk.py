# -*- coding: utf-8 -*-
"""
This example shows for MMS missionhow:
- to download data
- to build the associated timeseries
- to plot mission data

@author: hbreuill
"""
from datetime import datetime

#AIDApy Modules
from aidapy import load_data
import aidapy.aidaxr

###############################################################################
# Define data parameters
###############################################################################
# Time Interval
start_time = datetime(2017, 1, 1, 0, 0, 0)
end_time = datetime(2018, 1, 1, 0, 0, 0)

# Dictionary of data settings: mission, product, probe, coordinates
# Currently available products: 'dc_mag', 'i_dens', and 'all'
settings = {'prod': ['i_bulkv'], 'probes': ['1'], 'coords': 'gse', "mode": "low_res"}

###############################################################################
# Download and load desired data as aidapy timeseries
###############################################################################
xr_mms = load_data(mission='mms', start_time=start_time, end_time=end_time, **settings)
print(xr_mms)
#print(xr_mms['dc_mag1'])
#print(xr_mms['dc_mag2'])
###############################################################################
# Plot the loaded aidapy timeseries
###############################################################################
#xr_mms.graphical.peek()

toto = xr_mms['i_bulkv1'].to_dataframe()


toto.to_pickle("df_mms1_ibulkv_2017.pkl")
