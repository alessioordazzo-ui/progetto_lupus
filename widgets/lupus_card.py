from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from utils.theme import Theme


class LupusCard(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        with self.canvas.before:
            Color(*Theme.SURFACE)
            self.rect = RoundedRectangle(radius=[18])

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size