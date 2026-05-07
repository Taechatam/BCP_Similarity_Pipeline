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

def combine_data(path, output):
    #path = select_folder()

    label_folder = os.listdir(path)
    dataset = pd.DataFrame([])
    for label in label_folder:
        print(label)
        file_path = os.path.join(path, label)
        dna_data = pd.read_csv(os.path.join(file_path, 'Data_DNA.csv'))
        image_data = pd.read_csv(os.path.join(file_path, 'Data_Image.csv'))
        membrane_data = pd.read_csv(os.path.join(file_path, 'Data_Expanded_membrane.csv'))

        combined_df = pd.merge(dna_data, membrane_data, how='inner',
                               left_on=['ImageNumber', 'Parent_Expanded_membrane'],
                               right_on=['ImageNumber', 'ObjectNumber'])
        combined_df['label'] = label
        #combined_df.to_csv('test.csv', index=False)
        #combined_df = combined_df[(combined_df.AreaShape_Area_x > 300) & (combined_df.AreaShape_Area_y > 300)]
        file_location = []
        for index in range(len(combined_df)):
            for image_number in range(len(image_data.Group_Index)):
                if combined_df['ImageNumber'].iloc[index] == image_number+1:
                    image_file = image_data.FileName_CRC.iloc[image_number]
                    overlay_file = image_file[:-4]+'_overlay.tiff'
                    #location = os.path.join(image_data.PathName_RGB.iloc[image_number], image_data.FileName_RGB.iloc[image_number])
                    location = os.path.join(file_path, overlay_file)
                    file_location.append(location)
        combined_df['image_file'] = file_location
        annotate_position = []
        for i in range(combined_df.shape[0]):
            index_data = combined_df.loc[i]
            xmax = index_data['AreaShape_BoundingBoxMaximum_X_y']
            ymax = index_data['AreaShape_BoundingBoxMaximum_Y_y']
            xmin = index_data['AreaShape_BoundingBoxMinimum_X_y']
            ymin = index_data['AreaShape_BoundingBoxMinimum_Y_y']
            image_file_path = index_data['image_file']
            annotate_position.append([xmin, ymin, xmax, ymax, image_file_path])
        combined_df['annotation']= annotate_position

        print(f'{label}: {len(combined_df)} cells')
        dataset = dataset.append(combined_df, ignore_index=True)
        ## Anotate cell with image file
    #print(dataset.columns)
    select_feature_df = dataset[['label', 'AreaShape_MajorAxisLength_x', 'AreaShape_MajorAxisLength_y', 'AreaShape_MinorAxisLength_x', 'AreaShape_MinorAxisLength_y',
                          'AreaShape_Area_x', 'AreaShape_Area_y', 'AreaShape_Perimeter_x', 'AreaShape_Perimeter_y', 'AreaShape_Compactness_x', 'AreaShape_Compactness_y',
                          'AreaShape_Eccentricity_x', 'AreaShape_Eccentricity_y', 'AreaShape_Extent_x', 'AreaShape_Extent_y', 'AreaShape_MaxFeretDiameter_x', 'AreaShape_MaxFeretDiameter_y',
                          'AreaShape_MaximumRadius_x', 'AreaShape_MaximumRadius_y', 'AreaShape_MeanRadius_x', 'AreaShape_MeanRadius_y', 'AreaShape_MinFeretDiameter_x',
                          'AreaShape_MinFeretDiameter_y', 'AreaShape_Solidity_x', 'AreaShape_Solidity_y', 'Intensity_MeanIntensity_CRC_Blue_x', 'Intensity_MeanIntensity_CRC_Blue_y',
                          'Intensity_MinIntensityEdge_CRC_Blue_y', 'Intensity_StdIntensity_CRC_Blue_x', 'Intensity_StdIntensity_CRC_Blue_y']]

    annotate_df = select_feature_df.copy()
    annotate_df['annotation'] = dataset.annotation
    save_file = input("Do you want to save file (y/n): ")
    if save_file == 'y':
        file_name = input("File name: ")
        select_feature_df.to_csv(os.path.join(output, f"{file_name}.csv"), index=False)

        #annotate_df = annotate_df.drop_duplicates(subset=['annotation'], keep="first")
        annotate_df.to_csv(os.path.join(output, f'{file_name}_annotate_cell.csv'), index=False)
    else: return dataset

#combine_data()


path = "G:\Khim project\Filo/raw"
output = "G:\Khim project\Filo/test_data"
combine_data(path, output)