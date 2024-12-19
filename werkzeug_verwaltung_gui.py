from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from werkzeug_verwaltung import WerkzeugVerwaltung

class WerkzeugScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.verwaltung = WerkzeugVerwaltung()

        # Überschrift
        self.add_widget(Label(
            text='Werkzeugverwaltung',
            size_hint_y=None,
            height=50
        ))

        # Buttons
        buttons = [
            ('Werkzeug hinzufügen', self.show_hinzufuegen),
            ('Werkzeug ausleihen', self.show_ausleihen),
            ('Werkzeug zurückgeben', self.show_zurueckgeben)
        ]
        
        for text, callback in buttons:
            self.add_widget(Button(
                text=text,
                size_hint_y=None,
                height=50,
                on_press=callback
            ))

        # Bestandsanzeige
        self.bestand_text = TextInput(
            readonly=True,
            multiline=True
        )
        self.add_widget(self.bestand_text)
        self.show_bestand()

    def show_bestand(self):
        text = ""
        if not self.verwaltung.werkzeuge:
            text = "Keine Werkzeuge im Bestand."
        else:
            for werkzeug in self.verwaltung.werkzeuge:
                status = "Verfügbar" if werkzeug.verfuegbar else f"Ausgeliehen an {werkzeug.ausgeliehen_an}"
                text += f"\nName: {werkzeug.name}\n"
                text += f"Producent: {werkzeug.producent}\n"
                text += f"Model: {werkzeug.model}\n"
                text += f"Status: {status}\n"
                text += "-" * 40 + "\n"
        self.bestand_text.text = text 

    def show_ausleihen(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Dropdown für verfügbare Werkzeuge
        verfuegbare_werkzeuge = [w.name for w in self.verwaltung.werkzeuge if w.verfuegbar]
        if not verfuegbare_werkzeuge:
            popup = Popup(
                title='Fehler',
                content=Label(text='Keine Werkzeuge verfügbar.'),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup.open()
            return

        werkzeug_input = TextInput(
            multiline=False,
            hint_text='Werkzeug Name'
        )
        person_input = TextInput(
            multiline=False,
            hint_text='Name der Person'
        )
        
        content.add_widget(Label(text='Verfügbare Werkzeuge:\n' + '\n'.join(verfuegbare_werkzeuge)))
        content.add_widget(werkzeug_input)
        content.add_widget(person_input)
        
        def ausleihen(instance):
            erfolg, nachricht = self.verwaltung.werkzeug_ausleihen(
                werkzeug_input.text.strip(),
                person_input.text.strip()
            )
            if erfolg:
                self.show_bestand()
                popup.dismiss()
            info = Popup(
                title='Info',
                content=Label(text=nachricht),
                size_hint=(None, None),
                size=(300, 200)
            )
            info.open()
        
        content.add_widget(Button(text='Ausleihen', on_press=ausleihen))
        
        popup = Popup(
            title='Werkzeug ausleihen',
            content=content,
            size_hint=(None, None),
            size=(400, 400)
        )
        popup.open()

    def show_zurueckgeben(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Liste der ausgeliehenen Werkzeuge
        ausgeliehene_werkzeuge = [
            f"{w.name} (ausgeliehen an {w.ausgeliehen_an})" 
            for w in self.verwaltung.werkzeuge 
            if not w.verfuegbar
        ]
        
        if not ausgeliehene_werkzeuge:
            popup = Popup(
                title='Info',
                content=Label(text='Keine Werkzeuge sind ausgeliehen.'),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup.open()
            return

        werkzeug_input = TextInput(
            multiline=False,
            hint_text='Werkzeug Name'
        )
        
        content.add_widget(Label(text='Ausgeliehene Werkzeuge:\n' + '\n'.join(ausgeliehene_werkzeuge)))
        content.add_widget(werkzeug_input)
        
        def zurueckgeben(instance):
            erfolg, nachricht = self.verwaltung.werkzeug_zurueckgeben(
                werkzeug_input.text.strip()
            )
            if erfolg:
                self.show_bestand()
                popup.dismiss()
            info = Popup(
                title='Info',
                content=Label(text=nachricht),
                size_hint=(None, None),
                size=(300, 200)
            )
            info.open()
        
        content.add_widget(Button(text='Zurückgeben', on_press=zurueckgeben))
        
        popup = Popup(
            title='Werkzeug zurückgeben',
            content=content,
            size_hint=(None, None),
            size=(400, 400)
        )
        popup.open()