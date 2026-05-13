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


Utility ScriptsAdditional tools provided for data management:Script / FilePurposeDownsamp_all.pyRandomly down-samples data based on the smallest sample size in the set (run before Step 2).module/downsamp.pyA module for selecting a specific number of randomly sampled data points.similarity_combine_1folder.pyMerges multiple similarity index files into a single master file.similarity_plot.pyVisualizes similarity across different strains, including the option to plot the ROC-calculated threshold line.
