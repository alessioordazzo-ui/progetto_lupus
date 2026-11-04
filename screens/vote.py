from kivy.uix.screenmanager import Screen
from kivy.properties import (
    StringProperty,
    ListProperty,
    BooleanProperty
)

from kivymd.uix.button import MDRaisedButton


class VoteScreen(Screen):

    # ==========================================
    # STATO DELLA VOTAZIONE
    # ==========================================

    selected_player = StringProperty("")
    players = ListProperty([])

    can_local_vote = BooleanProperty(False)
    is_local_silenced = BooleanProperty(False)

    vote_status_message = StringProperty(
        "Caricamento votazione..."
    )

    # ==========================================
    # GIOCATORE LOCALE
    # ==========================================

    def ottieni_giocatore_locale(self):
        """
        Recupera il giocatore locale.
        """

        if self.manager is None:
            return None

        if not self.manager.has_screen("game"):
            return None

        game_screen = self.manager.get_screen("game")

        return next(
            (
                player
                for player in game_screen.players
                if player["name"] == game_screen.local_player_name
            ),
            None
        )

    # ==========================================
    # AGGIORNAMENTO STATO LOCALE
    # ==========================================

    def aggiorna_stato_votazione(self):
        """
        Aggiorna i permessi e il messaggio
        in base allo stato reale del giocatore.
        """

        giocatore = self.ottieni_giocatore_locale()
        print("\n=== DEBUG VOTAZIONE ===")
        print("Giocatore locale:", giocatore)

        if giocatore is not None:
            print("Nome:", giocatore.get("name"))
            print("Vivo:", giocatore.get("alive"))
            print("Silenziato:", giocatore.get("silenced"))
            print("Può votare:", giocatore.get("can_vote"))

        print("========================\n")

        self.can_local_vote = False
        self.is_local_silenced = False

        if giocatore is None:
            self.vote_status_message = (
                "Giocatore locale non disponibile."
            )
            return

        if not giocatore.get("alive", False):
            self.vote_status_message = (
                "Sei stato eliminato. Non puoi votare."
            )
            return

        self.is_local_silenced = giocatore.get(
            "silenced", False
        )

        if self.is_local_silenced:
            self.vote_status_message = (
                "SEI STATO SILENZIATO! "
                "Oggi non puoi parlare né votare."
            )
            return

        if not giocatore.get("can_vote", True):
            self.vote_status_message = (
                "Non puoi partecipare alla votazione."
            )
            return

        self.can_local_vote = True

        self.vote_status_message = (
            "Scegli il giocatore che vuoi votare"
        )

    # ==========================================
    # VERIFICA PERMESSO DI VOTO
    # ==========================================

    def puo_votare(self):
        """
        Verifica lo stato effettivo del giocatore.

        Non dipende dal messaggio visualizzato.
        """

        giocatore = self.ottieni_giocatore_locale()

        if giocatore is None:
            return False

        if not giocatore.get("alive", False):
            return False

        if giocatore.get("silenced", False):
            return False

        if not giocatore.get("can_vote", True):
            return False

        return True

    # ==========================================
    # APERTURA SCHERMATA
    # ==========================================

    def on_pre_enter(self, *args):
        """
        Prepara la schermata di votazione.
        """

        super().on_pre_enter(*args)

        game_screen = self.manager.get_screen("game")

        self.players = [
            player
            for player in game_screen.players
            if player.get("alive", False)
        ]

        self.selected_player = ""

        self.aggiorna_stato_votazione()

        self.update_players()

        print(
            f"Stato votazione: {self.vote_status_message}"
        )

    # ==========================================
    # LISTA GIOCATORI
    # ==========================================

    def update_players(self):
        """
        Genera i pulsanti dei giocatori vivi.
        """

        if "players_list" not in self.ids:
            return

        players_list = self.ids.players_list
        players_list.clear_widgets()

        votazione_consentita = self.puo_votare()

        for player in self.players:

            button = MDRaisedButton(
                text=player["name"],
                size_hint_x=1,
                disabled=not votazione_consentita
            )

            button.bind(
                on_release=lambda instance, name=player["name"]:
                    self.select_player(name)
            )

            players_list.add_widget(button)

    # ==========================================
    # SELEZIONE GIOCATORE
    # ==========================================

    def select_player(self, player_name):
        """
        Seleziona il giocatore da votare.
        """

        if not self.puo_votare():
            print("Votazione non consentita.")
            self.selected_player = ""
            return

        self.selected_player = player_name

        print(f"Giocatore selezionato: {player_name}")

    # ==========================================
    # CONFERMA VOTO
    # ==========================================

    def confirm_vote(self):
        """
        Conferma il voto ed elimina il
        giocatore selezionato.
        """

        if not self.puo_votare():
            print(
                "Voto bloccato: il giocatore "
                "non ha diritto di voto."
            )
            self.selected_player = ""
            return

        if not self.selected_player:
            return

        game_screen = self.manager.get_screen("game")

        bersaglio = next(
            (
                player
                for player in game_screen.players
                if player["name"] == self.selected_player
                and player.get("alive", False)
            ),
            None
        )

        if bersaglio is None:
            print(
                "Il giocatore selezionato "
                "non è disponibile."
            )
            return

        game_screen.kill_player(self.selected_player)

        print(
            f"{self.selected_player} è stato eliminato."
        )

        game_screen.phase = "notte"
        self.manager.current = "game"

    # ==========================================
    # USCITA SENZA VOTO
    # ==========================================

    def skip_vote(self):
        """
        Termina la fase di voto
        senza eliminazioni.
        """

        game_screen = self.manager.get_screen("game")

        print(
            "Votazione terminata senza eliminazioni."
        )

        game_screen.phase = "notte"
        self.manager.current = "game"