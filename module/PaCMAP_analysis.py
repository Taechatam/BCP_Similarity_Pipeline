import matplotlib.pyplot as plt
#from pacmap import pacmap
import pacmap
from module.module import *

class pacmap_analysis:
    def __init__(self, dataset, file_name, output):
        self.dataset = dataset
        self.columns = dataset.columns
        self.file_name = file_name
        self.output = output
    def fit_transform(self):
        #data = self.dataset[self.columns[self.columns != 'label']]
        data = self.dataset.drop(['label', 'annotation'], axis=1)
        data = data.to_numpy()
        model = pacmap.PaCMAP(n_components=2, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0)
        #model = pacmap.PaCMAP(n_dims=2, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0)
        x_pacmap = model.fit_transform(data, init="pca")
        pacmap_df = pd.DataFrame(x_pacmap, columns = ['Component 1', 'Component 2'])
        pacmap_df['label'] = self.dataset.label
        pacmap_df['annotation'] = self.dataset.annotation

        axe = plt.figure(figsize=(10, 10))
        ax = plt.subplot()
        ax.set_xlabel('Component 1', fontsize=10)
        ax.set_ylabel('Component 2', fontsize=10)
        ax.set_title('{}'.format(self.file_name), fontsize=30)
        colors = [
    "#e6194b",  # Red
    "#3cb44b",  # Green
    "#4363d8",  # Blue
    "#f58231",  # Orange
    "#911eb4",  # Purple
    "#42d4f4",  # Cyan
    "#f032e6",  # Magenta
    "#bfef45",  # Lime
    "#fabed4",  # Pink
    "#469990",  # Teal
    "#ffe119",  # Yellow
    "#9A6324",  # Brown
    "#808000",  # Olive
    "#000075",  # Navy
    "#800000",  # Maroon
    "#aaffc3",  # Mint
    "#ff7f50",  # Coral
    "#87ceeb",  # Sky Blue
    "#ffd700",  # Gold
    "#fa8072",  # Salmon
    "#4b0082",  # Indigo
    "#40e0d0",  # Turquoise
    "#dda0dd",  # Plum
    "#d2691e",  # Chocolate
    "#90ee90",  # Light Green
    "#4682b4",  # Steel Blue
    "#ff6347",  # Tomato
    "#da70d6",  # Orchid
    "#708090",  # Slate Gray
    "#ccccff"   # Periwinkle
]
        # ['purple', 'blue', 'red', 'lime', 'brown', 'green', 'black', 'orange', 'pink', 'gold']
        #colors = ['red', 'blue']
        #select_label = ['Amikacin', 'Ciprofloxacin', 'Colistin', 'Meropenem', 'Minocycline', 'Piperacillin', 'untreated']
        for label, color in zip(pacmap_df.label.unique(), colors):
            indicesToKeep = pacmap_df['label'] == label
            ax.scatter(pacmap_df.loc[indicesToKeep, 'Component 1']
                       , pacmap_df.loc[indicesToKeep, 'Component 2']
                       , c=color, s=7)
        ax.legend(pacmap_df.label.unique(), fontsize=5, loc=0)
        ax.grid()
        figure_file = os.path.join(self.output, f'{self.file_name}.jpeg')
        plt.savefig(figure_file)
        plt.show()
        return pacmap_df