from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import MainFile

# ------------------ MAIN MENU ------------------
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        layout.add_widget(Label(
            text="NFL Predictor",
            font_size=40,
            size_hint=(1, 0.3)
        ))

        layout.add_widget(Label(
            text="Henry Johnson",
            font_size=20,
            size_hint=(1, 0.2)
        ))

        stats_btn = Button(
            text="Statistics",
            size_hint=(1, 0.25)
        )
        stats_btn.bind(on_press=self.go_to_stats)
        layout.add_widget(stats_btn)

        predictor_btn = Button(
            text="Predictor",
            size_hint=(1, 0.25)
        )
        predictor_btn.bind(on_press=self.go_to_predictor)
        layout.add_widget(predictor_btn)

        self.add_widget(layout)

    def go_to_stats(self, instance):
        self.manager.current = "stats"

    def go_to_predictor(self, instance):
        self.manager.current = "predictor"


# ------------------ STATISTICS SCREEN ------------------

class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        main_layout.add_widget(Label(text="Select a Team", font_size=30, size_hint=(1, 0.1)))

        scroll = ScrollView()

        grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        teams = MainFile.teams()

        for team in teams:
            btn = Button(text=team, size_hint_y=None, height=60)
            btn.bind(on_press=self.team_selected)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def team_selected(self, instance):
        team_name = instance.text

        stat_screen = self.manager.get_screen("stat_type")
        stat_screen.load_team(team_name)

        self.manager.current = "stat_type"

    def go_back(self, instance):
        self.manager.current = "menu"


# ------------------ PREDICTOR SCREEN ------------------

class PredictorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20)

        layout.add_widget(Label(text="Predictor Page", font_size=30))

        back_btn = Button(text="Back")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "menu"

class StatTypeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_team = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.title = Label(text="", font_size=30)
        layout.add_widget(self.title)

        team_btn = Button(text="Team Stats")
        team_btn.bind(on_press=self.go_to_team_stats)
        layout.add_widget(team_btn)

        player_btn = Button(text="Player Stats")
        player_btn.bind(on_press=self.go_to_player_stats)
        layout.add_widget(player_btn)

        back_btn = Button(text="Back")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def load_team(self, team_name):
        self.selected_team = team_name
        self.title.text = f"{team_name}"

    def go_to_team_stats(self, instance):
        screen = self.manager.get_screen("team_stats")
        screen.load_team(self.selected_team)
        self.manager.current = "team_stats"

    def go_to_player_stats(self, instance):
        screen = self.manager.get_screen("player_stats")
        screen.load_team(self.selected_team)
        self.manager.current = "player_stats"

    def go_back(self, instance):
        self.manager.current = "stats"


# ------------------ TEAM STATS SCREEN ------------------

class TeamStatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text="Team Stats", font_size=30)
        self.layout.add_widget(self.label)

        self.stats_label = Label(text="", font_size=18)
        self.layout.add_widget(self.stats_label)

        back_btn = Button(text="Back")
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def load_team(self, team_name):
        self.label.text = f"{team_name} Stats"

        # Replace this with your actual data logic
        self.stats_label.text = f"Showing stats for {team_name}"

    def go_back(self, instance):
        self.manager.current = "stats"




class PlayerStatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text="Player Stats", font_size=30)
        layout.add_widget(self.label)

        self.content = Label(text="")
        layout.add_widget(self.content)

        back_btn = Button(text="Back")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def load_team(self, team_name):
        self.label.text = f"{team_name} Player Stats"

        # Replace with real logic later
        self.content.text = f"Showing player stats for {team_name}"

    def go_back(self, instance):
        self.manager.current = "stats"
# ------------------ APP ------------------

class MyApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(StatsScreen(name="stats"))
        sm.add_widget(PredictorScreen(name="predictor"))
        sm.add_widget(StatTypeScreen(name="stat_type"))
        sm.add_widget(TeamStatsScreen(name="team_stats"))
        sm.add_widget(PlayerStatsScreen(name="player_stats"))
        return sm


if __name__ == "__main__":
    MyApp().run()