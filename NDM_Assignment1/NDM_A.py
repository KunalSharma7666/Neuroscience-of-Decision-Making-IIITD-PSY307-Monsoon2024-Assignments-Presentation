import matplotlib.pyplot as plt
import scipy.io

#Loading data from the .mat file
dataset_A = scipy.io.loadmat('dataset_A.mat')
dataset_H = scipy.io.loadmat('dataset_H.mat')

# Accessing data where: Face data is stored in index 0, Text data is stored in index 1, Speech data is stored in index 2

face_H, text_H, speech_H = dataset_H['dataset_H'][0]
data_H = [face_H, text_H, speech_H]

face_A, text_A, speech_A = dataset_A['dataset_A'][0]
data_A = [face_A, text_A, speech_A]

# To create a figure with 6 subplots arranged in 3 rows and 2 columns
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(12, 8), sharex=True, sharey=True)
green_l=[]
red_l=[]
# Used list comprehension to define stimuli and regions
stimuli, regions = [stim for stim in ['Face', 'Text', 'Speech']], [region for region in ['H', 'A']]

i = 0
# Iterate over the stimuli types (Face, Text, Speech) using a while loop
while i < 3:
    trial = 0
    # Left column: dataset_H (Region H) for 30 trials
    while trial < 30:
        arr = []
        x = 0
        # Collecting data points from data_H[i][trial][0] using a while loop
        while x < len(data_H[i][trial][0]):
            temp = data_H[i][trial][0][x][0]
            arr.append(temp)
            x += 1
        axs[i, 0].plot(arr, [trial] * len(arr), 'bo', markersize=2)
        trial += 1

    # Define stimulus onset and offset properties
    line_info = [
        (0, 'green', 'Stimulus - Onset'),
        (1000, 'red', 'Stimulus - Offset')
    ]

    # Looping on the line information to add vertical lines
    for position, color, label in line_info:
        if color=='green':
            green_l=axs[i, 0].axvline(position, color=color, linestyle='--', label=label)
        else:
            red_l=axs[i, 0].axvline(position, color=color, linestyle='--', label=label)

    # Set title and ylabel
    axs[i, 0].set_title(f'{stimuli[i]} - Region H')
    axs[i, 0].set_ylabel('Trials')

    trial = 0
    # Right column: dataset_A (Region A) for 30 trials
    while trial < 30:
        arr = []
        x = 0
        # Collecting data points from data_A[i][trial][0] using a while loop
        while x < len(data_A[i][trial][0]):
            temp = data_A[i][trial][0][x][0]
            arr.append(temp)
            x += 1
        axs[i, 1].plot(arr, [trial] * len(arr), 'bo', markersize=2)
        trial += 1
        
    # Define positions and colors for vertical lines
    positions = [0, 1000]
    colors = ['green', 'red']

    # Looping on positions and colors to add vertical lines
    for pos, color in zip(positions, colors):
        axs[i, 1].axvline(pos, color=color, linestyle='--')

    # Set title for the subplot
    axs[i, 1].set_title(f'{stimuli[i]} - Region A')

    i += 1


# Used to Set common labels by using a single invisible axis
fig.add_subplot(111, frameon=False)  # Adding a subplot to act as the frame
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)  # Used to hide tick labels
lables = [green_l, red_l]
fig.legend(handles=lables, loc='upper right')
plt.xlabel('Time (ms)', fontsize=12)
plt.ylabel('Trial Number', fontsize=12, labelpad=20)

plt.show()
