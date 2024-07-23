import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty

# Lista delle squadre di Serie A
clubs = [
    "Atalanta", "Bologna", "Cagliari", "Empoli", "Fiorentina", "Genoa", "Inter", 
    "Juventus", "Lazio", "Lecce", "Milan", "Napoli", "Roma", "Salernitana", 
    "Sampdoria", "Sassuolo", "Spezia", "Torino", "Udinese", "Verona"
]

# Funzione per calcolare le statistiche in base al ruolo
def calculate_stats(role, is_goalkeeper):
    stats = {
        "goals": 0,
        "assists": 0,
        "clean_sheets": 0  # Contatore per le reti inviolate (solo per Portiere)
    }

    if role == "Portiere" and is_goalkeeper:
        stats["clean_sheets"] = random.randint(0, 15)  # Numero casuale di reti inviolate
    else:
        stats["goals"] = calculate_goals(role)
        stats["assists"] = calculate_assists(role)

    return stats

# Funzione per calcolare i gol in base al ruolo
def calculate_goals(role):
    if role in ["Difensore", "Portiere"]:
        return random.choices([0, 1], [0.9, 0.1])[0]  # 10% di probabilità di fare un gol
    else:
        return random.randint(1, 50)

# Funzione per calcolare gli assist in base al ruolo
def calculate_assists(role):
    if role in ["Difensore", "Portiere"]:
        return random.choices([0, 1], [0.85, 0.15])[0]  # 15% di probabilità di fare un assist
    else:
        return random.randint(1, 30)

class CareerSimulator(BoxLayout):
    result_text = StringProperty()
    role = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_club = ""
        self.current_age = 0
        self.trophies_accumulated = 0
        self.ballon_dor_won = False
        self.player_stats = {
            "goals": 0,
            "assists": 0,
            "clean_sheets": 0
        }

    def start_career(self):
        self.selected_club = random.choice(clubs)
        self.current_age = 16  # Inizia la carriera a 16 anni
        self.trophies_accumulated = 0
        self.ballon_dor_won = False
        self.player_stats = {
            "goals": 0,
            "assists": 0,
            "clean_sheets": 0
        }
        self.simulate_next_two_years()

    def simulate_next_two_years(self):
        stats = calculate_stats(self.role, self.role == "Portiere")

        self.player_stats["goals"] += stats["goals"]
        self.player_stats["assists"] += stats["assists"]
        self.player_stats["clean_sheets"] += stats["clean_sheets"]

        self.current_age += 2

        if self.current_age > 40:
            self.show_message("Fine della Carriera", self.generate_stats_message())
            if self.ballon_dor_won:
                self.show_goat_message()
            self.current_age = 16
            self.trophies_accumulated = 0
            self.ballon_dor_won = False
            self.player_stats = {
                "goals": 0,
                "assists": 0,
                "clean_sheets": 0
            }
        else:
            self.trophies_accumulated += random.randint(0, 2)
            if random.random() < 0.01:
                self.ballon_dor_won = True

        self.update_results()

    def generate_stats_message(self):
        return f"Riepilogo della Carriera:\n\n" \
               f"Gol totali: {self.player_stats['goals']}\n" \
               f"Assist totali: {self.player_stats['assists']}\n" \
               f"Reti inviolate (solo per Portiere): {self.player_stats['clean_sheets']}\n" \
               f"Trofei totali: {self.trophies_accumulated}\n" \
               f"Pallone d'Oro: {'Sì' if self.ballon_dor_won else 'No'}"

    def show_message(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.8))
        popup.open()

    def show_goat_message(self):
        self.show_message("Congratulazioni!", "SEI IL GOAT")

    def choose_team(self):
        def select_team(new_team):
            self.selected_club = new_team
            choose_team_popup.dismiss()
            self.simulate_next_two_years()

        team1 = random.choice(clubs)
        team2 = random.choice([club for club in clubs if club != team1])

        choose_team_layout = BoxLayout(orientation='vertical')
        btn_team1 = Button(text=team1, on_release=lambda *args: select_team(team1))
        btn_team2 = Button(text=team2, on_release=lambda *args: select_team(team2))

        choose_team_layout.add_widget(btn_team1)
        choose_team_layout.add_widget(btn_team2)

        choose_team_popup = Popup(title="Scegli una squadra", content=choose_team_layout, size_hint=(0.8, 0.8))
        choose_team_popup.open()

    def update_results(self):
        self.result_text = f"Età: {self.current_age}\n" \
                           f"Ruolo: {self.role}\n" \
                           f"Club: {self.selected_club}\n" \
                           f"Gol: {self.player_stats['goals']}\n" \
                           f"Assist: {self.player_stats['assists']}\n" \
                           f"Reti inviolate: {self.player_stats['clean_sheets']}\n" \
                           f"Trofei: {self.trophies_accumulated}"

class CareerApp(App):
    def build(self):
        return CareerSimulator()

if __name__ == '__main__':
    CareerApp().run()
