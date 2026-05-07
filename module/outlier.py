import pandas as pd
import numpy as np
import hdbscan ##

class outlier_detection:
    def __init__(self,dataset, eps, min_sample):
        self.eps = eps
        self.min_sample = min_sample
        self.dataset = dataset
        self.columns = dataset.columns
    def remove_outlier(self):
        model = hdbscan.HDBSCAN(min_cluster_size=self.min_sample, min_samples=self.eps)
        remove_outlier_df = pd.DataFrame([])
        for label in self.dataset.label.unique():
            select_dataset = self.dataset[self.dataset.label == label]
            select_dataset = select_dataset.reset_index(drop=True)
            data = select_dataset.drop(['label', 'annotation'], axis=1)
            #data = select_dataset[select_dataset.columns[select_dataset.columns != 'label']]
            data = data.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
            model.fit(data)
            select_dataset['cluster'] = model.labels_
            select_group = []

            ## Filter major group (more than 100 (10%) cells)
            for cluster_label in select_dataset.cluster.unique():
                #print(cluster_label)
                if len(select_dataset[select_dataset.cluster == cluster_label]) > 0.3*select_dataset.shape[0]:
                    select_group.append(cluster_label)
            remove_df = select_dataset[select_dataset.cluster.isin(select_group)]
            remove_df = remove_df.reset_index(drop=True)
            remove_outlier_df = pd.concat([remove_outlier_df, remove_df])
            remove_outlier_df.reset_index(drop=True, inplace=True)
            #remove_outlier_df = remove_outlier_df.append(remove_df)
            #print(remove_outlier_df)

        remove_outlier_df = remove_outlier_df[remove_outlier_df.columns[remove_outlier_df.columns != 'cluster']]
        remove_outlier_df = remove_outlier_df.reset_index(drop=True)
        print(remove_outlier_df.label.value_counts())
        return remove_outlier_df


