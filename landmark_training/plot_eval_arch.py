import matplotlib.pyplot as plt
import pandas as pd

filenames=[
# "hasil_evaluation_ld_based_on_arch.csv",
# "hasil_evaluation_ld_based_on_arch_no_candidate.csv"

"hasil_evaluation_ld_based_on_arch_fcr_variation_no_candidate.csv",

# "hasil_evaluation_ld_based_on_arch_w_manual.csv"
]
# folder='popiter'
folder='f_cr'
# folder='w_manual'
filename=folder+'\\'+filenames[0]


# pop iter
# _ FILE Rahang         Total      RMSE
df_arch = pd.read_csv(filename, encoding='utf-8', index_col=0)
# df_arch = df_arch.sort_values(by=['Rahang'], ascending=False)

if(len(filenames)>1):
    filename=folder+'\\'+filenames[1]

    # pop iter
    # _ FILE Rahang         Total      RMSE
    df_arch_no_candidate = pd.read_csv(filename, encoding='utf-8', index_col=0)
    # df_arch_no_candidate = df_arch_no_candidate.sort_values(by=['Rahang'], ascending=False)

    df_arch = pd.concat([df_arch, df_arch_no_candidate])

df_arch = df_arch.sort_values(by=['Rahang','FILE'], ascending=False)

print(df_arch)
# Create unique labels for the nested x-axis
def create_label_from_file(filename: str):
    names = filename.split("_")
    if len(names) == 1:
        return names
    if "0." in filename:
        return names[6]+" "+names[7]+("" if "no_candidate" not in filename else " NC")
    return names[3]+" "+names[4]+("" if "no_candidate" not in filename else " NC")

x_labels = [f"{create_label_from_file(c1)} - {c2}" for c1, c2 in zip(df_arch[:]['FILE'], df_arch[:]['Rahang'])]

# # Assign colors based on the labels
colors = []
for label in x_labels:
    if 'BOTH' in label:
        if("NC" in label):
            colors.append([1, 1, 0.3, 1])
        else:
            colors.append([1,0.4,0.4,1])
    elif 'UPPER' in label:
        if ("NC" in label):
            colors.append([0.3, 1, 1, 1])
        else:
            colors.append([0.4,1,0.4,1])
    elif 'LOWER' in label:
        if ("NC" in label):
            colors.append([1, 0.3, 1, 1])
        else:
            colors.append([0.4,0.4,1,1])

# # Plot based on nested x-axis (column 1 and column 2), and column 4 on the y-axis
plt.bar(range(len(df_arch)), df_arch[:]['RMSE'], color=colors)
plt.xticks(range(len(df_arch)), x_labels, rotation='vertical')

# # Add label values on top of each bar
for i, v in enumerate(df_arch[:]['RMSE']):
    plt.text(i, v, str(round(v, 2)), ha='center', va='bottom')
#
# plt.legend(x_labels)
plt.xlabel('Parameter - Arch')
plt.ylabel('RMSE')
# plt.title('Comparison RMSE value Arch based on number of iteration and number of population (cr=0.7 & f=0.5)')
plt.title('Comparison RMSE value Arch based on CR and F (iter=10 & popsize=1000)')
plt.tight_layout()
plt.show()
