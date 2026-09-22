from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, NumericProperty


class WaitingRoomScreen(Screen):

    # Stato del giocatore locale
    player_ready = BooleanProperty(False)

    # Numero massimo di giocatori nella lobby
    max_players = NumericProperty(10)

    # Numero attuale di giocatori
    player_count = NumericProperty(4)

    def toggle_ready(self):
        """Cambia lo stato del giocatore tra pronto e non pronto."""

        self.player_ready = not self.player_ready

        if self.player_ready:
            print("Giocatore pronto!")
        else:
            print("Giocatore non pronto!")

    def start_game(self):
        """Gestisce la richiesta di avvio della partita."""

        if not self.player_ready:
            print("Non puoi avviare la partita: devi essere pronto.")
            return

        print("Tutti pronti. Avvio della partita...")

        self.manager.current = "game"