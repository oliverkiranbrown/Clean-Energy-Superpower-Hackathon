import pandas as pd
import json

def load_data():
    accounts_df = pd.read_csv("./data/account_data.csv")

    accounts_df.set_index("hashed_account_no", inplace=True)
    predictions_df = pd.read_csv("./data/kaluza_predicted_ev.csv")
    full_df = predictions_df.join(accounts_df, on="hashed_account_no")
    

    return full_df

if __name__ == "__main__":
    print(load_data())
