from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

from pos import Pos


class Menu(Screen):
    """Main menu."""

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def goto_pos(self):
        app = App.get_running_app()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'pos'

        app.config.read(app.get_application_config())
        app.config.write()
