from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from screens.menu import MenuScreen
from utils.theme import LupusTheme
from widgets.lupus_section import LupusSection
from widgets.lupus_textfield import LupusTextField
from widgets.lupus_counter import LupusCounter
from widgets.lupus_player_card import LupusPlayerCard
from widgets.lupus_lobby_code import LupusLobbyCode
from screens.waiting_room import WaitingRoomScreen
from screens.game import GameScreen


class LupusApp(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"

        Builder.load_file("kv/menu.kv")
        Builder.load_file("kv/lupus_card.kv")
        Builder.load_file("kv/widgets/lupus_section.kv")
        Builder.load_file("kv/widgets/lupus_textfield.kv")
        Builder.load_file("kv/widgets/lupus_counter.kv")
        Builder.load_file("kv/widgets/lupus_player_card.kv")
        Builder.load_file("kv/widgets/lupus_lobby_code.kv")
        Builder.load_file("kv/waiting_room.kv")
        Builder.load_file("kv/game.kv")

        sm = ScreenManager()

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(WaitingRoomScreen(name="waiting_room"))
        sm.add_widget(GameScreen(name="game"))

        sm.current = "waiting_room"

        return sm

if __name__ == "__main__":
    LupusApp().run()