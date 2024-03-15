import streamlit as st
import xarray as xr
import kdephys as kde
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import os
from open_ephys.analysis import Session

subject = st.text_input('Subject Name', '')

directory = f'/Volumes/slap_mi/slap_mi/data/{subject}/habituation'
folders = os.listdir(directory)

folders = [f for f in folders if 'day' in f]
folders.sort()

recording = st.selectbox('Recording', folders)
node = st.number_input('Record Node', 0)

new_directory = f'/Volumes/slap_mi/slap_mi/data/{subject}/habituation/{recording}/'

oe_session = Session(new_directory)
rec = oe_session.recordnodes[node].recordings[0]
_data = rec.continuous[0]
data = rec.continuous[0].get_samples(start_sample_index=0, end_sample_index=10000000000000000000)

if len(data.shape) == 2:
    data = data[:, 0]

data = data.flatten()
time = np.array(_data.timestamps[:].astype('float64'))
t = time - time[0]

fs = round(1 / np.mean(np.diff(t)))

# -------------------------- Xarray Data ----------------------------------------------------------------
xr_data = xr.DataArray(data, dims=['time'], coords={'time': t})
frq, t, spg = kde.xr.spectral.single_spectrogram_welch(xr_data.data, fs=fs, nperseg=20000, noverlap=10000)
xarray_spg = xr.DataArray(
        spg,
        dims=("frequency", "time"),
        coords={
            "frequency": frq,
            "time": t,
        }
    )
delta = kde.xr.spectral.get_bandpower(xarray_spg, f_range=(0.5, 4))

#--------------------------------Delta Bandpower--------------------------------------
dp = delta.smooth(4)
f, ax = plt.subplots(1, 1, figsize=(30, 9))
ax.plot(dp.time, dp.data, color='black', linewidth=1.5)
ax.set_title(f'{subject} | {recording} | Delta Bandpower')
#ax.set_ylim(0, 1.5)
st.pyplot(f)

# --------------------------- SPG Over Time -------------------------------------------
f2, ax2 = plt.subplots(figsize=(30, 15))
ax2 = kde.plot.main.spectro_plotter(xarray_spg.sel(frequency = slice(0, 35)), ax=ax2)
ax2.set_title(f'{subject} | {recording} | Spectrogram')
st.pyplot(f2)

# ---------------------------- PSD ---------------------------------------------------
f3, ax3 = plt.subplots(figsize=(30, 15))
psd = xarray_spg.mean(dim='time')
ax3.plot(psd.frequency, psd.data, color='black', linewidth=1.5)
ax3.set_xlim(0, 80)
ax3.set_title(f'{subject} | {recording} | PSD')
st.pyplot(f3)