import pandas as pd

class DataHandler():
    def __init__(self):
        self.path_db = "https://github.com/bibi643/atp_MLOPS/raw/main/atp_data.csv"
        self.path_new_data = "http://tennis-data.co.uk/2023/2023.xlsx"
        self.path_save = "File_Data_Volume/atp_data.csv"

    def load_data(self):

        df = pd.read_csv(self.path_db, sep=',')
        return(df)

    def add_data(self):

        keeping_col = ['ATP', 'Location', 'Tournament', 'Date', 'Series', 'Court', 'Surface',
                'Round', 'Best of', 'Winner', 'Loser', 'WRank', 'LRank', 'Wsets',
                'Lsets', 'Comment', 'PSW', 'PSL', 'B365W', 'B365L']

        df = pd.read_excel(self.path_new_data)

        new_data = df[keeping_col]

        return(new_data)
    
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