
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ListProperty,
    BooleanProperty
)

from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

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

        # Gestore delle azioni notturne
        self.gestore_notte = GestoreNotte()

        # Identificativo della notte corrente
        self.notte_inizializzata = None

        # Archivio dei risultati investigativi
        # associati ai singoli giocatori
        self.casella_risultati = {}

        # Finestra dei risultati
        self.dialog_risultati = None

    # ==========================================
    # CONTROLLO AZIONI
    # ==========================================

    def giocatore_ha_agito(self, nome_giocatore):
        """
        Controlla se il giocatore ha già registrato
        un'azione durante la notte corrente.
        """

        return any(
            azione["attore"]["name"] == nome_giocatore
            for azione in self.gestore_notte.azioni
        )

    # ==========================================
    # INIZIALIZZAZIONE NOTTE
    # ==========================================

    def on_pre_enter(self):
        """
        Prepara la schermata notturna.

        Le azioni vengono mantenute quando
        si rientra nella stessa notte.
        """

        game_screen = self.manager.get_screen("game")

        self.day_number = game_screen.day_number
        self.local_player_role = game_screen.local_player_role

        # Nuova notte
        if self.notte_inizializzata != self.day_number:

            self.gestore_notte.reset()

            # Rimuove le protezioni della notte precedente
            for player in game_screen.players:
                player["protected"] = False

            self.notte_inizializzata = self.day_number

            print("=== NUOVA NOTTE ===")
            print("Notte:", self.day_number)

        # Verifica se il giocatore locale ha già agito
        self.action_used = self.giocatore_ha_agito(
            game_screen.local_player_name
        )

        self.selected_player = ""

        # Recupera l'azione associata al ruolo
        ruolo = get_ruolo(self.local_player_role)

        if ruolo:
            self.current_action = ruolo.get("azione", "")
        else:
            self.current_action = ""

        # Elenco dei giocatori ancora vivi
        self.available_players = [
            player
            for player in game_screen.players
            if player.get("alive", False)
        ]

        self.update_players()

        print("=== SCHERMATA NOTTURNA ===")
        print("Giocatore:", game_screen.local_player_name)
        print("Ruolo:", self.local_player_role)
        print("Azione:", self.current_action)
        print("Ha già agito:", self.action_used)

    # ==========================================
    # AGGIORNAMENTO GIOCATORI
    # ==========================================

    def update_players(self):
        """
        Aggiorna l'elenco dei giocatori
        selezionabili come bersaglio.
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

    # ==========================================
    # SELEZIONE BERSAGLIO
    # ==========================================

    def select_player(self, player_name):
        """
        Seleziona il bersaglio dell'azione notturna.
        """

        if self.action_used:
            print("Hai già effettuato un'azione questa notte.")
            return

        self.selected_player = player_name

        print("Bersaglio selezionato:", player_name)

    # ==========================================
    # ESECUZIONE AZIONE
    # ==========================================

    def execute_action(self):
        """
        Registra l'azione notturna del giocatore locale.
        """

        game_screen = self.manager.get_screen("game")
        nome_locale = game_screen.local_player_name

        # Impedisce azioni duplicate
        if self.giocatore_ha_agito(nome_locale):
            self.action_used = True
            print("Azione già registrata questa notte.")
            return

        if not self.selected_player:
            print("Seleziona prima un bersaglio.")
            return

        if not self.current_action:
            print("Il tuo ruolo non possiede un'azione notturna.")
            return

        # Recupera il giocatore che agisce
        attore = next(
            (
                player
                for player in game_screen.players
                if player["name"] == nome_locale
            ),
            None
        )

        # Recupera il bersaglio
        bersaglio = next(
            (
                player
                for player in game_screen.players
                if player["name"] == self.selected_player
            ),
            None
        )

        if attore is None or not attore.get("alive", False):
            print("Giocatore locale non disponibile.")
            return

        if bersaglio is None or not bersaglio.get("alive", False):
            print("Bersaglio non disponibile.")
            return

        # Registra l'azione nel gestore
        risultato = self.gestore_notte.aggiungi_azione(
            self.current_action,
            attore,
            bersaglio
        )

        print("=== REGISTRAZIONE AZIONE ===")
        print(risultato)

        if risultato.get("successo", False):
            self.action_used = True

    # ==========================================
    # RISULTATI PRIVATI
    # ==========================================

    def ottieni_risultati_giocatore(self, nome_giocatore):
        """
        Recupera i risultati investigativi
        associati al giocatore indicato.
        """

        return list(
            self.casella_risultati.get(nome_giocatore, [])
        )

    def mostra_risultati_privati(self):
        """
        Visualizza i risultati investigativi
        del giocatore locale.
        """

        game_screen = self.manager.get_screen("game")
        nome_locale = game_screen.local_player_name

        risultati = self.ottieni_risultati_giocatore(
            nome_locale
        )

        if risultati:
            messaggi = [
                risultato.get("messaggio", "")
                for risultato in risultati
            ]

            testo = "\n".join(messaggi)

        else:
            testo = "Nessun risultato investigativo disponibile."

        self.dialog_risultati = MDDialog(
            title="Risultati delle indagini",
            text=testo,
            buttons=[
                MDFlatButton(
                    text="CHIUDI",
                    on_release=self.chiudi_dialog_risultati
                )
            ]
        )

        self.dialog_risultati.open()

    def chiudi_dialog_risultati(self, *args):
        """
        Chiude la finestra dei risultati.
        """

        if self.dialog_risultati:
            self.dialog_risultati.dismiss()
            self.dialog_risultati = None

    # ==========================================
    # RISOLUZIONE NOTTE
    # ==========================================

    def finish_night(self):
        """
        Risolve le azioni della notte,
        conserva i risultati investigativi
        e passa al giorno successivo.
        """

        game_screen = self.manager.get_screen("game")

        print("=== RISOLUZIONE NOTTE ===")

        # Risolve protezioni, investigazioni e attacchi
        risultati_pubblici = self.gestore_notte.risolvi()

        # Conserva le informazioni investigative
        # prima del reset del gestore
        for nome_giocatore, risultati in (
            self.gestore_notte.risultati_privati.items()
        ):

            self.casella_risultati.setdefault(
                nome_giocatore, []
            ).extend(risultati)

        # Mostra nel terminale solo i risultati
        # non contrassegnati come privati
        for risultato in risultati_pubblici:
            print(risultato)

        # Aggiorna i giocatori
        game_screen.update_players()

        # Passaggio alla fase diurna
        game_screen.phase = "giorno"
        game_screen.day_number += 1

        # Pulisce le azioni della notte conclusa,
        # mantenendo la casella dei risultati
        self.gestore_notte.reset()
        self.notte_inizializzata = None

        # Ritorna alla schermata di gioco
        self.manager.current = "game"
