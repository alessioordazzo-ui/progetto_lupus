from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty

from kivymd.uix.button import MDRaisedButton


class VoteScreen(Screen):

    # =========================
    # STATO DELLA VOTAZIONE
    # =========================

    # Nome del giocatore attualmente selezionato
    selected_player = StringProperty("")

    # Lista dei giocatori disponibili per il voto
    players = ListProperty([])

    # =========================
    # APERTURA SCHERMATA
    # =========================

    def on_pre_enter(self):
        """
        Viene eseguito ogni volta che si entra
        nella schermata di votazione.
        """

        # Recupera la schermata principale della partita
        game_screen = self.manager.get_screen("game")

        # Prende solamente i giocatori ancora vivi
        self.players = [
            player
            for player in game_screen.players
            if player["alive"]
        ]

        # A ogni nuova votazione azzera la selezione precedente
        self.selected_player = ""

        # Genera i pulsanti dei giocatori
        self.update_players()

    # =========================
    # LISTA GIOCATORI
    # =========================

    def update_players(self):
        """
        Crea dinamicamente un pulsante
        per ogni giocatore ancora vivo.
        """

        players_list = self.ids.players_list

        # Rimuove eventuali pulsanti della votazione precedente
        players_list.clear_widgets()

        for player in self.players:

            button = MDRaisedButton(
                text=player["name"],
                size_hint_x=1
            )

            # Salviamo il nome del giocatore associato
            # a questo specifico pulsante.
            button.bind(
                on_release=lambda instance, name=player["name"]:
                self.select_player(name)
            )

            players_list.add_widget(button)

    # =========================
    # SELEZIONE GIOCATORE
    # =========================

    def select_player(self, player_name):
        """
        Seleziona il giocatore che si vuole votare.
        """

        self.selected_player = player_name

        print(f"Giocatore selezionato: {player_name}")

    # =========================
    # CONFERMA VOTO
    # =========================

    def confirm_vote(self):
        """
        Conferma il voto, elimina il giocatore
        selezionato e passa alla fase notturna.
        """

        # Sicurezza: se nessuno è stato selezionato,
        # non facciamo nulla.
        if not self.selected_player:
            return

        # Recupera la GameScreen
        game_screen = self.manager.get_screen("game")

        # Segna il giocatore selezionato come morto
        game_screen.kill_player(self.selected_player)

        print(f"{self.selected_player} è stato eliminato.")

        # Dopo la votazione inizia la notte
        game_screen.phase = "notte"

        # Torna alla schermata principale della partita
        self.manager.current = "game"