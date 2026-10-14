
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ListProperty,
    BooleanProperty
)

from kivymd.uix.button import MDRaisedButton

from operative.ruoli import get_ruolo
from operative.notte import GestoreNotte


class NightScreen(Screen):

    day_number = NumericProperty(1)

    local_player_role = StringProperty("")
    current_action = StringProperty("")
    selected_player = StringProperty("")

    available_players = ListProperty([])
    action_used = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.gestore_notte = GestoreNotte()
        self.notte_inizializzata = None

    def giocatore_ha_agito(self, nome_giocatore):
        """
        Verifica se un giocatore ha già registrato
        un'azione durante la notte corrente.
        """

        return any(
            azione["attore"]["name"] == nome_giocatore
            for azione in self.gestore_notte.azioni
        )

    def on_pre_enter(self):
        """
        Prepara la schermata senza cancellare
        le azioni della notte corrente.
        """

        game_screen = self.manager.get_screen("game")

        self.day_number = game_screen.day_number
        self.local_player_role = game_screen.local_player_role

        if self.notte_inizializzata != self.day_number:

            self.gestore_notte.reset()

            for player in game_screen.players:
                player["protected"] = False

            self.notte_inizializzata = self.day_number

            print("=== NUOVA NOTTE ===")
            print("Notte:", self.day_number)

        # Il blocco dell'azione dipende dal giocatore,
        # non dal numero di volte che apriamo la schermata.
        self.action_used = self.giocatore_ha_agito(
            game_screen.local_player_name
        )

        self.selected_player = ""

        ruolo = get_ruolo(self.local_player_role)

        if ruolo:
            self.current_action = ruolo.get("azione", "")
        else:
            self.current_action = ""

        self.available_players = [
            player
            for player in game_screen.players
            if player["alive"]
        ]

        self.update_players()

        print("=== NOTTE ===")
        print("Giocatore:", game_screen.local_player_name)
        print("Ruolo:", self.local_player_role)
        print("Azione:", self.current_action)
        print("Ha già agito:", self.action_used)
        print("Azioni registrate:", len(self.gestore_notte.azioni))

    def update_players(self):
        """
        Mostra i giocatori vivi selezionabili.
        """

        if "players_list" not in self.ids:
            return

        players_list = self.ids.players_list
        players_list.clear_widgets()

        for player in self.available_players:

            button = MDRaisedButton(
                text=player["name"],
                size_hint_x=1
            )

            button.bind(
                on_release=lambda instance, name=player["name"]:
                self.select_player(name)
            )

            players_list.add_widget(button)

    def select_player(self, player_name):
        """
        Seleziona il bersaglio.
        """

        if self.action_used:
            print("Il giocatore ha già agito.")
            return

        self.selected_player = player_name
        print("Bersaglio selezionato:", player_name)

    def execute_action(self):
        """
        Registra l'azione del giocatore locale.
        """

        game_screen = self.manager.get_screen("game")
        nome_locale = game_screen.local_player_name

        # Verifica anche nel gestore, non soltanto
        # tramite il flag dell'interfaccia.
        if self.giocatore_ha_agito(nome_locale):
            self.action_used = True
            print("Azione già registrata questa notte.")
            return

        if not self.selected_player:
            print("Nessun giocatore selezionato.")
            return

        if not self.current_action:
            print("Questo ruolo non possiede un'azione.")
            return

        attore = next(
            (
                player for player in game_screen.players
                if player["name"] == nome_locale
            ),
            None
        )

        bersaglio = next(
            (
                player for player in game_screen.players
                if player["name"] == self.selected_player
            ),
            None
        )

        if attore is None or not attore["alive"]:
            print("Giocatore locale non disponibile.")
            return

        if bersaglio is None or not bersaglio["alive"]:
            print("Bersaglio non disponibile.")
            return

        risultato = self.gestore_notte.aggiungi_azione(
            self.current_action,
            attore,
            bersaglio
        )

        print("=== AZIONE REGISTRATA ===")
        print(risultato)

        if risultato["successo"]:
            self.action_used = True
            print(
                "Totale azioni registrate:",
                len(self.gestore_notte.azioni)
            )

    def finish_night(self):
        """
        Risolve tutte le azioni registrate
        e passa al giorno successivo.
        """

        game_screen = self.manager.get_screen("game")

        print("=== RISOLUZIONE NOTTE ===")

        risultati = self.gestore_notte.risolvi()

        for risultato in risultati:
            print(risultato)

        game_screen.update_players()

        game_screen.phase = "giorno"
        game_screen.day_number += 1

        self.gestore_notte.reset()
        self.notte_inizializzata = None

        self.manager.current = "game"
