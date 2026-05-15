import pandas as pd
from scipy.spatial import distance
import numpy as np
from sklearn.cluster import MeanShift
import os

def similarity_index(input_file, output, output_file_name, ref_label, sample_label):
    raw = pd.read_csv(input_file)
    raw = raw.drop(['annotation'], axis=1)



    unknown = raw[raw.label == sample_label]
    unknown_data = unknown.drop(['label'], axis = 1)
    similarity_score = []
    summary_dict = {}

    ## Calculate similarity index
    for control in ref_label:

        control_dataset = raw[raw.label == control]
        if control_dataset.shape[0] > 0:
            control_data = control_dataset.drop(['label'], axis=1)
            print (f"{control}: {len(control_dataset)}")

            ## Identify cluster
            ms = MeanShift()
            ms.fit(control_data)

            center_cluster = ms.cluster_centers_
            control_dataset['cluster'] = ms.labels_
            cluster_filter = []
            for cluster in control_dataset.cluster.unique():
                cluster_df = control_dataset[control_dataset.cluster == cluster]

                ## Exclude minor cluster (less than 50)
                if len(cluster_df) > 50:
                    cluster_filter.append(cluster)
            control_dataset = control_dataset[control_dataset.cluster.isin(cluster_filter)]
            # print(control_dataset.cluster.value_counts())

            similarity_list = []
             rng = np.random.default_rng(seed=42)
            
            # Generate 200 unique indices without replacement
            # (replace=False ensures you don't pick the same row twice)
            random_indices = rng.choice(len(unknown_data), size=200, replace=False)

            for unknown_number in random_indices:
                unknow_point = unknown_data.iloc[unknown_number]

                mean_distance_list = []
                index_list = []
                for index_cluster in cluster_filter:
                    mean_distance_list.insert(len(mean_distance_list), distance.euclidean(unknow_point, center_cluster[index_cluster]))
                    index_list.insert(len(index_list), index_cluster)

                min_cluster_index = np.argmin(mean_distance_list)
                min_cluster = control_dataset[control_dataset.cluster == index_list[min_cluster_index]]

                distance_list = []
                for single_point in range(len(min_cluster)):
                    coordinate_single_point = min_cluster[min_cluster.columns[0:2]].iloc[single_point]
                    distance_list.append(distance.euclidean(unknow_point, coordinate_single_point))

                min_distance = np.amin(distance_list)
                similarity = 1 / (1 + min_distance)
                similarity_list.append(similarity)

            ## average similarity from 200 randomed data point
            similarity_score.append([control, np.mean(similarity_list)])
            summary_dict[control] = [np.mean(similarity_list)]

    similarity_df = pd.DataFrame.from_dict(summary_dict)
    similarity_df['sample_label'] = sample_label
    print(similarity_df)
    ## Export similarity index
    #file_name = input("File name: ")
    similarity_df.to_csv(os.path.join(output, f"{output_file_name}.csv"), index=False)



coordinate_file = r"C:\Workspace\Thesis\coding\Github_test\output3_clustered\coordinate_test.csv"
output = r"C:\Workspace\Thesis\coding\Github_test\output4_similarity"
output_file_name = 'test'
ref_label = ['untreated']
sample_label = 'treated'
similarity_index(coordinate_file, output, output_file_name, ref_label, sample_label)
