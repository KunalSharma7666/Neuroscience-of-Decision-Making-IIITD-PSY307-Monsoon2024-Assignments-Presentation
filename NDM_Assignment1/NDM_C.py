import scipy.io
import matplotlib.pyplot as plt
import numpy as np

# #Loading data from the .mat file
dataset_H = scipy.io.loadmat('dataset_H.mat')
dataset_A = scipy.io.loadmat('dataset_A.mat')

# Accessing data where: Face data is stored in index 0, Text data is stored in index 1, Speech data is stored in index 2
face_H, text_H, speech_H = dataset_H['dataset_H'][0]
data_H = [face_H, text_H, speech_H]

face_A, text_A, speech_A = dataset_A['dataset_A'][0]
data_A = [face_A, text_A, speech_A]

# Extracting the columns from each dataset
H_face = []
H_text = []
H_speech = []

i = 0
while i < 3:
    # List to store the extracted data for the current dataset
    arr1 = []
    trial = 0
    while trial < 30:
        # List to store the values from the current trial
        arr = []
        x = 0
        while x < len(data_H[i][trial][0]):
            temp = data_H[i][trial][0][x][0]
            arr.append(temp)
            x += 1
        arr1.append(arr)
        trial += 1

    # Assigning the extracted data to the appropriate dataset based on the index
    if i == 0:
        H_face = arr1
    if i == 1:
        H_text = arr1
    else:
        H_speech = arr1

    i += 1


A_face = []
A_text = []
A_speech = []

i = 0
while i < 3:
    # List to store the extracted data for the current dataset
    arr1 = []
    trial = 0
    while trial < 30:
        # List to store the values from the current trial
        arr = []
        x = 0
        while x < len(data_A[i][trial][0]):
            temp = data_A[i][trial][0][x][0]
            arr.append(temp)
            x += 1
        arr1.append(arr)
        trial += 1

    # Assigning the extracted data to the appropriate dataset based on the index
    if i==0:
        A_face=arr1
    if i==1:
        A_text=arr1
    else:
        A_speech=arr1

    i += 1

# Function to calculate average firing rate
def average_firing_rate(trials):
    firing_rates = np.zeros(1000 // 200)
    for trial in trials:
        trial = np.array(trial)  # Convert list to numpy array
        trial_spikes = trial[(trial >= 0) & (trial <= 1000)]  # Only consider spikes between 0-1000 ms
        hist, _ = np.histogram(trial_spikes, bins=np.arange(0, 1000 + 200, 200))
        firing_rates += hist
    firing_rates = firing_rates / len(trials) / (200 / 1000)  # Average over trials and convert to Hz
    return firing_rates

# Calculate average firing rates for each condition and region
fr_H_face = average_firing_rate(H_face)
fr_H_text = average_firing_rate(H_text)
fr_H_speech = average_firing_rate(H_speech)

fr_A_face = average_firing_rate(A_face)
fr_A_text = average_firing_rate(A_text)
fr_A_speech = average_firing_rate(A_speech)

# Function to determine preferred stimulus
def preferred_stimulus(fr_face, fr_text, fr_speech):
    # Created a dictionary to store the average firing rates
    avg_fr = dict(zip(['Face', 'Text', 'Speech'], map(np.mean, [fr_face, fr_text, fr_speech])))
    
    preferred_stim = max(avg_fr.items(), key=lambda x: x[1])[0]
    
    # Sorting stimuli by average firing rates in descending order
    sorted_stimuli = [stim for stim, _ in sorted(avg_fr.items(), key=lambda x: x[1], reverse=True)]
    
    return preferred_stim, sorted_stimuli, avg_fr


# Determine preferred stimulus for each neuron
pref_stim_H, order_H, avg_fr_H = preferred_stimulus(fr_H_face, fr_H_text, fr_H_speech)
pref_stim_A, order_A, avg_fr_A = preferred_stimulus(fr_A_face, fr_A_text, fr_A_speech)

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(15, 5), sharex=True, sharey=True)
time_bins = np.arange(0, 1000, 200)

# Plot for Neuron H
axs[0].plot(time_bins, fr_H_face, 'r', label='Face')
axs[0].plot(time_bins, fr_H_text, 'g', label='Text')
axs[0].plot(time_bins, fr_H_speech, 'b', label='Speech')
axs[0].set(title=f'Region H - Preferred: {pref_stim_H}\nOrder: {order_H}',  xlabel='Time (ms)', ylabel='Average Firing Rate (Hz)')
axs[0].legend(loc='best')
axs[0].grid(True)

# Plot for Neuron A
axs[1].plot(time_bins, fr_A_face, 'r', label='Face')
axs[1].plot(time_bins, fr_A_text, 'g', label='Text')
axs[1].plot(time_bins, fr_A_speech, 'b', label='Speech')
axs[1].set(title=f'Region A - Preferred: {pref_stim_A}\nOrder: {order_A}', 
           xlabel='Time (ms)', ylabel='Average Firing Rate (Hz)')
axs[1].legend(loc='best')
axs[1].grid(True)

plt.tight_layout()
plt.show()

# Printing average firing rates for Region H
print("Region H - Average Firing Rates:")
print(f"Face: {avg_fr_H['Face']:.2f} Hz | Text: {avg_fr_H['Text']:.2f} Hz | Speech: {avg_fr_H['Speech']:.2f} Hz")

# Printing average firing rates for Region A
print("Region A - Average Firing Rates:")
print(f"Face: {avg_fr_A['Face']:.2f} Hz | Text: {avg_fr_A['Text']:.2f} Hz | Speech: {avg_fr_A['Speech']:.2f} Hz")

