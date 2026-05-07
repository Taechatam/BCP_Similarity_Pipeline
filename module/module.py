import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog

def select_folder():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askdirectory()
    return file_path

def combine_data( ):
    #path = select_folder()
    path = "D:\CA project\CA6, 12, 15, 16 profile\profile"

    dataset = pd.DataFrame([])
    for main_label in os.listdir(path):
        main_directory = os.path.join(path, main_label)
        for sub_label in os.listdir(main_directory):
            sub_directory = os.path.join(main_directory, sub_label)
            data_membrane = pd.read_csv(os.path.join(sub_directory, "Data_Expanded_membrane.csv"))
            data_dna = pd.read_csv(os.path.join(sub_directory, "Data_DNA.csv"))
            merge_df = pd.merge(data_dna, data_membrane, how='inner',
                                left_on=['ImageNumber', 'Parent_Expanded_membrane'],
                                right_on=['ImageNumber', 'ObjectNumber'])
            merge_df['label'] = f"{main_label}_{sub_label}"
            dataset = pd.concat([dataset, merge_df], axis=0)
            dataset.rest_index(drop=True, inplace=True)
            #dataset = dataset.append(merge_df, ignore_index=True)
    select_feature_df = dataset[["AreaShape_Area_y", "AreaShape_FormFactor_y", 'AreaShape_MajorAxisLength_y', 'AreaShape_MinorAxisLength_y',
          "AreaShape_Perimeter_y", 'Intensity_StdIntensity_Ori_Blue_y', 'Intensity_StdIntensity_Ori_Green_y',
          "AreaShape_Compactness_y", 'AreaShape_Eccentricity_y', 'AreaShape_Extent_y', 'AreaShape_MaxFeretDiameter_y',
          "AreaShape_MaximumRadius_y", 'AreaShape_MeanRadius_y', 'AreaShape_MinFeretDiameter_y', 'AreaShape_Solidity_y',
          'AreaShape_Area_x', 'AreaShape_FormFactor_x', 'AreaShape_MajorAxisLength_x', 'AreaShape_MinorAxisLength_x',
          'AreaShape_Perimeter_x', 'Intensity_StdIntensity_Ori_Blue_x', 'Intensity_StdIntensity_Ori_Green_x', 'AreaShape_Compactness_x',
          'AreaShape_Eccentricity_x', 'AreaShape_Extent_x', 'AreaShape_MaxFeretDiameter_x', 'AreaShape_MaximumRadius_x',
          'AreaShape_MeanRadius_x', 'AreaShape_MinFeretDiameter_x', 'AreaShape_Solidity_x', 'Intensity_MeanIntensity_Ori_Blue_x',
          'Intensity_MeanIntensity_Ori_Blue_y', 'Intensity_MeanIntensity_Ori_Green_x', 'Intensity_MeanIntensity_Ori_Green_y', 'label']]

    average_df = pd.DataFrame([])
    for group in select_feature_df.label.unique():
        temp_df = select_feature_df[select_feature_df.label == group]
        temp_data = temp_df[temp_df.columns[temp_df.columns != 'label']]
        avg_df = temp_data.mean(axis=0)
        avg_df['label'] = group
        average_df = average_df.append(avg_df, ignore_index=True)
    average_df.to_csv("avg_df.csv", index=False)
    #select_feature_df.to_csv("Test.csv", index=False)
    """label_folder = os.listdir(path)
    dataset = pd.DataFrame([])
    for label in label_folder:
        file_path = os.path.join(path, label)
        dna_data = pd.read_csv(os.path.join(file_path, 'Data_DNA.csv'))
        image_data = pd.read_csv(os.path.join(file_path, 'Data_Image.csv'))
        membrane_data = pd.read_csv(os.path.join(file_path, 'Data_Expanded_membrane.csv'))

        combined_df = pd.merge(dna_data, membrane_data, how='inner',
                               left_on=['ImageNumber', 'Parent_Expanded_membrane'],
                               right_on=['ImageNumber', 'ObjectNumber'])
        combined_df['label'] = label
        #combined_df = combined_df[(combined_df.AreaShape_Area_x > 300) & (combined_df.AreaShape_Area_y > 300)]
        file_location = []
        for index in range(len(combined_df)):
            for image_number in range(len(image_data.Group_Index)):
                if combined_df['ImageNumber'].iloc[index] == image_number+1:
                    location = os.path.join(image_data.PathName_RGB.iloc[image_number], image_data.FileName_RGB.iloc[image_number])
                    file_location.append(location)
        combined_df['image_file'] = file_location

        print(f'{label}: {len(combined_df)} cells')
        dataset = dataset.append(combined_df, ignore_index=True)
        ## Anotate cell with image file

    select_feature_df = dataset[['label', 'AreaShape_MajorAxisLength_x', 'AreaShape_MajorAxisLength_y', 'AreaShape_MinorAxisLength_x', 'AreaShape_MinorAxisLength_y',
                          'AreaShape_Area_x', 'AreaShape_Area_y', 'AreaShape_Perimeter_x', 'AreaShape_Perimeter_y', 'AreaShape_Compactness_x', 'AreaShape_Compactness_y',
                          'AreaShape_Eccentricity_x', 'AreaShape_Eccentricity_y', 'AreaShape_Extent_x', 'AreaShape_Extent_y', 'AreaShape_MaxFeretDiameter_x', 'AreaShape_MaxFeretDiameter_y',
                          'AreaShape_MaximumRadius_x', 'AreaShape_MaximumRadius_y', 'AreaShape_MeanRadius_x', 'AreaShape_MeanRadius_y', 'AreaShape_MinFeretDiameter_x',
                          'AreaShape_MinFeretDiameter_y', 'AreaShape_Solidity_x', 'AreaShape_Solidity_y', 'Intensity_MeanIntensity_OriBlue_x', 'Intensity_MeanIntensity_OriBlue_y',
                          'Intensity_MinIntensityEdge_OriBlue_y', 'Intensity_MeanIntensity_OriGreen_x', 'Intensity_MeanIntensity_OriGreen_y', 'Intensity_MinIntensityEdge_OriGreen_y',
                          'Intensity_StdIntensity_OriBlue_x', 'Intensity_StdIntensity_OriGreen_x', 'Intensity_StdIntensity_OriBlue_y', 'Intensity_StdIntensity_OriGreen_y']]


    save_file = input("Do you want to save file (y/n): ")
    if save_file == 'y':
        file_name = input("File name: ")
        #select_feature_df.to_csv(os.path.join(path, f"{file_name}.csv"), index=False)
        dataset.to_csv(os.path.join(path, f'{file_name}.csv'), index=False)
    else: return dataset"""

#combine_data()