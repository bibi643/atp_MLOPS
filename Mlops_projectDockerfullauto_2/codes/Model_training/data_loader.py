import pandas as pd

class DataHandler():
    def __init__(self):
        self.path_db = "https://github.com/bibi643/atp_MLOPS/raw/main/atp_data.csv"
        self.path_new_data = "http://tennis-data.co.uk/2023/2023.xlsx"
        self.path_save = "File_Data_Volume/atp_data.csv"
        self.path_container="/File_Data_Volume/atp_data.csv"

    def load_data(self):

        df = pd.read_csv(self.path_db, sep=',')
        return(df)

    def add_data(self):

        df = pd.read_excel(self.path_new_data)
        return(df)
    
    def save_data(self, df):
        """
        Write csv file 
        """
        df.to_csv(self.path_save, sep=",")


    def read_from_volume(self):
        """Read from Volume mapped folder"""
        df= pd.read_csv(self.path_container, sep=',')
        return(df)
