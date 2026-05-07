from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

from module.Transformation import *

class normalize(transform):
    def __init__(self, dataset, feature):
        super().__init__(dataset, feature)
    def transform(self):
        scaler = StandardScaler()
        normalize_data = scaler.fit_transform(self.data)
        normalize_df = pd.DataFrame(normalize_data, columns=self.data.columns)
        normalize_df['label'] = self.dataset.label
        normalize_df['annotation'] = self.dataset.annotation
        normalize_df = normalize_df.replace([np.inf, -np.inf], np.nan).dropna(axis=1)
        return normalize_df

    def after_normalize(self):
        output_path = "D:\BCP\Proceeding_pipeline/Normalization"
        #untreated_data = self.untreated[self.untreated.columns[self.untreated.columns != 'label']]
        untreated_normalizer = normalize(self.untreated, self.data.columns)
        untreated_normalization = untreated_normalizer.transform()
        print(untreated_normalization)
        untreated_normalization = untreated_normalization[untreated_normalization.columns[untreated_normalization.columns != 'label']]
        untreated_df = self.untreated[untreated_normalization.columns]

        for i in untreated_df.columns:
        #for i in ['AreaShape_Area_x']:
            fig, axes = plt.subplots(1, 2, figsize=(5,5))
            fig.suptitle(i)
            sns.distplot(x=untreated_df[i], kde=True, hist=True, ax=axes[0], axlabel=i)
            axes[0].set_title("Before transformation")
            #plt.savefig(os.path.join(output_path, "Before_Transformation.png"))
            #fig, axes = plt.subplots(1, 1, figsize=(5, 5))
            #fig.suptitle(i)
            sns.distplot(x=untreated_normalization[i], kde=True, hist=True, ax=axes[1], axlabel=i)
            axes[1].set_title("After transformation")
            #plt.savefig(os.path.join(output_path, "After_Transformation.png"))
            #axes.set_title("After transformation")
            plt.savefig(os.path.join(output_path, f"{i}.png"))
        plt.show()