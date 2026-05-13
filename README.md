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
conda env create -f BCP_environment.yml
conda activate BCP_env
```

## How to Run the Pipeline (Step-by-Step Execution)

You can execute the entire pipeline directly from your terminal. Below is the complete command sequence for a standard analysis workflow, including optional data preprocessing.

### Quick Start Code Sequence

```bash
# Initialize and activate the computational environment
conda activate BCP_env

# [Optional] Step 0: Down-sample large datasets to handle group size imbalances
python Downsamp_all.py

# Step 1: Aggregate and clean CellProfiler CSV outputs
python step1_DataPreparation.py

# Step 2: Extract morphological features and map to Euclidean space
python step2_features_model.py

# Step 3: Quantify single-cell phenotypic Similarity Indices
python step3_similarity_index.py

# Step 4: Construct ROC curves and define diagnostic thresholds
python step4_ROC.py
```
