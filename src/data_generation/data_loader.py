import pandas as pd

class DataHandler():
    def __init__(self):
        self.path_db = "https://github.com/bibi643/atp_MLOPS/raw/main/atp_data.csv"
        self.path_new_data = "http://tennis-data.co.uk/2023/2023.xlsx"
        self.path_save = "File_Data_Volume/atp_data.csv"

    def load_data(self, type : str ):

        if type == "csv":
            df = pd.read_csv(self.path_db, sep=',')

        elif type =="excel":
            df = pd.read_excel(self.path_new_data)

        else:
            raise ValueError("Type de données non pris en charge.")
    
        return(df)
    
    def merge_data(self, df, new_data):
        """
        add new data
        """
        df = pd.concat([df,new_data])
        return(df)
    
    def save_date(self, df):
        """
        Write csv file 
        """
        df.to_csv(self.path_save, sep=",")