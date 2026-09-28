from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ListProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock


class GameScreen(Screen):

    # =========================
    # STATO DELLA PARTITA
    # =========================

    day_number = NumericProperty(1)
    phase = StringProperty("giorno")

    # Per ora il giocatore locale è impostato manualmente.
    # In futuro arriverà dalla lobby.
    local_player_name = StringProperty("Alessio")
    local_player_role = StringProperty("IN ATTESA")

    # =========================
    # GIOCATORI
    # =========================

    players = ListProperty([
        {
            "name": "Alessio",
            "alive": True,
            "role": "Curatore"
        },
        {
            "name": "Marco",
            "alive": True,
            "role": "Lupo"
        },
        {
            "name": "Luca",
            "alive": True,
            "role": "Veggente"
        },
        {
            "name": "Sara",
            "alive": True,
            "role": "Serial Killer"
        }
    ])

    # =========================
    # INIZIALIZZAZIONE
    # =========================

    def on_kv_post(self, base_widget):
        self.update_local_player_role()
        self.update_players()

    def on_pre_enter(self):
        self.update_local_player_role()
        self.update_players()

        print("PROPERTY:", self.local_player_role)
        print("LABEL:", self.ids.role_label.text)

    # =========================
    # RUOLO GIOCATORE LOCALE
    # =========================

    def update_local_player_role(self):
        for player in self.players:
            if player["name"] == self.local_player_name:
                self.local_player_role = player.get("role", "IN ATTESA")
                return
            
        self.local_player_role = "IN ATTESA"

            
    # =========================
    # LISTA GIOCATORI
    # =========================

    def update_players(self):
        if "players_list" not in self.ids:
            return

        players_list = self.ids.players_list
        players_list.clear_widgets()

        for player in self.players:

            player_row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="45dp"
            )

            name_label = MDLabel(
                text=player["name"],
                font_style="Body1"
            )

            if player["alive"]:
                status = "VIVO"
                color = (0, 0.8, 0, 1)
            else:
                status = "MORTO"
                color = (0.8, 0, 0, 1)

            status_label = MDLabel(
                text=status,
                halign="right",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=color
            )

            player_row.add_widget(name_label)
            player_row.add_widget(status_label)

            players_list.add_widget(player_row)

    # =========================
    # ELIMINAZIONE GIOCATORE
    # =========================

    def kill_player(self, player_name):
        for player in self.players:
            if player["name"] == player_name:
                player["alive"] = False
                break

        self.update_players()

    # =========================
    # CAMBIO FASE
    # =========================

    def next_phase(self):
        if self.phase == "giorno":
            self.phase = "notte"
        else:
            self.phase = "giorno"
            self.day_number += 1

    # =========================
    # NAVIGAZIONE
    # =========================

    def open_vote(self):
        self.manager.current = "vote"

    def open_night(self):
        self.manager.current = "night"