
from kivy.base import EventLoop
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (
    NumericProperty,
    StringProperty
)

from screens.night import NightScreen
from screens.vote import VoteScreen


EventLoop.ensure_window()


class GameTest(Screen):

    day_number = NumericProperty(1)
    local_player_role = StringProperty("Curatore")
    local_player_name = StringProperty("Alessio")
    phase = StringProperty("notte")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.players = [
            {
                "name": "Alessio",
                "role": "Curatore",
                "alive": True
            },
            {
                "name": "Marco",
                "role": "Lupo Silenziatore",
                "alive": True
            },
            {
                "name": "Sara",
                "role": "Villico",
                "alive": True
            }
        ]

    def update_players(self):
        pass

    def kill_player(self, name):
        for player in self.players:
            if player["name"] == name:
                player["alive"] = False


manager = ScreenManager()

game = GameTest(name="game")
night = NightScreen(name="night")
vote = VoteScreen(name="vote")

manager.add_widget(game)
manager.add_widget(night)
manager.add_widget(vote)

alessio = game.players[0]
marco = game.players[1]

# ==========================================
# NOTTE 1: APPLICAZIONE SILENZIO
# ==========================================

night.on_pre_enter()

risultato = night.gestore_notte.aggiungi_azione(
    "silenzia",
    marco,
    alessio
)

assert risultato["successo"], risultato

night.finish_night()

assert alessio["silenced"] is True
assert alessio["can_vote"] is False
assert game.phase == "giorno"

print("NOTTE 1: silenzio applicato correttamente.")

# ==========================================
# GIORNO 2: BLOCCO DEL VOTO
# ==========================================

assert vote.puo_votare() is False

print("GIORNO 2: voto correttamente bloccato.")

# ==========================================
# NOTTE 2: SCADENZA SILENZIO
# ==========================================

game.phase = "notte"

night.on_pre_enter()

assert alessio["silenced"] is False
assert alessio["can_vote"] is True

print("NOTTE 2: silenzio scaduto correttamente.")
print("TEST CICLO COMPLETO SUPERATO")
