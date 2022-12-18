import glob
import numpy as np
from utility.calculation import find_distance_between_two_points
import math
import pandas as pd

def dist(pts1, pts2):
    return math.sqrt(
        math.pow((pts1[0]-pts2[0]),2) +
        math.pow((pts1[1]-pts2[1]),2) +
        math.pow((pts1[2]-pts2[2]),2)
    )
    
path_save_ground_truth = 'saved_landmark'
path_save_predict = 'saved_landmark_predict_manual'

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
    for k in glob.glob(p+"\\step_0"+"/*.csv"):
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
    for ii in range(len(df_gt)):
        if(df_gt.iloc[ii]['landmark']!= 3 and df_gt.iloc[ii]['landmark']!=4):
            t = df_pred.loc[
                (df_pred['label'] == df_gt.iloc[ii]['label']) & (df_pred['landmark'] == df_gt.iloc[ii]['landmark'])
            ]
            if(len(t.index)>0):       
                idxpred = t.index[0]
                dist = find_distance_between_two_points(
                    np.array([
                        df_pred.iloc[idxpred]["x"],
                        df_pred.iloc[idxpred]["y"],
                        df_pred.iloc[idxpred]["z"],
                        ]), 
                    np.array([
                        df_gt.iloc[ii]["x"],
                        df_gt.iloc[ii]["y"],
                        df_gt.iloc[ii]["z"],
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
    
    for ii in range(len(df_gt)):
        if(df_gt.iloc[ii]['landmark']!= 3 and df_gt.iloc[ii]['landmark']!=4):
        
        
            t = df_pred.loc[
                (df_pred['label'] == df_gt.iloc[ii]['label']) & (df_pred['landmark'] == df_gt.iloc[ii]['landmark'])
            ]
            if(len(t.index)>0):       
            
                idxpred = t.index[0]
                dist = find_distance_between_two_points(
                    np.array([
                        df_pred.iloc[idxpred]["x"],
                        df_pred.iloc[idxpred]["y"],
                        df_pred.iloc[idxpred]["z"],
                        ]), 
                    np.array([
                        df_gt.iloc[ii]["x"],
                        df_gt.iloc[ii]["y"],
                        df_gt.iloc[ii]["z"],
                    ]))
                total_bot += math.pow(dist,2)
                
                i_bot+=1
    # print(df_gt.head())
    # print(df_pred.head())
    
    # # for i in range(len(df_gt.head())):
    # #     print(df_gt.head().iloc[i]["x"])
print("RMSE rahang keduanya", (total_bot+total_top), math.sqrt((total_top+total_bot)/(i_up+i_bot)))
print("RMSE rahang atas",total_top, math.sqrt(total_top/i_up)) # 
print("RMSE rahang bawah",total_bot, math.sqrt(total_bot/i_bot)) 
    
    
