from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition

class Pos(Screen):
    """Pos main."""

    def menu(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'menu'
        # self.manager.get_screen('login').resetForm()
