from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty


class GameScreen(Screen):

    day_number = NumericProperty(1)

    phase = StringProperty("giorno")

    def next_phase(self):
        if self.phase == "giorno":
            self.phase = "notte"
        else:
            self.phase = "giorno"
            self.day_number += 1