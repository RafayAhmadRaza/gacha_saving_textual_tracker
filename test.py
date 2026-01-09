from datetime import date
import pandas as pd
from pathlib import Path

path = Path("test_primos.csv")

def add_entry_spreadsheet(value:int):
        df = load_spreadsheet(path)
        today = date.today().isoformat()

        last_total = df["total"].iloc[-1] if not df.empty else 0
        new_total = last_total + value

        new_row = pd.DataFrame([{
             "date":"2026-01-09",
             "primogems":value,
             "total": new_total,
        }])

        df = pd.concat([df,new_row],ignore_index=True)

        save_spreadsheet(path,df)

    
def load_spreadsheet(path):
    
    if not path.exists():
        df = pd.DataFrame(columns=["date","primogems","total"])
        df.to_csv(path,index=False)
        print("created")
        return df        
    print("loaded")
    return pd.read_csv(path)

def save_spreadsheet(path,df:pd.DataFrame):
    df.to_csv(path)


def update_entry_spreadsheet(df:pd.DataFrame, path,value:int,entry_date: str | None = None, ):
    
    target_date = entry_date or date.today().isoformat()

    mask = df["date"] == target_date

    if not mask.any():
         raise ValueError(f"No entry found for date {target_date}")
    df.loc[mask,"primogems"] = value
    
    start_idx = df.index[mask][0]

    prev_total = df.loc[start_idx-1,"total"] if start_idx > 0 else 0
    running = prev_total

    for i in range(start_idx,len(df)):
         running+=df.loc[i,"primogems"]
         df.loc[i,"total"] = running 

    save_spreadsheet(path,df)

    

# add_entry_spreadsheet(300) 

df = load_spreadsheet(path=path)

# update_entry_spreadsheet(df,path,900,"2026-01-09")
# print(df.head(0))
print(str(df["primogems"].iloc[-1]))
