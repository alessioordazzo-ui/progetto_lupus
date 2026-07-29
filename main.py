from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from widgets.lupus_button import LupusButton
from widgets.lupus_title import LupusTitle
from screens.splash import SplashScreen
from screens.menu import MenuScreen

Builder.load_file("kv/splash.kv")
Builder.load_file("kv/menu.kv")


class LupusApp(App):

    def build(self):

        sm = ScreenManager()

        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MenuScreen(name="menu"))

        sm.current = "menu"   # Per ora mostriamo direttamente il menu

        return sm


if __name__ == "__main__":
    LupusApp().run()