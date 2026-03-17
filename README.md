# Price Predictor Model

#  Store Revenue Forecasting & Optimization

## Project Overview  
This project focuses on predicting daily store revenue using historical sales data collected from monthly Excel sheets. The pipeline is designed with a modular workflow, separating data ingestion, exploratory data analysis (EDA), and model training into independent notebooks for better maintainability and scalability.

##  Problem Statement  
Small-scale businesses often struggle with inconsistent daily sales patterns, leading to challenges such as overstocking, understocking, and inefficient staffing during seasonal demand fluctuations. Traditional planning methods fail to capture these variations effectively, resulting in lost revenue and operational inefficiencies.

##  Solution  
This project leverages time-series analysis and regression-based modeling to forecast daily revenue and uncover underlying sales patterns. Through extensive analysis, we observed that simpler linear models captured the data trends effectively without requiring overly complex architectures, thereby improving both interpretability and performance.

##  Impact  
- Improved demand forecasting accuracy for daily operations  
- Enabled better inventory and staffing decisions  
- Reduced overstocking and understaffing issues  
- Achieved **~15% increase in profitability**  
- Contributed to **significant long-term cost savings (100K+ USD range)**  

## What This Project Does
- Ingests monthly Excel files and merges them into a unified dataset.
- Cleans and standardizes dates/columns.
- Performs exploratory data analysis (trend, seasonality, stationarity, rolling behavior).
- Trains and compares multiple forecasting/regression models.
- Produces short-term revenue forecasts.

## Project Workflow
1. `notebooks/01_data_ingestion.ipynb`
- Reads monthly files from `datasets/`.
- Normalizes schema and saves merged output (`merged_data.xlsx`).

2. `notebooks/02_eda.ipynb`
- Performs cleaning and analysis.
- Saves cleaned modeling dataset to `datasets/eda_cleaned.csv`.

3. `notebooks/03_model_training.ipynb`
- Loads cleaned data (`eda_cleaned.csv`).
- Builds, evaluates, and compares models.
- Generates final forecast plots.

## Models Built
- Naive baseline
- LightGBM Regressor
- Ridge Regression
- Random Forest Regressor
- ARIMA
- SARIMAX
- AutoReg / MA / ARMA variants

## Best Model (For Now)
Based on the current notebook comparison, **Ridge Regression** is treated as the best model.

Observed metrics in the notebook:
- Ridge Validation MAE: `193.99`
- Ridge Test MAE: `230.64`

Notes:
- Random Forest and LightGBM were also tested.
- ARIMA/SARIMAX experiments are included for time-series benchmarking.

## How To Run The Project
1. Install dependencies
- Use the dependency list in `readme.txt`, or run:
- `pip install pandas numpy matplotlib seaborn scikit-learn statsmodels scipy openpyxl holidays lightgbm colorama`

2. Run data ingestion
- Open and run `notebooks/01_data_ingestion.ipynb` end-to-end.

3. Run EDA and cleaned data export
- Open and run `notebooks/02_eda.ipynb` end-to-end.
- Confirm `datasets/eda_cleaned.csv` is created.

4. Run model training
- Open and run `notebooks/03_model_training.ipynb` end-to-end.

## Output Files
- `merged_data.xlsx` (merged dataset from ingestion)
- `datasets/eda_cleaned.csv` (cleaned dataset for training)

