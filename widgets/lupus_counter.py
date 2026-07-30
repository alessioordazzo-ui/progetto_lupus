from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout


class LupusCounter(BoxLayout):

    value = NumericProperty(10)
    minimum = NumericProperty(4)
    maximum = NumericProperty(30)

    def increase(self):
        if self.value < self.maximum:
            self.value += 1

    def decrease(self):
        if self.value > self.minimum:
            self.value -= 1