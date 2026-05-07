from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.svm import SVC ##
import time
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_selection import RFECV ##
from sklearn.metrics import confusion_matrix
import seaborn as sns
import os
class feature_selection:
    def __init__(self, dataset, feature_file, output):
        self.dataset = dataset
        self.columns = dataset.columns
        self.feature_file = feature_file
        self.output = output
    def method(self):
        if self.feature_file == 'None':
            data = self.dataset.drop(['label', 'annotation'], axis=1)
            #data = self.dataset[self.columns[:-1]]
            X_train, X_test, y_train, y_test = train_test_split(data, self.dataset.label,
                                                                test_size=0.2, random_state=42)
            model = SVC(kernel='linear', C=1)
            selector = RFECV(model, step=1, cv=3, verbose=1)
            selector.fit(X_train, y_train)
            """plt.figure()
            plt.xlabel("Number of features selected")
            plt.ylabel("Cross validation score (accuracy)")
            plt.plot(range(selector.n_features_,
                           len(selector.grid_scores_) + selector.n_features_),
                     selector.grid_scores_)
            plt.show()"""
            prediction = selector.predict(X_test)
            print("Accuracy: {}".format(accuracy_score(y_test, prediction)))
            print(classification_report(y_test, prediction))
            select_feature = data.columns[selector.support_]
            print ("Optimum number of feature: {}".format(selector.n_features_))
            select_feature_df = pd.DataFrame(select_feature, columns = ['feature'])
            print (self.dataset.label.unique())
            feature_file = input("Save feature in csv: ")
            select_feature_df.to_csv(os.path.join(self.output, f"{feature_file}.csv"), index=False)
            select_data = data[select_feature]
            select_data['label'] = self.dataset.label
            select_data['annotation'] = self.dataset.annotation
            self.feature = select_feature
            return select_data

        if self.feature_file != 'None':
            feature_df = pd.read_csv(self.feature_file,header=0, sep=r'\s+')
            select_feature = feature_df.feature
            print (select_feature)
            print ("You selected features: {}".format(len(select_feature)))
            select_data = self.dataset[select_feature]
            select_data['label'] = self.dataset.label
            select_data['annotation'] = self.dataset.annotation
            self.feature = select_feature
            return select_data

    def method_combination(self):
        if self.feature_file == 'None':
            data = self.dataset.drop(['label'], axis=1)
            #data = self.dataset[self.columns[:-1]]
            ## Determine combination label
            label_unique = self.dataset.label.unique()
            for i in label_unique:
                if "+" in i:
                    control_label = i.split("+")
                    combination_label = i
                else: pass
            control_label.append("untreated")
            control_dataset = self.dataset[self.dataset.label.isin(control_label)]
            control_data = control_dataset.drop(['label'], axis=1)
            X_train, X_test, y_train, y_test = train_test_split(control_data, control_dataset.label,
                                                            test_size=0.2, random_state=42)

            model = SVC(kernel='linear', C=1)
            selector = RFECV(model, step=1, cv=3, verbose=1)
            selector.fit(X_train, y_train)
            prediction = selector.predict(X_test)
            print("Accuracy: {}".format(accuracy_score(y_test, prediction)))
            print(classification_report(y_test, prediction))
            select_feature = data.columns[selector.support_]
            print("Optimum number of feature: {}".format(selector.n_features_))
            select_feature_df = pd.DataFrame(select_feature, columns=['feature'])
            select_feature_df.to_csv(os.path.join(self.output, f"{combination_label}_feature.csv"), index=False)
            select_data = data[select_feature]
            select_data['label'] = self.dataset.label
            self.feature = select_feature
            return select_data

        if self.feature_file != 'None':
            feature_df = pd.read_csv(self.feature_file, header=0, sep=r'\s+')
            select_feature = feature_df.feature
            print(select_feature)
            print("You selected features: {}".format(len(select_feature)))
            select_data = self.dataset[select_feature]
            select_data['label'] = self.dataset.label
            self.feature = select_feature
        return select_data

    def group_quality(self):
        print ("Start training: ")
        start = time.time()
        X_train, X_test, y_train, y_test = train_test_split(self.dataset[self.feature], self.dataset.label,
                                                            test_size = 0.2, random_state = 42)
        model = SVC(kernel='linear', C=1)
        model.fit(X_train, y_train)
        end = time.time()
        print ("Time consuming: {}".format(end-start))
        prediction = model.predict(X_test)
        print ("Accuracy: {}".format(accuracy_score(y_test, prediction)))
        print(classification_report(y_test, prediction))

        matrix = confusion_matrix(y_test, prediction)
        confusion_dataframe = pd.DataFrame(matrix, index=self.dataset.label.unique(),
                                           columns=self.dataset.label.unique())

        sns.heatmap(confusion_dataframe, annot=True, cbar=None, cmap="Blues")
        plt.title("Confusion Matrix"), plt.tight_layout()
        plt.ylabel("True Class"), plt.xlabel("Predicted Class")
        #plt.show()

        return accuracy_score(y_test, prediction)