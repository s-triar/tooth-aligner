import pandas as pd
import matplotlib.pyplot as plt

# Create the DataFrame
data = {
    'index': [0, 1, 2, 3, 4, 5, 6, 7, 8],
    'FILE': ['ld_saved_de_iter10_pop1000_f05_cr07.csv', 'ld_saved_de_iter10_pop1000_f05_cr07.csv',
             'ld_saved_de_iter10_pop1000_f05_cr07.csv', 'ld_saved_de_iter100_pop100_f05_cr07.csv',
             'ld_saved_de_iter100_pop100_f05_cr07.csv', 'ld_saved_de_iter100_pop100_f05_cr07.csv',
             'ld_saved_de_iter1000_pop10_f05_cr07.csv', 'ld_saved_de_iter1000_pop10_f05_cr07.csv',
             'ld_saved_de_iter1000_pop10_f05_cr07.csv'],
    'Rahang': ['BOTH', 'UPPER', 'LOWER', 'BOTH', 'UPPER', 'LOWER', 'BOTH', 'UPPER', 'LOWER'],
    'Total': [50070.10523582971, 28547.386519399435, 21522.718716430252, 50566.260008677156,
              27061.681050328116, 23504.57895834903, 53356.790769077634, 27670.07833078864,
              25686.712438289003],
    'RMSE': [4.118424184419927, 3.109746595574219, 2.7001655271722673, 4.138779031653915,
             3.0277443961074275, 2.8217469313703845, 4.251446062337056, 3.0615899085087035,
             2.94982386814517]
}

df = pd.DataFrame(data)

# Group by "Rahang" column
grouped = df.groupby('Rahang')

# Create the bar chart
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['skyblue', 'lightgreen', 'lightpink']
positions = [0.1, 0.9, 1.9]  # X-axis positions for the groups

for i, (name, group) in enumerate(grouped):
    ax.bar(positions[i], group['RMSE'], label=name, color=colors[i])
    for j, rmse in enumerate(group['RMSE']):
        ax.text(positions[i], rmse, f'{rmse:.2f}', ha='center', va='bottom')

ax.set_xlabel('Rahang')
ax.set_ylabel('RMSE')
ax.set_title('RMSE by Rahang')
ax.set_xticks(positions)
ax.set_xticklabels(grouped.groups.keys())
ax.legend()

plt.tight_layout()
plt.show()
