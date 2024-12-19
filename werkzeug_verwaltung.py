import json
from datetime import datetime

class Werkzeug:
    def __init__(self, name, producent, model, serien_nummer, verfuegbar=True):
        self.name = name
        self.producent = producent
        self.model = model
        self.serien_nummer = serien_nummer
        self.verfuegbar = verfuegbar
        self.ausgeliehen_an = None
        self.historie = []  # Liste für die Ausleih-Historie

class WerkzeugVerwaltung:
    def __init__(self):
        self.werkzeuge = []
        self.load_data()

    def save_data(self):
        werkzeuge_data = []
        for werkzeug in self.werkzeuge:
            werkzeug_dict = {
                'name': werkzeug.name,
                'producent': werkzeug.producent,
                'model': werkzeug.model,
                'serien_nummer': werkzeug.serien_nummer,
                'verfuegbar': werkzeug.verfuegbar,
                'ausgeliehen_an': werkzeug.ausgeliehen_an,
                'historie': werkzeug.historie
            }
            werkzeuge_data.append(werkzeug_dict)
        
        with open('werkzeuge.json', 'w', encoding='utf-8') as f:
            json.dump(werkzeuge_data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        try:
            with open('werkzeuge.json', 'r', encoding='utf-8') as f:
                werkzeuge_data = json.load(f)
                for w_data in werkzeuge_data:
                    werkzeug = Werkzeug(
                        w_data['name'],
                        w_data['producent'],
                        w_data['model'],
                        w_data['serien_nummer']
                    )
                    werkzeug.verfuegbar = w_data['verfuegbar']
                    werkzeug.ausgeliehen_an = w_data['ausgeliehen_an']
                    werkzeug.historie = w_data.get('historie', [])  # Lädt die Historie, falls vorhanden
                    self.werkzeuge.append(werkzeug)
        except FileNotFoundError:
            pass

    def werkzeug_hinzufuegen(self, name, producent, model, serien_nummer):
        for werkzeug in self.werkzeuge:
            if werkzeug.name.lower() == name.lower():
                print(f"Ein Werkzeug mit dem Namen '{name}' existiert bereits!")
                return
        
        werkzeug = Werkzeug(name, producent, model, serien_nummer)
        self.werkzeuge.append(werkzeug)
        self.save_data()
        print(f"Werkzeug '{name}' wurde hinzugefügt.")

    def werkzeug_ausleihen(self, werkzeug_name, person):
        werkzeug_gefunden = False
        datum = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        for werkzeug in self.werkzeuge:
            if werkzeug.name.lower() == werkzeug_name.lower():
                werkzeug_gefunden = True
                if werkzeug.verfuegbar:
                    werkzeug.verfuegbar = False
                    werkzeug.ausgeliehen_an = person
                    # Historie-Eintrag hinzufügen
                    werkzeug.historie.append({
                        'aktion': 'Ausgeliehen',
                        'person': person,
                        'datum': datum
                    })
                    self.save_data()
                    print(f"Werkzeug '{werkzeug.name}' wurde am {datum} an {person} ausgeliehen.")
                else:
                    print(f"Werkzeug '{werkzeug.name}' ist bereits ausgeliehen an {werkzeug.ausgeliehen_an}.")
                break
        
        if not werkzeug_gefunden:
            print(f"Werkzeug '{werkzeug_name}' nicht gefunden.")

    def werkzeug_zurueckgeben(self, werkzeug_name):
        werkzeug_gefunden = False
        datum = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        for werkzeug in self.werkzeuge:
            if werkzeug.name.lower() == werkzeug_name.lower():
                werkzeug_gefunden = True
                if not werkzeug.verfuegbar:
                    person = werkzeug.ausgeliehen_an
                    werkzeug.verfuegbar = True
                    werkzeug.ausgeliehen_an = None
                    # Historie-Eintrag hinzufügen
                    werkzeug.historie.append({
                        'aktion': 'Zurückgegeben',
                        'person': person,
                        'datum': datum
                    })
                    self.save_data()
                    print(f"Werkzeug '{werkzeug.name}' wurde am {datum} zurückgegeben.")
                else:
                    print(f"Werkzeug '{werkzeug.name}' war nicht ausgeliehen.")
                break
        
        if not werkzeug_gefunden:
            print(f"Werkzeug '{werkzeug_name}' nicht gefunden.")

    def historie_anzeigen(self, werkzeug_name):
        for werkzeug in self.werkzeuge:
            if werkzeug.name.lower() == werkzeug_name.lower():
                print(f"\nHistorie für Werkzeug '{werkzeug.name}':")
                print("-" * 50)
                if werkzeug.historie:
                    for eintrag in werkzeug.historie:
                        print(f"Aktion: {eintrag['aktion']}")
                        print(f"Person: {eintrag['person']}")
                        print(f"Datum: {eintrag['datum']}")
                        print("-" * 50)
                else:
                    print("Keine Historie vorhanden.")
                return
        print(f"Werkzeug '{werkzeug_name}' nicht gefunden.")

    def bestand_anzeigen(self):
        if not self.werkzeuge:
            print("Keine Werkzeuge im Bestand.")
            return
        
        print("\nAktueller Werkzeugbestand:")
        print("-" * 50)
        for werkzeug in self.werkzeuge:
            status = "Verfügbar" if werkzeug.verfuegbar else f"Ausgeliehen an {werkzeug.ausgeliehen_an}"
            print(f"Name: {werkzeug.name}")
            print(f"Producent: {werkzeug.producent}")
            print(f"Model: {werkzeug.model}")
            print(f"Serien Nummer: {werkzeug.serien_nummer}")
            print(f"Status: {status}")
            if werkzeug.historie:
                letzter_eintrag = werkzeug.historie[-1]
                print(f"Letzte Aktion: {letzter_eintrag['aktion']} von {letzter_eintrag['person']} am {letzter_eintrag['datum']}")
            print("-" * 50)

if __name__ == "__main__":
    verwaltung = WerkzeugVerwaltung()
    
    while True:
        print("\nWerkzeugverwaltung - Menü:")
        print("1. Werkzeug hinzufügen")
        print("2. Werkzeug ausleihen")
        print("3. Werkzeug zurückgeben")
        print("4. Bestand anzeigen")
        print("5. Historie anzeigen")
        print("6. Programm beenden")
        
        wahl = input("\nBitte wählen Sie eine Option (1-6): ")
        
        if wahl == "1":
            name = input("Name des Werkzeugs: ")
            producent = input("Producent des Werkzeugs: ")
            model = input("Model des Werkzeugs: ")
            serien_nummer = input("Serien Nummer des Werkzeugs: ")
            verwaltung.werkzeug_hinzufuegen(name, producent, model, serien_nummer)
        
        elif wahl == "2":
            name = input("Name des Werkzeugs: ")
            person = input("Name der Person: ")
            verwaltung.werkzeug_ausleihen(name, person)
        
        elif wahl == "3":
            name = input("Name des Werkzeugs: ")
            verwaltung.werkzeug_zurueckgeben(name)
        
        elif wahl == "4":
            verwaltung.bestand_anzeigen()
        
        elif wahl == "5":
            name = input("Name des Werkzeugs: ")
            verwaltung.historie_anzeigen(name)
        
        elif wahl == "6":
            print("Programm wird beendet.")
            break
        
        else:
            print("Ungültige Eingabe! Bitte wählen Sie eine Zahl zwischen 1 und 6.")