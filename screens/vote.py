
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
    # INIZIALIZZAZIONE
    # ==========================================

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Registro dei voti della partita.
        # Chiave: (giorno, nome del votante)
        # Valore: informazioni sul voto.
        self.voti_registrati = {}

        self.voto_registrato = None

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
    # CONTROLLO VOTO GIA' REGISTRATO
    # ==========================================

    def ha_gia_votato(self):
        """
        Controlla se il giocatore locale
        ha gia' votato nella giornata corrente.
        """

        if self.manager is None:
            return False

        if not self.manager.has_screen("game"):
            return False

        game_screen = self.manager.get_screen("game")

        chiave_voto = (
            game_screen.day_number,
            game_screen.local_player_name
        )

        return chiave_voto in self.voti_registrati

    # ==========================================
    # AGGIORNAMENTO STATO LOCALE
    # ==========================================

    def aggiorna_stato_votazione(self):
        """
        Aggiorna i permessi e il messaggio
        in base allo stato reale del giocatore.
        """

        giocatore = self.ottieni_giocatore_locale()

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
                "Oggi non puoi parlare ne' votare."
            )
            return

        if not giocatore.get("can_vote", True):
            self.vote_status_message = (
                "Non puoi partecipare alla votazione."
            )
            return

        if self.ha_gia_votato():
            self.vote_status_message = (
                "Hai gia' votato in questa giornata."
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
        Verifica il diritto di voto effettivo,
        compreso il controllo del doppio voto.
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

        if self.ha_gia_votato():
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
            f"Stato votazione: {self.vote_status_message}",
            flush=True
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
            print("Votazione non consentita.", flush=True)
            self.selected_player = ""
            return

        if not any(
            player["name"] == player_name
            and player.get("alive", False)
            for player in self.players
        ):
            print("Giocatore non disponibile.", flush=True)
            return

        self.selected_player = player_name

        print(
            f"Giocatore selezionato: {player_name}",
            flush=True
        )

    # ==========================================
    # CONFERMA VOTO
    # ==========================================

    def confirm_vote(self):
        """
        Registra un voto senza eliminare
        immediatamente il bersaglio.
        """

        if not self.puo_votare():
            print(
                "Voto bloccato: giocatore non autorizzato "
                "oppure voto gia' registrato.",
                flush=True
            )
            self.selected_player = ""
            self.aggiorna_stato_votazione()
            return

        if not self.selected_player:
            print("Nessun giocatore selezionato.", flush=True)
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
            print("Bersaglio non disponibile.", flush=True)
            return

        chiave_voto = (
            game_screen.day_number,
            game_screen.local_player_name
        )

        voto = {
            "votante": game_screen.local_player_name,
            "bersaglio": self.selected_player,
            "giorno": game_screen.day_number
        }

        # Registra il voto.
        self.voti_registrati[chiave_voto] = voto
        self.voto_registrato = voto

        print("\n=== VOTO REGISTRATO ===", flush=True)
        print("Votante:", voto["votante"], flush=True)
        print("Bersaglio:", voto["bersaglio"], flush=True)
        print("Giorno:", voto["giorno"], flush=True)
        print("Bersaglio vivo:", bersaglio["alive"], flush=True)
        print("======================\n", flush=True)

        # Aggiorna i permessi e disabilita
        # i pulsanti dopo il voto.
        self.selected_player = ""

        self.aggiorna_stato_votazione()
        self.update_players()

    # ==========================================
    # USCITA SENZA VOTO
    # ==========================================

    def skip_vote(self):
        """
        Termina la fase di voto
        senza eliminazioni.

        Gestione provvisoria:
        il conteggio collettivo dei voti
        sara' implementato successivamente.
        """

        game_screen = self.manager.get_screen("game")

        print(
            "Votazione terminata senza eliminazioni.",
            flush=True
        )

        game_screen.phase = "notte"
        self.manager.current = "game"
