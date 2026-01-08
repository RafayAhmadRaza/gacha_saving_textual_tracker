from textual.app import App, ComposeResult
from textual.widgets import Footer, Header,Label
from textual.containers import HorizontalGroup, VerticalScroll
import pandas as pd
import json
from datetime import date
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "GachaTracker"
CONFIG_FILE = CONFIG_DIR / "config.json"
CSV_FILE_TEST = "test_primos.csv"

class CurrencyManagement():
    pass

class ConfigManager():
    def load_config(path):
        if not path.exists():
            return {}
        return json.loads(path.read_text())
    def save_config(path,data):
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,indent=2))
    
class DataManagement:

    def __init__(self,path:Path):
        self.path = path

    def add_entry_spreadsheet(self,value:int):
        df = self.load_spreadsheet()
        today = date.today().isoformat()
        last_total = df["total"].iloc[-1] if not df.empty else 0
        
        new_total = last_total+value

        new_row = pd.DataFrame([{
            "date":today,
            "primogems":value,
            "total":new_total,
        }])

        df = pd.concat([df,new_row],ignore_index=True)

        self.save_spreadsheet(df)


    
    def load_spreadsheet(self) -> pd.DataFrame:
        self.path.parent.mkdir(parents=True,exist_ok=True)
        if not self.path.exists():
            df = pd.DataFrame(columns=["date","primogems","total"])
            df.to_csv(self.path,index=False)
            return df        
            
        return pd.read_csv(self.path)
    
    def save_spreadsheet(self,df:pd.DataFrame):
        df.to_csv(self.path)


    def update_entry_spreadsheet(self,df:pd.DataFrame, value:int,entry_date:str | None=None):
        target_date = entry_date or date.today().isoformat()

        mask = df["date"] == target_date
        if not mask.any():
            raise ValueError(f"No Entry found for date {target_date}")
        df.loc[mask,"primogems"] = value

        start_idx = df.index[mask][0]

        prev_total = df.local[start_idx-1,"total"] if start_idx > 0 else 0 
        running = prev_total

        for i in range(start_idx,len(df)):
            running+=df.loc[i,"primogems"]
            df.loc[i,"total"] = running
        
        self.save_spreadsheet(df)

class GachaData(HorizontalGroup):
    
    def compose(self) -> ComposeResult:
       """ Create Text Form of Data """
       yield Label("Date")
       yield Label("Value")
       yield Label("Total")



class Gacha_Tracker_App(App):
    BINDINGS = [("d","toggle_dark","Toggle dark mode"),("a","Add Today Currency Collecting","Add Currency"),("u","Update Today's Currency Entry","Update Entry")]
    dataManager = DataManagement(path=CSV_FILE_TEST)

    def compose(self) -> ComposeResult:
        yield Header()
        yield GachaData()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            
            "textual-dark" if self.theme == "textual-light" else "textual-light"
            
            )


if __name__ == "__main__":
    app = Gacha_Tracker_App()
    app.run()