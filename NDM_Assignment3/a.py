import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ttest_ind, ttest_rel, mannwhitneyu, wilcoxon
from scipy.stats import sem
import numpy as np
from scipy.stats import shapiro

# Helper function to calculate proportion of switches after gain and loss trials
def helper(choices, wins, losses):
    n_participants, n_trials = choices.shape
    gain_switch_rates = np.zeros(n_participants)
    loss_switch_rates = np.zeros(n_participants)

    p_idx = 0
    while p_idx < n_participants:
        l_trials = 0
        g_switches = 0
        g_trials = 0
        l_switches = 0
        t_idx = 0
        while t_idx < n_trials - 1:
            if (wins.iloc[p_idx, t_idx]) + (losses.iloc[p_idx, t_idx]) > 0:
                g_trials += 1
                if (choices.iloc[p_idx, t_idx]) != (choices.iloc[p_idx, t_idx + 1]):
                    g_switches += 1
            elif (wins.iloc[p_idx, t_idx]) + (losses.iloc[p_idx, t_idx]) < 0:
                l_trials += 1
                if (choices.iloc[p_idx, t_idx]) != (choices.iloc[p_idx, t_idx + 1]):
                    l_switches += 1
            t_idx += 1

        if g_trials > 0:
            gain_switch_rates[p_idx] = g_switches / g_trials
        else:
            gain_switch_rates[p_idx] = 0

        if l_trials > 0:
            loss_switch_rates[p_idx] = l_switches / l_trials
        else:
            loss_switch_rates[p_idx] = 0

        p_idx += 1

    return gain_switch_rates, loss_switch_rates


# Process data for both groups
grp1_choices = pd.ExcelFile('choice.xlsx').parse('group1')
grp2_choices = pd.ExcelFile('choice.xlsx').parse('group2')
grp1_wins = pd.ExcelFile('win.xlsx').parse('group1')
grp2_wins = pd.ExcelFile('win.xlsx').parse('group2')
grp1_losses = pd.ExcelFile('loss.xlsx').parse('group1')
grp2_losses = pd.ExcelFile('loss.xlsx').parse('group2')

grp1_gain_rates, grp1_loss_rates = helper(grp1_choices, grp1_wins, grp1_losses)
grp2_gain_rates, grp2_loss_rates = helper(grp2_choices, grp2_wins, grp2_losses)

# Calculate means and standard errors for plotting
mean_grp1 = [np.mean(grp1_gain_rates), np.mean(grp1_loss_rates)]
err_grp1 = [sem(grp1_gain_rates), sem(grp1_loss_rates)]
mean_grp2 = [np.mean(grp2_gain_rates), np.mean(grp2_loss_rates)]
err_grp2 = [sem(grp2_gain_rates), sem(grp2_loss_rates)]

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
x_labels = ['Gain Trials', 'Loss Trials']

# Group 1
axes[0].bar(x_labels, mean_grp1, yerr=err_grp1, capsize=5, alpha=0.7)
axes[0].set_title('Group 1')
axes[0].set_ylabel('Mean Proportion of Switches')
axes[0].set_ylim(0, 1)

# Group 2
axes[1].bar(x_labels, mean_grp2, yerr=err_grp2, capsize=5, alpha=0.7)
axes[1].set_title('Group 2')

plt.tight_layout()
plt.show()

# Printing results for Shapiro-Wilk Normality Test
print("\nShapiro-Wilk Normality Test Results:")
print("-" * 35)
print(f"Group 1 Gain Trials: Statistic={shapiro(grp1_gain_rates).statistic}, P-value={shapiro(grp1_gain_rates).pvalue}")
print(f"Group 1 Loss Trials: Statistic={shapiro(grp1_loss_rates).statistic}, P-value={shapiro(grp1_loss_rates).pvalue}")
print(f"Group 2 Gain Trials: Statistic={shapiro(grp2_gain_rates).statistic}, P-value={shapiro(grp2_gain_rates).pvalue}")
print(f"Group 2 Loss Trials: Statistic={shapiro(grp2_loss_rates).statistic}, P-value={shapiro(grp2_loss_rates).pvalue}")


# i) Between groups comparison
if shapiro(grp2_gain_rates).pvalue < 0.05:
    gain_test = mannwhitneyu(grp1_gain_rates, grp2_gain_rates)
else:
    gain_test = ttest_ind(grp1_gain_rates, grp2_gain_rates, equal_var=False)

if shapiro(grp2_loss_rates).pvalue < 0.05:
    loss_test = mannwhitneyu(grp1_loss_rates, grp2_loss_rates)
else:
    loss_test = ttest_ind(grp1_loss_rates, grp2_loss_rates, equal_var=False)

# ii) Within groups comparison (gain vs loss within each group)
if shapiro(grp1_gain_rates).pvalue > 0.05 and shapiro(grp1_loss_rates).pvalue > 0.05:
    grp1_gain_loss_test = ttest_rel(grp1_gain_rates, grp1_loss_rates)
else:
    grp1_gain_loss_test = wilcoxon(grp1_gain_rates, grp1_loss_rates)

if shapiro(grp2_gain_rates).pvalue < 0.05 or shapiro(grp2_loss_rates).pvalue < 0.05:
    grp2_gain_loss_test = wilcoxon(grp2_gain_rates, grp2_loss_rates)
else:
    grp2_gain_loss_test = ttest_rel(grp2_gain_rates, grp2_loss_rates)

# Printing results for Mann-Whitney U Statistical Test
print("\nMann-Whitney U Statistical Test Results:")
print("-" * 39)
print(f"Gain Trials Between Groups: Statistic={gain_test.statistic}, P-value={gain_test.pvalue}")
print(f"Loss Trials Between Groups: Statistic={loss_test.statistic}, P-value={loss_test.pvalue}")

# Printing results for Wilcoxon Signed-Rank Statistical Test
print("\nWilcoxon Signed-Rank Statistical Test Results:")
print("-" * 45)
print(f"Within Group 1 (Gain vs Loss): Statistic={grp1_gain_loss_test.statistic}, P-value={grp1_gain_loss_test.pvalue}")
print(f"Within Group 2 (Gain vs Loss): Statistic={grp2_gain_loss_test.statistic}, P-value={grp2_gain_loss_test.pvalue}\n")
