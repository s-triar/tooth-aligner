import glob
import numpy as np
from utility.calculation import find_distance_between_two_points
import math
import pandas as pd
from constant.enums import ToothType

def dist(pts1, pts2):
    return math.sqrt(
        math.pow((pts1[0]-pts2[0]),2) +
        math.pow((pts1[1]-pts2[1]),2) +
        math.pow((pts1[2]-pts2[2]),2)
    )
    
# path_save_ground_truth = 'saved_landmark'
# path_save_predict = 'saved_landmark_predict_manual'
# path_save_ground_truth = 'D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix'
# path_save_predict = 'D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\saved_ld_auto'

path_save_ground_truth = 'D:\\tesis\\fix'
path_save_predict = 'D:\\Code\\tooth-aligner\\saved_ld_weight_manual'

people = []

up = "UPPER"
low = "LOWER"

upper_path_data_gt =[]
lower_path_data_gt =[]
upper_path_data_pred =[]
lower_path_data_pred =[]

for p in glob.glob(path_save_ground_truth+"/**"):
    # person = p.split("\\")
    # people.append(person[-1])
    for k in glob.glob(p+"/*.csv"):
        if(up in k):
            upper_path_data_gt.append(k)
        else:
            lower_path_data_gt.append(k)
            
for p in glob.glob(path_save_predict+"/**"):
    person = p.split("\\")
    people.append(person[-1])
    for k in glob.glob(p+"\\step_0"+"/*.csv"):
        if(up in k):
            upper_path_data_pred.append(k)
        else:
            lower_path_data_pred.append(k)       

total_top=0
total_bot=0
i_up = 0
i_bot=0
for ty in ToothType:
    i_up = 0
    i_bot=0
    label = ty.value
    if label != 0:
        for i in range(len(people)):
            indv="\\"+people[i]+"\\"
            p=""
            for h in upper_path_data_gt:
                if(indv in h):
                    p=h
                    break
            
            df_gt = pd.read_csv(p, index_col=0)
            for h in upper_path_data_pred:
                if(indv in h):
                    p=h
                    break
            df_pred = pd.read_csv(p, index_col=0)
            
            df_gt = df_gt.loc[
                (df_gt['label'] == label)
            ]
            for index, row in df_gt.iterrows():
                # print(row.index)
                ii=index
                # print(ii)
                # print(df_gt)
                t = df_pred.loc[
                    (df_pred['label'] == row['label']) & (df_pred['landmark'] == row['landmark'])
                ]
                idxpred = t.index[0]
                dist = find_distance_between_two_points(
                    np.array([
                        df_pred.iloc[idxpred]["x"],
                        df_pred.iloc[idxpred]["y"],
                        df_pred.iloc[idxpred]["z"],
                        ]), 
                    np.array([
                        row["x"],
                        row["y"],
                        row["z"],
                    ]))
                total_top += math.pow(dist,2)
                
                i_up+=1
                
                
            p=""
            for h in lower_path_data_gt:
                if(indv in h):
                    p=h
                    break
            
            df_gt = pd.read_csv(p, index_col=0)
            for h in lower_path_data_pred:
                if(indv in h):
                    p=h
                    break
            df_pred = pd.read_csv(p, index_col=0)
            
            df_gt = df_gt.loc[
                (df_gt['label'] == label)
            ]
            for index, row in df_gt.iterrows():
                ii = index   
                
                
                t = df_pred.loc[
                    (df_pred['label'] == row['label']) & (df_pred['landmark'] == row['landmark'])
                ]
                idxpred = t.index[0]
                dist = find_distance_between_two_points(
                    np.array([
                        df_pred.iloc[idxpred]["x"],
                        df_pred.iloc[idxpred]["y"],
                        df_pred.iloc[idxpred]["z"],
                        ]), 
                    np.array([
                        row["x"],
                        row["y"],
                        row["z"],
                    ]))
                total_bot += math.pow(dist,2)
                
                i_bot+=1
            # print(df_gt.head())
            # print(df_pred.head())
            
            # # for i in range(len(df_gt.head())):
            # #     print(df_gt.head().iloc[i]["x"])
        print("RMSE rahang keduanya", label, (total_bot+total_top), math.sqrt((total_top+total_bot)/(i_up+i_bot)))
        print("RMSE rahang atas", label,total_top, math.sqrt(total_top/i_up)) # 
        print("RMSE rahang bawah", label,total_bot, math.sqrt(total_bot/i_bot)) 
        
        
