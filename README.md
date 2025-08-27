## Technical Interview: Real Estate Data Analysis

This repository contains my solution to the technical interview assignment of the analysis of real estate sales using data from Statbel. The project demonstrates skills in data manipulation, visualisation and building a practical data driven tool.

## Project Structure
- data/: contains the raw and processed data
    - administrative boundaries: https://statbel.fgov.be/sites/default/files/files/opendata/Statistische%20sectoren/sh_statbel_statistical_sectors_31370_20240101.shp.zip
    - realestate statistical data: https://statbel.fgov.be/sites/default/files/files/documents/Bouwen%20%26%20wonen/2.1%20Vastgoedprijzen/NM/FR_immo_statbel_trimestre_par_commune.xlsx
- notebooks/: Jupyter notebooks showing step by stpe process of:
    - Data Loading and Cleaning: Raexploration 
    - Data Transformatiion:  Data transformation to a convenient format to query and visualise. This includes creting a single column for date/time and separate columns fo N (number of sales) and € (price)
    - Exploratory Data Analysis (EDA): Visualising key trends and identifying patterns
    - Price Corrector Implementation: Price correction model
- README.md: This file, providing overview of the project
- requirements.txt: A list of all necessary Pythoon libraries to run this project
- src/: A python Script, price_corrector.py, containing the reusable function for the price corrector.  This separates the logic from the exploratory notebooks.


## How to Run


1. Clone the repository:
```
bash

git clone repo-name.git
cd repo-name

```

2. Set up the environment:

```
bash

python3 -m venv rockestate
source rockestate/bin/activate
pip install -r requirements.txt

```

3. Run the notebooks:
Open the Jupyternotebooks in the notebooks/ directory to explore the data, see the visualisation and understand the price corrector implementation.

## Data Exploration and Visualisation

- Evolution over time: I have created a time-series plot that shows the eveolution of number of sales (N) and average prices (€) over the 15 year period. The plots reveals cyclical patterns and highlight key periods of growth/dip in the real estate industry. These can be correlated wit major economic events, or policy changes. Key events are:
    - Year 2015 - In Q1 of 2015, there was negative growth (60% in sales) and (7.5% in house prices). This was caused by pending tax reforms, postponed transactions (anticipated reductions in in property taxes), economic uncertainty and a seasonal market volatility.

    - Year 2020 - COVID-19  global epidemiologic outbreak caused significant shocks globally. In Belgium, this is evident by a negative growth rate of 60 % in sales and around 6% drop in the median price.

    - Year 2025 - In Q1, there is small growth rate (5%) in number of sales but over 7% growth rate in prices. This is due an increase in the sale of expensive homes rather than a broad increase in the prices of all property types. The tax reforms incentivised purchase of more expensive properties. 

- Bonus 1: Spatial Visualisation: Use geopandas for a static map visualisation

- Bonus 2: Interactive Visualisation: I have used folium to make the spatial visualisation interactive. I display the mean price across every municipality in the year 2024. 

- Further improvements:

    1. Creating a an exploratory visualisation allowing to dynamically select the years
    2. Clicking on a municipality produces a line chart showing evolution of the prices, and number of sales
    3. Dynamically showing the rate of growth of sales for each administrative unit (municipality, province,region)
    4. Using libraries such as Dash and Plotly can allow to create more complex and dynamic visualisation


## Price Corrector
The "price corrector" adjusts a property's value based on the historical market trends.
- Methodology: It uses a ratio-based approach. It calculates the average price change between two quarters for a specific municipality and property type.

    - ``` price at t1 = Price at t0 * (Average Price in Q_t1/ Average Price in Q_t0)```

- Bonus 3: Forecasting: To forecast future quarters, I use a linear regression and Lightweight Gradient Boosting Model. 

    - Model Selection:A Linear Regression model and  A LightGBM regressor are selected to provide a comprative analysis.

    - Feature Engineeering: I extract of additional informative feaures to enable the model capture trends and seasonality.
        - Lagged Price: The median price from the previous quarter (prix_median_lag1)
        - Rolling MEan: A rolling average of prices over the last quarters (prix_median_rolling_4q) to smooth out noise and capture yearly trends

    - Data Preparation: The dataset was prepared as follows:
        - Time-Serieis Indexing: A datetime index was created to handle the time-series data
        - Categorical Encoding: Features like property_type were one-hot encoded, while refnis (municipality code) was label-encoded.

    - Data Split: The data was split chronologically to prevent data leakage:
        - Training Data: 2010-2022
        - Validation Data: 2023
        - Test Data: 2024

    - Model Performance : Both models were evaluated on the Test Dataset using the Mean Absolute Error(MAE) to compare their predictive accuracy

    - Findings: Linear Regression model had MAE 26016.85 EUR of while the LightGBM had MAE of  Set:25447.63 EUR Given the current real estate prices, this represents an error rate of (5% - 10%) which can be acceptable, given that we are working with Mean Prices that are already aggregated at the municipality level.

    - Improvements:
        - Feature engineering - curent features used are sensitive to unpredictable market shifts
        - More informative Features - demographics, interest rates, inflation, 
        - hyperparameter tuning of the models
        - Different model architecture such as RNNs
        - use mlflow to track model artifacts.
