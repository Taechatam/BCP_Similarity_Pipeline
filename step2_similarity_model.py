from module.Transformation import *
from module.Normalization import *
from module.PaCMAP_analysis import *
from module.outlier import *
from module.Feature_selection import feature_selection
def analyze(label_list, file_path, output_path, graph_titile):
    graph_title = graph_titile  # Add this line at the top of your function

    ## Import CSV file ##
    file_dict = {}
    file_dict['data_file'] = 'None'
    file_dict['feature_file'] = 'None'
    file_name = os.listdir(file_path)
    for name in file_name:
        if 'data' in name:
            file_dict['data_file'] = name
        if 'feature' in name:
            file_dict['feature_file'] = name
    print('Data file: {}'.format(file_dict['data_file']))
    print("Feature file: {}".format(file_dict['feature_file']))
    if file_dict['feature_file'] != 'None':
        feature_file = "{}/{}".format(file_path, file_dict['feature_file'])
    else:
        feature_file = 'None'
    dataset = pd.read_csv('{}/{}'.format(file_path, file_dict['data_file']))

    #dataset = pd.read_csv(file_path)

    dataset = dataset.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
    dataset = dataset[dataset.label.isin(label_list)]
    dataset.reset_index(drop=True, inplace=True)
    print('After remove Nan')
    print(dataset.label.value_counts())

    select_feature = dataset.columns[~(dataset.columns.isin(['label', 'annotation']))]
    for i in dataset.label.unique():
        print(f"{i}: {len(dataset[dataset.label == i])} cells")


    ## Transformation
    transformer = transform(dataset, select_feature)
    #dataset_transformation = transformer.transform()
    dataset_transformation = transformer.transform_data()
    #dataset_transformation = transformer.transform_log()
    print("Data transformation done!\n")
    print(dataset_transformation.label.value_counts())
    #check_transformation = transformer.after_transform()


    ## Remove outlier ##
    print("Remove outlier")
    #outlier = outlier_detection(dataset_transformation_normalization, 1, 10)
    # min_sample ,min_cluster
    outlier = outlier_detection(dataset_transformation, 2,10)
    remove_outlier_df = outlier.remove_outlier()

    ## Feature selection ##
    print("Feature selection")
    # Find combination label
    combination_bool = False
    for label in label_list:
        if "+" in label:
            combination_bool = True
        else:
            pass
    fs = feature_selection(remove_outlier_df, feature_file, output_path)

    if combination_bool:
        rfecv_df = fs.method_combination()
    else:
        rfecv_df = fs.method()

    tmp_data = rfecv_df.drop(['label', 'annotation'], axis=1)
    select_feature = tmp_data.columns

    # histogram plot #
    df_melted = rfecv_df.melt(id_vars='label', value_vars=select_feature, var_name='feature', value_name='value')
    # Function to plot histograms in batches
    def plot_histograms_in_batches(df, batch_size=9, output_path="."):
        features = df['feature'].unique()
        num_batches = (len(features) + batch_size - 1) // batch_size  # Calculate the number of batches

        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(features))
            batch_features = features[start_idx:end_idx]

            # Filter the DataFrame to include only the features in the current batch
            df_batch = df[df['feature'].isin(batch_features)]

            # Plot the histograms for the current batch
            g = sns.displot(df_batch, x='value', col='feature', hue='label', kind='kde', col_wrap=3,
                            facet_kws={'sharex': False, 'sharey': False}, alpha=0.7)

            # Adding legends
            g.add_legend()

            # Customizing the plot
            g.fig.subplots_adjust(top=0.9)
            g.fig.suptitle(f'Batch {i + 1}', fontsize=16)

           # Saving the plot as an image
            print(f'{output_path}/histograms_batch_{i + 1}.png')
            g.savefig(f'{output_path}/histograms_batch_{i + 1}.png')
            plt.close(g.fig)


    plot_histograms_in_batches(df_melted, batch_size=9, output_path=output_path)
    ## UMAP analysis
    print("PaCMAP analysis")
    #graph_title = input("Graph title: ")
    pacmap_model = pacmap_analysis(rfecv_df, graph_title, output_path)
    pacmap_df = pacmap_model.fit_transform()


    pacmap_df.to_csv(os.path.join(output_path, f"coordinate_{graph_titile}.csv"), index=False)
    #umap_df.to_csv(os.path.join(output_path, 'coordinate_PA03_remove_outlier.csv'), index=False)
    #plt.show()

    rfecv_df.to_csv(os.path.join(output_path, f"histogram.csv"), index=False)

    try:
        # Reuse the feature_selection object we already ran earlier
        fs = feature_selection(rfecv_df, feature_file="None", output=output_path)
        fs.feature = rfecv_df.drop(['label','annotation'], axis=1).columns
        
        # Check if we have features to work with
        if len(fs.feature) == 0:
            print("Warning: No features found after dropping label/annotation columns")
            return
        
        print(f"Working with {len(fs.feature)} features")
        
        # Evaluate model quality
        fs.group_quality()
        
        # Rank the selected features
        ranking = fs.rank_features()
        
        # Save results
        output_file = os.path.join(output_path, f"ranked_features_{graph_title}.csv")
        ranking.to_csv(output_file, index=False)
        print("Ranking saved:", output_file)
    
    except Exception as e:
        print(f"Error in feature ranking: {e}")

            # Quick data check
    print(f"Dataset shape: {rfecv_df.shape}")
    print(f"Features to rank: {len(fs.feature)}")
    print(f"Target distribution:\n{rfecv_df['label'].value_counts()}")
        


## input
file_path = r"C:\Workspace\Thesis\coding\Github_test\output2"# folder path that contains the csv file of the specific strain and the feature list csv file.
output_path = r"C:\Workspace\Thesis\coding\Github_test\output3"
graph_title = 'ATCC17978_14f'
analyze(['CIP','untreated'],file_path, output_path, graph_title)
# ['CIP1','CIP2','CIP3','CIP4','CIP5','CIP6'], ['untreated1','untreated2','untreated3','untreated4','untreated5','untreated6']
# 'CIP','untreated'
#for i in ['CIP1','untreated1','CIP2','untreated2','CIP3','untreated3','CIP4','untreated4','CIP5','untreated5','CIP6','untreated6','CIP7','untreated7','CIP8','untreated8','CIP9','untreated9','CIP10','untreated10','CIP11','untreated11','CIP12','untreated12','CIP13','untreated13','CIP14','untreated14','CIP15','untreated15','CIP16','untreated16','CIP17','untreated17','CIP18','untreated18','CIP19','untreated19','CIP20','untreated20','CIP21','untreated21']:
#    analyze(['Uninfected', i], file_path, output_path)
# 'TM01','TM02','TM03','TM04','TM05','TM06'
plt.show()


