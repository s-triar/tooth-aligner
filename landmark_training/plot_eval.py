import matplotlib.pyplot as plt

# Data
data = [
    [0, 'ld_saved_de_pop10_iter1000_f05_cr07_no_candidate.csv', 'BOTH', 33930.91286234167, 3.3903114420706224],
    [1, 'ld_saved_de_pop10_iter1000_f05_cr07_no_candidate.csv', 'UPPER', 21305.600897849796, 2.6865115815107505],
    [2, 'ld_saved_de_pop10_iter1000_f05_cr07_no_candidate.csv', 'LOWER', 12625.311964491873, 2.0680587991262698],
    [3, 'ld_saved_de_pop100_iter100_f05_cr07_no_candidate.csv', 'BOTH', 33286.84476966829, 3.3579802599240205],
    [4, 'ld_saved_de_pop100_iter100_f05_cr07_no_candidate.csv', 'UPPER', 21160.712470305345, 2.6773612068501804],
    [5, 'ld_saved_de_pop100_iter100_f05_cr07_no_candidate.csv', 'LOWER', 12126.132299362944, 2.0267630335323212],
    [6, 'ld_saved_de_pop1000_iter10_f05_cr07_no_candidate.csv', 'BOTH', 32180.962700965974, 3.3017283548247143],
    [7, 'ld_saved_de_pop1000_iter10_f05_cr07_no_candidate.csv', 'UPPER', 20241.58358416189, 2.6185692674025107],
    [8, 'ld_saved_de_pop1000_iter10_f05_cr07_no_candidate.csv', 'LOWER', 11939.37911680409, 2.0110955026722612]
]

# Extract columns for plotting
column1 = [row[1] for row in data]
column2 = [row[2] for row in data]
column4 = [row[4] for row in data]

# Create unique labels for the nested x-axis
x_labels = [f"{c1} - {c2}" for c1, c2 in zip(column1, column2)]

# Assign colors based on the labels
colors = []
for label in x_labels:
    if 'BOTH' in label:
        colors.append('red')
    elif 'UPPER' in label:
        colors.append('blue')
    elif 'LOWER' in label:
        colors.append('green')

# Plot based on nested x-axis (column 1 and column 2), and column 4 on the y-axis
plt.bar(range(len(data)), column4, color=colors)
plt.xticks(range(len(data)), x_labels, rotation='vertical')

# Add label values on top of each bar
for i, v in enumerate(column4):
    plt.text(i, v, str(round(v, 2)), ha='center', va='bottom')

plt.xlabel('Column 1 - Column 2')
plt.ylabel('Column 4')
plt.title('Bar Chart - Columns 1, 2, and 4')
plt.tight_layout()
plt.show()