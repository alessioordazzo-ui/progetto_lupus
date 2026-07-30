from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard


class LupusLobbyCode(BoxLayout):

    lobby_code = StringProperty("X4J8PQ")

    def copy_code(self):
        Clipboard.copy(self.lobby_code)
        print(f"Codice {self.lobby_code} copiato!")