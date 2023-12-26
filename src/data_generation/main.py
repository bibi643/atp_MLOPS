# Package

from data_loader import DataHandler
import pandas as pd

#Init 
data_handler = DataHandler()

# 01 Import data
print('Load data')

df = data_handler.load_data()\
                .drop(['elo_winner','elo_loser','proba_elo'],axis=1)\
                .assign(Date=lambda x: pd.to_datetime(x['Date'], format='%Y-%m-%d'))

new_data = data_handler.add_data()

#02 Add new data

new_df = data_handler.merge_data(df, new_data)

# 03 Save the data
print('Save Data')
data_handler.save_date(new_df)