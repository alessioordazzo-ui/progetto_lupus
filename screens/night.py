
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

        self.gestore_notte = GestoreNotte()
        self.notte_inizializzata = None

        # Archivio persistente dei risultati privati.
        self.casella_risultati = {}

        self.dialog_risultati = None

    # ==========================================
    # CONTROLLO AZIONI
    # ==========================================

    def giocatore_ha_agito(self, nome_giocatore):
        """
        Verifica se il giocatore ha già registrato
        un'azione nella notte corrente.
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

        Mantiene le azioni quando si rientra
        nella stessa notte.

        Rimuove gli effetti temporanei
        della giornata precedente.
        """

        game_screen = self.manager.get_screen("game")

        self.day_number = game_screen.day_number
        self.local_player_role = game_screen.local_player_role

        if self.notte_inizializzata != self.day_number:

            self.gestore_notte.reset()

            # Identifica la notte corrente
            # per la gestione dell'Investigatore.
            self.gestore_notte.imposta_notte(
                self.day_number
            )

            # Rimuove gli effetti temporanei
            # della notte e del giorno precedenti.
            for player in game_screen.players:

                # La protezione del Curatore
                # non dura oltre la notte.
                player["protected"] = False

                # Il silenzio termina all'inizio
                # della notte successiva.
                player["silenced"] = False

                # Il giocatore recupera
                # il diritto di voto.
                player["can_vote"] = True

            self.notte_inizializzata = self.day_number

            print("=== NUOVA NOTTE ===")
            print("Notte:", self.day_number)
            print("Effetti temporanei precedenti rimossi.")

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
        Aggiorna i giocatori selezionabili.
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
        Seleziona il bersaglio dell'azione.
        """

        if self.action_used:
            print("Hai già effettuato un'azione questa notte.")
            return

        self.selected_player = player_name

        print("Bersaglio selezionato:", player_name)

    # ==========================================
    # REGISTRAZIONE AZIONE
    # ==========================================

    def execute_action(self):
        """
        Registra l'azione notturna del giocatore locale.
        """

        game_screen = self.manager.get_screen("game")
        nome_locale = game_screen.local_player_name

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

        attore = next(
            (
                player
                for player in game_screen.players
                if player["name"] == nome_locale
            ),
            None
        )

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
        Restituisce i risultati privati
        conservati per il giocatore.
        """

        return list(
            self.casella_risultati.get(nome_giocatore, [])
        )

    def mostra_risultati_privati(self):
        """
        Mostra esclusivamente i risultati
        del giocatore locale.
        """

        game_screen = self.manager.get_screen("game")
        nome_locale = game_screen.local_player_name

        risultati = self.ottieni_risultati_giocatore(
            nome_locale
        )

        if risultati:
            testo = "\n".join(
                risultato.get("messaggio", "")
                for risultato in risultati
            )
        else:
            testo = "Nessun risultato privato disponibile."

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
    # CONCLUSIONE NOTTE
    # ==========================================

    def finish_night(self):
        """
        Risolve le azioni, conserva i risultati
        privati e avanza al giorno successivo.
        """

        game_screen = self.manager.get_screen("game")

        print("=== RISOLUZIONE NOTTE ===")

        risultati_pubblici = self.gestore_notte.risolvi()

        # Conserva i risultati privati
        # di Veggente, Investigatore e altri ruoli.
        for nome_giocatore, risultati in (
            self.gestore_notte.risultati_privati.items()
        ):
            self.casella_risultati.setdefault(
                nome_giocatore, []
            ).extend(risultati)

        for risultato in risultati_pubblici:
            print(risultato)

        game_screen.update_players()

        game_screen.phase = "giorno"
        game_screen.day_number += 1

        # Lo stato delle indagini rimane conservato
        # nel GestoreNotte.
        self.gestore_notte.reset()
        self.notte_inizializzata = None

        self.manager.current = "game"
