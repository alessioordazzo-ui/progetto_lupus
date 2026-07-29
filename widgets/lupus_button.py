from kivy.uix.button import Button
from utils.theme import Theme


class LupusButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""

        self.background_color = Theme.BUTTON

        self.color = Theme.TEXT

        self.font_size = "22sp"

        self.size_hint = (.7, .08)

        self.bold = True