from kivy.uix.label import Label
from utils.theme import Theme


class LupusTitle(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.color = Theme.TEXT

        self.bold = True

        self.font_size = "42sp"