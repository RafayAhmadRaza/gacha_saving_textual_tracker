from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.containers import HorizontalGroup, VerticalScroll

class CurrencyManagement():
    pass

class SpreadSheetManagement():
    pass

class Gacha_Tracker_App(App):
    BINDINGS = [("d","toggle_dark","Toggle dark mode"),("a","Add Today Currency Collecting","Add Currency"),("u","Update Today's Currency Entry","Update Entry")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            
            "textual-dark" if self.theme == "textual-light" else "textual-light"
            
            )


if __name__ == "__main__":
    app = Gacha_Tracker_App()
    app.run()