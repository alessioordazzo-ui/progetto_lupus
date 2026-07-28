# interfaccia.py
# Interfaccia grafica Kivy/KivyMD con due schermate separate:
# - SchermataNarratore: lista completa di giocatori + ruoli + stato
# - SchermataGiocatore: solo il proprio ruolo, e se è un Lupo, i suoi compagni
#
# NOTA SUL TEST IN LOCALE (senza rete):
# Finché non c'è il networking (Fase 4), non esiste ancora un modo per un
# telefono di "sapere" automaticamente quale giocatore è. Per questo nel menu
# c'è uno spinner per scegliere manualmente "chi sei". Quando arriverà la rete,
# questa scelta sparirà: sarà il server a sapere quale client è quale giocatore,
# e a mandare a ciascuno solo la sua vista_giocatore() via socket/JSON.

from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

import gioco  # tutta la logica di partita vive in gioco.py


class SchermataMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", spacing="20dp", padding="40dp")
        self.add_widget(self.layout)
        self._costruisci_menu()

    def _costruisci_menu(self):
        self.layout.clear_widgets()

        self.layout.add_widget(MDLabel(text="Lupus App", halign="center", font_style="H3"))

        bottone_narratore = MDRaisedButton(
            text="Sono il Narratore",
            pos_hint={"center_x": 0.5},
            on_release=self.vai_a_narratore,
        )
        self.layout.add_widget(bottone_narratore)

        self.layout.add_widget(MDLabel(
            text="Oppure entra come Giocatore (solo per test locale):",
            halign="center",
        ))

        self.spinner_giocatori = Spinner(
            text="Scegli un giocatore",
            values=list(gioco.giocatori_connessi),
            size_hint=(None, None),
            size=("240dp", "48dp"),
            pos_hint={"center_x": 0.5},
        )
        self.layout.add_widget(self.spinner_giocatori)

        bottone_giocatore = MDRaisedButton(
            text="Entra come Giocatore",
            pos_hint={"center_x": 0.5},
            on_release=self.vai_a_giocatore,
        )
        self.layout.add_widget(bottone_giocatore)

    def vai_a_narratore(self, *args):
        self.manager.get_screen("narratore").aggiorna()
        self.manager.current = "narratore"

    def vai_a_giocatore(self, *args):
        nome_scelto = self.spinner_giocatori.text
        if nome_scelto not in gioco.giocatori_connessi:
            return  # nessun giocatore valido selezionato, non facciamo nulla
        self.manager.get_screen("giocatore").imposta_giocatore(nome_scelto)
        self.manager.current = "giocatore"


class SchermataNarratore(Screen):
    """Il Narratore vede TUTTI i giocatori, il loro ruolo, la fazione e se sono vivi."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", padding="20dp", spacing="10dp")
        self.add_widget(self.layout)
        self.spinner_bersaglio = None

    def aggiorna(self):
        self.layout.clear_widgets()
        self.layout.add_widget(MDLabel(text="Pannello Narratore", halign="center", font_style="H5"))

        area_scroll = ScrollView()
        lista = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing="6dp")
        lista.bind(minimum_height=lista.setter("height"))

        for riga in gioco.vista_narratore():
            stato = "VIVO" if riga["vivo"] else "MORTO"
            testo = f"{riga['nome']} — {riga['ruolo']} ({riga['fazione']}) — {stato}"
            lista.add_widget(MDLabel(text=testo, size_hint_y=None, height="30dp"))

        area_scroll.add_widget(lista)
        self.layout.add_widget(area_scroll)

        # Azione: elimina un giocatore (solo tra i vivi)
        vivi = [nome for nome, info in gioco.partita.items() if info["vivo"]]
        self.spinner_bersaglio = Spinner(
            text="Scegli chi eliminare",
            values=vivi,
            size_hint=(None, None),
            size=("240dp", "48dp"),
            pos_hint={"center_x": 0.5},
        )
        self.layout.add_widget(self.spinner_bersaglio)

        bottone_elimina = MDRaisedButton(
            text="Elimina giocatore",
            pos_hint={"center_x": 0.5},
            on_release=self.elimina_bersaglio,
        )
        self.layout.add_widget(bottone_elimina)

        bottone_indietro = MDRaisedButton(
            text="Torna al menu",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: setattr(self.manager, "current", "menu"),
        )
        self.layout.add_widget(bottone_indietro)

    def elimina_bersaglio(self, *args):
        nome_bersaglio = self.spinner_bersaglio.text
        if nome_bersaglio in gioco.partita:
            gioco.lincia_giocatore(nome_bersaglio)
        self.aggiorna()  # ridisegna la schermata con lo stato aggiornato


class SchermataGiocatore(Screen):
    """Il Giocatore vede SOLO il proprio ruolo. Se è un Lupo, può vedere i compagni."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical", padding="30dp", spacing="15dp")
        self.add_widget(self.layout)
        self.nome_giocatore = None

    def imposta_giocatore(self, nome):
        self.nome_giocatore = nome
        self._disegna()

    def _disegna(self):
        self.layout.clear_widgets()
        dati = gioco.vista_giocatore(self.nome_giocatore)

        self.layout.add_widget(MDLabel(text=f"Ciao {dati['nome']}", halign="center", font_style="H5"))
        self.layout.add_widget(MDLabel(text=f"Il tuo ruolo: {dati['ruolo']}", halign="center", font_style="H6"))
        self.layout.add_widget(MDLabel(text=dati["descrizione"], halign="center"))

        if not dati["vivo"]:
            self.layout.add_widget(MDLabel(text="☠️ Sei morto: puoi ancora guardare, non parlare.", halign="center"))

        # Solo i Lupi vedono questo bottone: per tutti gli altri, altri_lupi è None
        if dati["altri_lupi"] is not None:
            bottone_lupi = MDRaisedButton(
                text="🐺 Vedi gli altri Lupi",
                pos_hint={"center_x": 0.5},
                on_release=self.mostra_altri_lupi,
            )
            self.layout.add_widget(bottone_lupi)

        bottone_indietro = MDRaisedButton(
            text="Torna al menu",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: setattr(self.manager, "current", "menu"),
        )
        self.layout.add_widget(bottone_indietro)

    def mostra_altri_lupi(self, *args):
        dati = gioco.vista_giocatore(self.nome_giocatore)
        compagni = dati["altri_lupi"]

        if compagni:
            testo = "\n".join(f"{c['nome']} ({'vivo' if c['vivo'] else 'morto'})" for c in compagni)
        else:
            testo = "Sei l'unico Lupo rimasto in partita."

        popup = Popup(
            title="I tuoi compagni Lupi",
            content=MDLabel(text=testo, halign="center"),
            size_hint=(0.8, 0.5),
        )
        popup.open()


class LupusApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"

        # Assegna i ruoli una volta sola, all'avvio dell'app
        gioco.assegna_ruoli()

        sm = ScreenManager()
        sm.add_widget(SchermataMenu(name="menu"))
        sm.add_widget(SchermataNarratore(name="narratore"))
        sm.add_widget(SchermataGiocatore(name="giocatore"))
        return sm


if __name__ == "__main__":
    LupusApp().run()