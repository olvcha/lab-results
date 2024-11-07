from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        # layout = BoxLayout(orientation='vertical')
        # layout.add_widget(Button(text='Go to New result Screen', on_press=self.switch_to_new_result_screen))
        # self.add_widget(layout)

    def switch_to_new_result_screen(self, instance):
        self.manager.current = 'new_result_screen'