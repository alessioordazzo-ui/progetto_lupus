from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class LupusSection(BoxLayout):
    title = StringProperty("")
    icon = StringProperty("")