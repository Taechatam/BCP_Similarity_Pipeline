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
import numpy as np
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import StandardScaler  # Add this line


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
    
    
    '''def rank_features(self):
        """
        Rank the selected features using:
        1) Linear SVM coefficients
        2) Permutation importance
        """
        print("Ranking features...")

        X = self.dataset[self.feature]
        y = self.dataset.label

        # Train linear SVM
        model = SVC(kernel='linear', C=1, random_state=42)
        model.fit(X, y)

        # --- Ranking by coefficients (linear SVM weights) ---
        coef_importance = pd.Series(
            np.abs(model.coef_).ravel(),
            index=self.feature
        ).sort_values(ascending=False)

        # --- Ranking by permutation importance ---
        perm_importance = permutation_importance(model, X, y, n_repeats=20, random_state=42)
        perm_df = pd.DataFrame({
            "Feature": X.columns,
            "Permutation Importance": perm_importance.importances_mean,
            "Std": perm_importance.importances_std
        }).sort_values(by="Permutation Importance", ascending=False)

        # Combine into one DataFrame
        rank_df = pd.DataFrame({
            "Feature": coef_importance.index,
            "SVM Coefficient Importance": coef_importance.values
        }).merge(perm_df, on="Feature")

        print(rank_df)
        return rank_df'''
    
    def rank_features(self, test_size=0.2, scoring='accuracy', scale_features=True):
        """
        Rank the selected features using:
        1) Linear SVM coefficients
        2) Permutation importance
        
        Args:
            test_size (float): Proportion of data to use for validation
            scoring (str): Scoring metric for permutation importance
            scale_features (bool): Whether to standardize features
        """
        print("Ranking features...")
        
        X = self.dataset[self.feature]
        y = self.dataset.label
        
        # Split data to avoid overfitting in permutation importance
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features if requested
        if scale_features:
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_val_scaled = scaler.transform(X_val)
            
            # Convert back to DataFrame to preserve column names
            X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
            X_val_scaled = pd.DataFrame(X_val_scaled, columns=X.columns)
        else:
            X_train_scaled = X_train
            X_val_scaled = X_val
        
        # Train linear SVM (same config as your other methods)
        model = SVC(kernel='linear', C=1, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Check model performance first
        train_score = model.score(X_train_scaled, y_train)
        val_score = model.score(X_val_scaled, y_val)
        print(f"Model performance - Train: {train_score:.3f}, Validation: {val_score:.3f}")
        
        # --- Ranking by coefficients (linear SVM weights) ---
        coef_importance = pd.Series(
            np.abs(model.coef_).ravel(),
            index=self.feature
        ).sort_values(ascending=False)
        
        # --- Ranking by permutation importance (on validation set) ---
        perm_importance = permutation_importance(
            model, X_val_scaled, y_val, 
            n_repeats=20, 
            random_state=42,
            scoring=scoring,
            n_jobs=-1  # Use all available cores
        )
        
        perm_df = pd.DataFrame({
            "Feature": X_val_scaled.columns,
            "Permutation Importance": perm_importance.importances_mean,
            "Std": perm_importance.importances_std
        }).sort_values(by="Permutation Importance", ascending=False)
        
        # Combine into one DataFrame with rankings
        rank_df = pd.DataFrame({
            "Feature": coef_importance.index,
            "SVM Coefficient Importance": coef_importance.values,
            "Coef Rank": range(1, len(coef_importance) + 1)
        }).merge(perm_df, on="Feature")
        
        # Add permutation importance ranking
        rank_df = rank_df.sort_values("Permutation Importance", ascending=False)
        rank_df["Perm Rank"] = range(1, len(rank_df) + 1)
        
        # Calculate average rank for final ranking
        rank_df["Average Rank"] = (rank_df["Coef Rank"] + rank_df["Perm Rank"]) / 2
        rank_df = rank_df.sort_values("Average Rank")
        
        # Add confidence intervals for permutation importance
        rank_df["Perm CI Lower"] = rank_df["Permutation Importance"] - 1.96 * rank_df["Std"]
        rank_df["Perm CI Upper"] = rank_df["Permutation Importance"] + 1.96 * rank_df["Std"]
        
        # Reorder columns for better readability
        rank_df = rank_df[[
            "Feature", "Average Rank",
            "SVM Coefficient Importance", "Coef Rank",
            "Permutation Importance", "Perm Rank", "Std",
            "Perm CI Lower", "Perm CI Upper"
        ]]
        
        print("\nFeature Rankings:")
        print("=" * 80)
        print(rank_df.round(4))
        
        # Highlight features with statistically significant permutation importance
        significant_features = rank_df[rank_df["Perm CI Lower"] > 0]
        if len(significant_features) > 0:
            print(f"\nFeatures with statistically significant importance (95% CI > 0):")
            print(significant_features["Feature"].tolist())
        else:
            print(f"\nWarning: No features show statistically significant permutation importance!")
            print("Consider checking your model performance or feature quality.")
        
        return rank_df
 