# Package

from data_loader import DataHandler
from utile import path_db, log_separator




#Init 
data_handler = DataHandler()

# 01 Import data
print('Lancement du code 01: data_loader.py')
df = data_handler.load_data()
print('taille du dataframe:', df.shape)
log_separator()



# 02 Save the data
print('Lancement du code 02: data_loader.py')
data_handler.save_data(df)
log_separator()




