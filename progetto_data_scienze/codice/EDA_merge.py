import pandas as pd
import numpy as np

#EDA merge
final_df = pd.read_json("progetto_data_scienze/codice/final_json.json")
final_df.head(5)
final_df.info()
final_df.shape
final_df.columns
final_df.isna().sum()
#final_df.describe()