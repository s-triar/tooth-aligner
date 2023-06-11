import matplotlib.pyplot as plt
import pandas as pd

filenames=[
# "hasil_evaluation_ld_based_on_ld.csv",
# "hasil_evaluation_ld_based_on_ld_no_candidate.csv"

# "hasil_evaluation_ld_based_on_ld_fcr_variation_no_candidate.csv",

    # "popiter\\hasil_evaluation_ld_based_on_ld_popiter_with_candidate_v2.csv",
    # "popiter\\hasil_evaluation_ld_based_on_ld_popiter_no_candidate_v2.csv",
    # "wmanual\\hasil_evaluation_ld_based_on_ld_manual_w_with_v2.csv",
    "hasil_evaluation_ld_based_on_ld_popiter_with_new_data.csv"
]

# folder='popiter'
# folder='f_cr'

filename=filenames[0]

# pop iter
# _ FILE Rahang         Total      RMSE
df_arch = pd.read_csv(filename, encoding='utf-8', index_col=0)
if "wc" in filename:
    pick = "pop100_iter100"
    df_arch = df_arch[df_arch['FILE'].str.contains(pick)]
    print(df_arch)
# df_arch = df_arch.sort_values(by=['Rahang'], ascending=False)
if len(filenames) > 1:
    filename=filenames[1]

    # pop iter
    # _ FILE Rahang         Total      RMSE
    df_arch_no_candidate = pd.read_csv(filename, encoding='utf-8', index_col=0)
    # df_arch_no_candidate = df_arch_no_candidate.sort_values(by=['Rahang'], ascending=False)
    if "nc" in filename:
        pick = "pop1000_iter10"
        df_arch_no_candidate=df_arch_no_candidate[df_arch_no_candidate['FILE'].str.contains(pick)]
    df_arch = pd.concat([df_arch, df_arch_no_candidate])

if len(filenames) > 2:
    filename = filenames[2]

    # pop iter
    # _ FILE Rahang         Total      RMSE
    df_arch_no_candidate = pd.read_csv(filename, encoding='utf-8', index_col=0)
    # df_arch_no_candidate = df_arch_no_candidate.sort_values(by=['Rahang'], ascending=False)

    df_arch = pd.concat([df_arch, df_arch_no_candidate])
df_arch = df_arch.sort_values(by=['Rahang', 'Landmark', 'FILE'], ascending=False)

landmarks = df_arch[:]['Landmark'].drop_duplicates()
# print(landmarks)

archs = df_arch[:]['Rahang'].drop_duplicates()
# print(archs)

# Create unique labels for the nested x-axis
def create_label_from_file(filename: str):
    names = filename.split("_")
    # print(filename, names)
    if len(names)==1 or len(names)==2:
        return names[-1]
    return names[3]+" "+names[4]+(" WC" if "nc" not in filename else " NC")

for a in archs:
    df_arch_cp = df_arch[df_arch['Rahang'] == a]
    x_labels = [f"{create_label_from_file(c1)} - {c2} - {c3}" for c1, c2, c3 in zip(df_arch_cp[:]['FILE'], df_arch_cp[:]['Rahang'], df_arch_cp[:]['Landmark'])]

    # # Assign colors based on the labels
    colors = []
    for label in x_labels:
        if 'BOTH' in label:
            if ("NC" in label):
                colors.append([1, 1, 0.3, 1])
            elif ("manual" in label):
                colors.append([0.8, 0.4, 0.8, 1])
            else:
                colors.append([1, 0.4, 0.4, 1])
        elif 'UPPER' in label:
            if ("NC" in label):
                colors.append([0.3, 1, 1, 1])
            elif ("manual" in label):
                colors.append([0.1, 0.7, 0.4, 1])
            else:
                colors.append([0.4, 1, 0.4, 1])
        elif 'LOWER' in label:
            if ("NC" in label):
                colors.append([1, 0.3, 1, 1])
            elif ("manual" in label):
                colors.append([0.4, 0.1, 1, 1])
            else:
                colors.append([0.4, 0.4, 1, 1])
    plt.rcParams["figure.figsize"] = [8, 10]
    # # Plot based on nested x-axis (column 1 and column 2), and column 4 on the y-axis
    plt.barh(range(len(df_arch_cp)), df_arch_cp[:]['RMSE'], color=colors)
    plt.yticks(range(len(df_arch_cp)), x_labels, rotation='horizontal')

    # # Add label values on top of each bar
    for i, v in enumerate(df_arch_cp[:]['RMSE']):
        plt.text(v/2, i, str(round(v, 2)), ha='center', va='center', rotation='horizontal')
    #
    # plt.legend(x_labels)
    plt.ylabel('Parameter - Arch')
    plt.xlabel('RMSE')

    # plt.title('Comparison RMSE value Landmark based on number of iteration and number of population (cr=0.7 & f=0.5)')
    # plt.title('Comparison RMSE value Arch based on CR and F (iter=10 & popsize=1000)')
    plt.title('Comparison RMSE value DE')
    plt.tight_layout()
    plt.show()
