# BCP_Similarity_Pipeline

## Project Summary
This repository contains the antibiotic susceptibility testing (AST) pipeline developed for morphological analysis of bacterial cells. It is an early-state model designed to determine the degree of morphological changes to predict the susceptibility profile of antibiotic-responsive bacteria, specifically validated on *Acinetobacter baumannii*.

The pipeline leverages single-cell feature extraction to quantify cellular responses and calculate a **Similarity Index** against known profiles to determine resistance or sensitivity.

## Available Data
Example data files are provided to demonstrate the pipeline requirements. These are CSV files containing morphological features extracted via **CellProfiler**.

* [**`cellprofiler_data_example/`**](./cellprofiler_data_example/) - Folder containing raw feature-extracted CSV files from CellProfiler.
* [**`14_features.csv`**](./14_features.csv) - A reference file listing the 14 morphological features selected for the final model.
* [**`example_data_for_ROC.csv`**](./example_data_for_ROC.csv) - A formatted data set used for Receiver Operating Characteristic (ROC) curve determination.

## Installation & Environment
To ensure all dependencies (such as `pandas`, `scikit-learn`, and `matplotlib`) are correctly installed, use the provided environment file:

```bash
conda activate BCP_environment
```

## How to Run the Pipeline

Execute the core pipeline sequentially from your terminal using the commands below:

### 1. Data Preparation
Run [`step1_DataPreparation.py`](./step1_DataPreparation.py) to aggregate and clean individual CSV outputs from CellProfiler into a single usable dataset.

### 2. Feature Modeling & Visualization
Run [`step2_features_model.py`](./step2_features_model.py) 
* Extracts specific morphological features.
* Maps data points into Euclidean space.
* Generates visualizations of the selected feature sets.

### 3. Similarity Index Calculation
Run [`step3_similarity_index.py`](./step3_similarity_index.py) to calculate the Similarity Index between treated and untreated samples.

### 4. ROC Analysis & Thresholding
Run [`step4_ROC.py`](./step4_ROC.py) to determine the optimal diagnostic threshold.
* [**Requirement:**] Data must follow the format of [`example_data_for_ROC.csv`](./example_data_for_ROC.csv).
* [**Requirement:**] Requires labels for both sensitive and resistant known susceptibility references.


