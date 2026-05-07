import pandas as pd
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
        combined_df = combined_df.drop_duplicates(
            subset=['AreaShape_BoundingBoxMaximum_X_y', 'AreaShape_BoundingBoxMaximum_Y_y'], keep='last')
        key_column = ['AreaShape', 'Intensity', 'annotation', 'label']
        select_column = []
        for column in combined_df.columns:
            for key in key_column:
                if (key in column) and ('Location' not in column):
                    select_column.append(column)
                else:
                    pass
        select_data = combined_df[select_column]
        select_data = select_data.drop(['AreaShape_BoundingBoxMaximum_X_x', 'AreaShape_BoundingBoxMaximum_Y_x', 'AreaShape_BoundingBoxMinimum_X_x', 'AreaShape_BoundingBoxMinimum_Y_x', 'AreaShape_Center_X_x', 'AreaShape_Center_Y_x',
                                          'AreaShape_BoundingBoxMaximum_X_y', 'AreaShape_BoundingBoxMaximum_Y_y', 'AreaShape_BoundingBoxMinimum_X_y', 'AreaShape_BoundingBoxMinimum_Y_y', 'AreaShape_Center_X_y', 'AreaShape_Center_Y_y'], axis=1)

        print(f'{label}: {len(combined_df)} cells')
        dataset = pd.concat([dataset, select_data], axis=0)
        dataset.reset_index(drop=True, inplace=True)
        #dataset = dataset.append(combined_df, ignore_index=True)
        ## Anotate cell with image file


    annotate_df = dataset.copy()
    #
    annotate_df['annotation'] = dataset.annotation
    save_file = input("Do you want to save file (y/n): ")
    if save_file == 'y':
        file_name = input("File name (including \"_data\" in name) :")
        #dataset.to_csv(os.path.join(output, f"{file_name}.csv"), index=False)

        #annotate_df = annotate_df.drop_duplicates(subset=['annotation'], keep="first")
        annotate_df.to_csv(os.path.join(output, f'{file_name}_annotate_cell.csv'), index=False)
    else: return dataset

#combine_data()


path = r"C:\Workspace\Thesis\coding\Github_test\TM00_cellprofiler"
output = r"C:\Workspace\Thesis\coding\Github_test\output"
combine_data(path, output)