import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import sem

def helper(choice_df, loss_df):
    num_users, num_steps = choice_df.shape
    deck_data = {d: [] for d in range(1, 5)}  # Deck proportions

    i = 0
    while i < num_users:
        deck_count = {d: 0 for d in range(1, 5)}
        loss_count = 0

        j = 0
        while j < num_steps - 1:
        
            # Loss trial and switch occurred
            if (loss_df.iloc[i, j]) < 0 and (choice_df.iloc[i, j]) != choice_df.iloc[i, j + 1]:  
                loss_count += 1
                deck_count[choice_df.iloc[i, j]] += 1
            j += 1

        # Calculating proportions for this user
        d = 1
        while d <= 4:
            if loss_count > 0:
                prop = deck_count[d] / loss_count
            else:
                prop = 0
            deck_data[d].append(prop)
            d += 1
        i += 1

    # Computing means 
    mean_data = {d: np.mean(deck_data[d]) for d in deck_data}
    #computing SEMs
    sem_data = {d: sem(deck_data[d]) for d in deck_data}
    return mean_data, sem_data

# Process data for both group1 and group2
group1_choice = pd.ExcelFile('choice.xlsx').parse('group1')
group2_choice = pd.ExcelFile('choice.xlsx').parse('group2')
group1_loss = pd.ExcelFile('loss.xlsx').parse('group1')
group2_loss = pd.ExcelFile('loss.xlsx').parse('group2')

# Calculating proportions for group 1
group1_mean, group1_sem = helper(group1_choice, group1_loss)
# Calculating proportions for group 1
group2_mean, group2_sem = helper(group2_choice, group2_loss)

# Preparing data for plotting
group1_vals = [group1_mean[d] for d in [1, 2, 3, 4]]
group1_errs = [group1_sem[d] for d in [1, 2, 3, 4]]
group2_vals = [group2_mean[d] for d in [1, 2, 3, 4]]
group2_errs = [group2_sem[d] for d in [1, 2, 3, 4]]

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
x_labels = ['Deck 1', 'Deck 2', 'Deck 3', 'Deck 4']

# plot for Group 1
axes[0].bar(x_labels, group1_vals, yerr=group1_errs, capsize=5, alpha=0.7)
axes[0].set_title('Group 1')
axes[0].set_ylabel('Mean Proportion')

# plot for Group 2
axes[1].bar(x_labels, group2_vals, yerr=group2_errs, capsize=5, alpha=0.7)
axes[1].set_title('Group 2')

plt.tight_layout()
plt.show()

# Ranking decks by mean proportions for group 1
group1_rank = sorted(group1_mean.items(), key=lambda x: x[1], reverse=True)

# Ranking decks by mean proportions for group 2
group2_rank = sorted(group2_mean.items(), key=lambda x: x[1], reverse=True)

# Print rankings for group 1
print("\nGroup 1 Rankings:")
for rank, (deck, mean) in enumerate(group1_rank, start=1):
    print(f"Rank {rank}: Deck {deck} with Mean Proportion {mean}")

# Print rankings for group 2
print("\nGroup 2 Rankings:")
for rank, (deck, mean) in enumerate(group2_rank, start=1):
    print(f"Rank {rank}: Deck {deck} with Mean Proportion {mean}")
print('\n')