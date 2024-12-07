

import scipy.io
import matplotlib.pyplot as plt
import numpy as np

#Loading data from the .mat file
dataset_A = scipy.io.loadmat('dataset_A.mat')
dataset_H = scipy.io.loadmat('dataset_H.mat')

# Accessing data where: Face data is stored in index 0, Text data is stored in index 1, Speech data is stored in index 2
face_H, text_H, speech_H = dataset_H['dataset_H'][0]
data_H = [face_H, text_H, speech_H]

face_A, text_A, speech_A = dataset_A['dataset_A'][0]
data_A = [face_A, text_A, speech_A]

green_l=[]
red_l=[]

# Define function for PSTH computation
def psth(data, duration=3000):

    num_bins = duration // 10
    psth = np.zeros(num_bins)
    
    for trial in data:
        # Extract timestamps and convert to appropriate format
        timestamps = [spike[0] for spike in trial[0]]
        # Bin the spike timestamps
        binned_spikes, _ = np.histogram(timestamps, bins=np.arange(-1000, duration - 1000 + 10, 10))
        psth += binned_spikes
    
    # Average over the number of trials
    psth /= len(data)
    return psth

# Define function for moving average smoothing
def smooth_psth(psth, window_size=50):
    window = window_size // 10  # Convert window size to number of bins
    return np.convolve(psth, np.ones(window)/window, mode='same')

window_size = 50  # ms
duration = 3000  # ms (total duration of recording)

# making figure with 6 subplots: 3 rows x 2 columns
fig, axs = plt.subplots(3, 2, figsize=(12, 8), sharex=True, sharey=True)
stimuli = ['Face', 'Text', 'Speech']

# Looping over the stimuli types (Face, Text, Speech)
for i in range(3):
    # Region H (left column)
    psth_H = psth(data_H[i] ,duration=duration)
    time_bins = np.arange(-1000, duration - 1000, 10)
    axs[i, 0].plot(time_bins, smooth_psth(psth_H, window_size=window_size), color='blue')
    green_l = axs[i, 0].axvline(0, color='green', linestyle='--', label='Stimulus Onset')  # Stimulus onset
    red_l = axs[i, 0].axvline(1000, color='red', linestyle='--', label='Stimulus Offset')  # Stimulus offset
    axs[i, 0].set_title(f'{stimuli[i]} - Region H')
    axs[i, 0].set_ylabel('Firing Rate (Hz or spikes/bin)')
    axs[i, 0].grid(True)

    # Region A (right column)
    psth_A = psth(data_A[i], duration=duration)
    axs[i, 1].plot(time_bins, smooth_psth(psth_A, window_size=window_size), color='blue')
    axs[i, 1].axvline(0, color='green', linestyle='--', label='Stimulus Onset')  # Stimulus onset
    axs[i, 1].axvline(1000, color='red', linestyle='--', label='Stimulus Offset')  # Stimulus offset
    axs[i, 1].set_title(f'{stimuli[i]} - Region A')
    axs[i, 1].grid(True)

# Set common labels and layout
lables = [green_l, red_l]
fig.text(0.5, 0.04, 'Time (ms)', ha='center', fontsize=12)
fig.text(0.04, 0.5, 'Smoothed Firing Rate', va='center', rotation='vertical', fontsize=12)
fig.legend(handles=lables, loc='upper right')
plt.show()
