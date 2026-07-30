from kivy.properties import (
    StringProperty,
    BooleanProperty,
)

from kivy.uix.boxlayout import BoxLayout


class LupusPlayerCard(BoxLayout):

    player_name = StringProperty("Giocatore")

    role = StringProperty("Giocatore")

    ready = BooleanProperty(False)

    host = BooleanProperty(False)