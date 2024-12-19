from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class WerkzeugScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Überschrift
        self.add_widget(Label(
            text='Werkzeugverwaltung',
            size_hint_y=None,
            height=50
        ))

        # Buttons
        self.add_widget(Button(
            text='Werkzeug hinzufügen',
            size_hint_y=None,
            height=50
        ))
        self.add_widget(Button(
            text='Werkzeug ausleihen',
            size_hint_y=None,
            height=50
        ))
        self.add_widget(Button(
            text='Werkzeug zurückgeben',
            size_hint_y=None,
            height=50
        ))

        # Bestandsanzeige
        self.bestand_text = TextInput(
            text='Werkzeugbestand wird hier angezeigt...',
            readonly=True,
            multiline=True,
            size_hint=(1, 1)
        )
        self.add_widget(self.bestand_text)

class WerkzeugApp(App):
    def build(self):
        return WerkzeugScreen()

if __name__ == '__main__':
    WerkzeugApp().run() 