# weather_data_analysis_app
Interacting with a database using SQLalchemy and creating an app using Flask

## Purpose
Use preexisting database with seven years of daily temperature readings to analyze weather patterns. Also, an API is built to let other users access the data.

## Tools
The SQLAlchemy pachaged was used to interact with the sqlite database within the jupyter notebook. Pandas, Numpy and the DateTime package are also used to analyse data. Python's Flask package is used to construct the API.

## Results
The jupyter notebook contains initial analysis with visualizations of both precipitation and temperature data. The weatherapp.py file contains code for the API to be activated. Available routes for the user include accessing precipitation, station and temperature data. There are also interactive routes that filter the data using dates that are input by the user.
