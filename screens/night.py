from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty


class NightScreen(Screen):

    day_number = NumericProperty(1)

    def on_pre_enter(self):
        """
        Recupera il numero del giorno/notte
        dalla GameScreen.
        """

        game_screen = self.manager.get_screen("game")

        self.day_number = game_screen.day_number

    def finish_night(self):
        """
        Termina la notte e passa al giorno successivo.
        """

        game_screen = self.manager.get_screen("game")

        # Passaggio al giorno successivo
        game_screen.phase = "giorno"
        game_screen.day_number += 1

        # Ritorno alla schermata principale
        self.manager.current = "game"