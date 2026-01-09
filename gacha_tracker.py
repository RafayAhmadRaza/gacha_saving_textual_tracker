from textual.app import App, ComposeResult
from textual.widgets import Footer, Header,Label,Static
from textual.containers import HorizontalGroup, VerticalScroll
import pandas as pd
import json
from datetime import date
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "GachaTracker"
CONFIG_FILE = CONFIG_DIR / "config.json"
CSV_FILE_TEST = Path("test_primos.csv")

class CurrencyManagement():
    def Gain_Caculator(self,A:int,B:int):
        return str(A+B)

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

class LabelData(HorizontalGroup):


    def compose(self) -> ComposeResult:
       """ Create Text Form of Data """
       yield Label("Date",id="Date")
       yield Label("Primo",id="Primo")
       yield Label("Total ",id="Total")
       
class GachaData(Static):
    def __init__(self,df,**kwargs):
        super().__init__(**kwargs)

        self.df = df

    def _on_mount(self):
        self.update(self.df.to_string(index=False,header=False))

class Get_Previous_Entry(Static):
    def __init__(self,df,**kwargs):
        super().__init__(**kwargs)

        self.df = df

    def _on_mount(self):
        self.update(str(self.df["primogems"].iloc[-2]))

class Get_Today_Entry(Static):

    def __init__(self,df,**kwargs):
        super().__init__(**kwargs)

        self.df = df

    def _on_mount(self):
        self.update(str(self.df["primogems"].iloc[-1]))

class Get_Total_Primos(Static):
    def __init__(self,df,**kwargs):
        super().__init__(**kwargs)

        self.df = df

    def _on_mount(self):
        self.update(str(self.df["total"].iloc[-1]))
    
    




class Gacha_Tracker_App(App):
    CSS_PATH = "Label.tcss"

    BINDINGS = [("d","toggle_dark","Toggle dark mode"),("a","Add Today Currency Collecting","Add Currency"),("u","Update Today's Currency Entry","Update Entry"),("v","View Entire History","View History")]
    dataManager = DataManagement(path=CSV_FILE_TEST)
    
    df = dataManager.load_spreadsheet()
    Gain = CurrencyManagement().Gain_Caculator(df["primogems"].iloc[-1],
                                                df["primogems"].iloc[-2]
                                                )

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Today's Entry: ",id="L1")
        yield Get_Today_Entry(self.df)

        yield Label("Previous Days Entry: ")
        yield Get_Previous_Entry(self.df)

        yield Label("Gain: ")
        yield Label(str(self.Gain))


        yield Label("Total: ")
        yield Get_Total_Primos(self.df)

        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            
            "textual-dark" if self.theme == "textual-light" else "textual-light"
            
            )


if __name__ == "__main__":
    app = Gacha_Tracker_App()
    app.run()