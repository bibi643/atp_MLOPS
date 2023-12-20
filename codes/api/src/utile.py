#Hard values

import os
import pandas as pd
import numpy as np

#Define object 

#Path data
path_root = "https://github.com/bibi643/atp_MLOPS/raw/main"
path_db = os.path.join(path_root, "atp_data.csv")

#Columns 
keeping_col =[#'atp'
              'location'
              ,'tournament'
              ,'date'
              ,'series'
              ,'surface'
              ,'round'
              ,'best_of'
              ,'proba_elo'
              ]

target='winner'



def to_pandas(data, colnames = None):
    temp = pd.DataFrame(data, columns=colnames)
    return(temp)





