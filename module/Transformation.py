import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.preprocessing import QuantileTransformer ##

class transform:
    def __init__(self, dataset, feature):
        self.feature = feature
        self.dataset = dataset
        self.data = dataset[feature]
        self.untreated = dataset[dataset.label == 'untreated']


    def transform(self):
        print(self.data.columns)
        transform_df = np.cbrt(self.data + 1)
        transform_df['label'] = self.dataset['label']
        transform_df['annotation'] = self.dataset['annotation']
        transform_df = transform_df.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
        return transform_df



    def transform_data(self):
        trans = QuantileTransformer(n_quantiles=1500, output_distribution='uniform')
        transform_data = trans.fit_transform(self.data)
        transform_df = pd.DataFrame(transform_data, columns=self.data.columns)
        transform_df['label'] = self.dataset['label']
        transform_df['annotation'] = self.dataset['annotation']
        transform_df = transform_df.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
        return transform_df

    def after_transform(self):
        output_path = "C:/Workspace/Thesis/results/Transformation"
        os.makedirs(output_path, exist_ok=True)  # Ensure output directory exists

        # Perform transformation on untreated data
        untreated_transformer = transform(self.untreated, self.feature)
        untreated_transformation = untreated_transformer.transform()
        untreated_transformation = untreated_transformation[untreated_transformation.columns[untreated_transformation.columns != 'label']]
        untreated_df = self.untreated[untreated_transformation.columns]

        for i in untreated_df.columns:
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))  # One row, two plots side by side
            fig.suptitle(i)

            # Before transformation
            sns.histplot(data=untreated_df, x=i, kde=True, ax=axes[0])
            axes[0].set_title("Before transformation")

            # After transformation
            sns.histplot(data=untreated_transformation, x=i, kde=True, ax=axes[1])
            axes[1].set_title("After transformation")

            # Save plot
            plt.tight_layout()
            plt.savefig(os.path.join(output_path, f"{i}.png"))
            plt.close()

        print(f"All plots saved to {output_path}")
        return untreated_transformation