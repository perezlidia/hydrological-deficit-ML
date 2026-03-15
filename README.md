# Spatial Modeling of Hydrological Deficit Using Machine Learning

This repository contains the datasets, scripts, and outputs used in the study:

"Spatial modeling of hydrological deficit using machine learning and climatic data (1960–2024) in Northwestern Mexico."

The objective of this project is to analyze and model the spatial distribution of hydrological deficit using climatic data and machine learning techniques.

------------------------------------------------------------

STUDY AREA

The study area corresponds to northwestern Mexico and includes the following states:

-  Sonora
-  Sinaloa
-  Baja California
-  Baja California Sur

These regions are characterized by arid and semi-arid climates with low precipitation and high potential evapotranspiration.

------------------------------------------------------------

DATA SOURCES

The analysis uses the following climatic variables:

-  Precipitation (PR)
-  Potential Evapotranspiration (ETP)

Data sources:

-  TerraClimate dataset
-  Geographic data from INEGI and CONABIO

Spatial resolution: approximately 4 km  
Temporal coverage: 1960–2024

------------------------------------------------------------

METHODOLOGICAL WORKFLOW

The workflow implemented in this repository includes the following steps:

1. Climate data preprocessing
2. Water balance calculation
3. Hydrological deficit identification
4. Dataset construction
5. Machine learning model training
6. Model evaluation
7. SHAP interpretability analysis
8. Spatial prediction of hydrological deficit probability

------------------------------------------------------------

MACHINE LEARNING MODELS

Two machine learning algorithms were used:

-  Random Forest (RF)
-  Gradient Boosting (GB)

Model performance was evaluated using:

-  RMSE (Root Mean Square Error)
-  MAE (Mean Absolute Error)
-  R² (Coefficient of Determination)

------------------------------------------------------------

MAIN OUTPUTS

The repository includes the following spatial outputs:

-  PR_mean.tif
-  ETP_mean.tif
-  WB_mean.tif
-  HD_probability.tif
-  HD_frequency.tif

These layers represent the spatial distribution of climatic conditions and hydrological deficit probability across northwestern Mexico.

------------------------------------------------------------

REPRODUCIBILITY

All scripts required to reproduce the analysis are available in the scripts directory.

The repository ensures full reproducibility of the workflow used to generate the results presented in the article.

------------------------------------------------------------

INSTALLATION

Install the required Python libraries using:

pip install -r requirements.txt

------------------------------------------------------------

DATA AND CODE AVAILABILITY

All datasets, raster outputs, and Python scripts used in this study are publicly available in this repository to ensure reproducibility of the results.

------------------------------------------------------------

PROJECT LEAD

Lidia Yadira Pérez Aguilar
Facultad de Informática Culiacán, Universidad Autónoma de Sinaloa, Culiacán, Sinaloa, México
Researcher in geospatial analysis and environmental data science.
lidiaperez@uas.edu.mx

------------------------------------------------------------

LICENSE

This project is released under the MIT License.

If this code is used or adapted in other studies, please cite it as follows:
Code used or adapted from Pérez-Aguilar et al. (2026) under the MIT License.
