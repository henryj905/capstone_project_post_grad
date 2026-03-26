from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import MainFile
import OffensivePerTeam

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

        self.manager.current = "year_selection"

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
        self.selected_year = None

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
        self.title.text = team_name

    def load_year(self, year):
        self.selected_year = year
        self.title.text = f"{year}"

    def go_to_team_stats(self, instance):
        screen = self.manager.get_screen("team_stats")
        screen.load_team(self.selected_team, self.selected_year)
        self.manager.current = "team_stats"

    def go_to_player_stats(self, instance):
        screen = self.manager.get_screen("player_stats")
        screen.load_team(self.selected_team)
        self.manager.current = "player_stats"

    def go_back(self, instance):
        self.manager.current = "year_selection"


class YearSelection(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_year = None
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title = Label(text="Year", font_size=30)
        main_layout.add_widget(self.title)

        scroll = ScrollView()

        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        years = list(range(2017, 2025))
        for year in years:
            year_btn = Button(text=f"{year}", size_hint_y=None, height = 60)
            year_btn.bind(on_press=self.go_to_stat_screen)
            grid.add_widget(year_btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.2))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def load_year(self, instance):
        year = instance.text

        stat_screen = self.manager.get_screen("stat_type")
        stat_screen.load_team(year)

        self.manager.current = "stat_type"
    def go_to_stat_screen(self, instance):
        screen = self.manager.get_screen("stat_type")
        screen.load_year(self.selected_year)
        self.manager.current = "stat_type"

    def go_back(self, instance):
        self.manager.current = "stats"

# ------------------ TEAM STATS SCREEN ------------------
class TeamStatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.team_name = None
        self.compare_team = None

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title
        self.label = Label(text="Team Stats", font_size=30, size_hint=(1, 0.1))
        self.layout.add_widget(self.label)

        # Scrollable grid for stats
        scroll = ScrollView()
        self.stats_grid = GridLayout(
            cols=2,
            spacing=5,
            size_hint_y=None
        )
        self.stats_grid.bind(minimum_height=self.stats_grid.setter('height'))
        scroll.add_widget(self.stats_grid)
        self.layout.add_widget(scroll)

        # Button row (Back + Compare)
        btn_row = BoxLayout(size_hint=(1, 0.1), spacing=10)
        back_btn = Button(text="Back")
        back_btn.bind(on_press=self.go_back)
        compare_btn = Button(text="Compare")
        compare_btn.bind(on_press=self.go_to_compare)
        btn_row.add_widget(back_btn)
        btn_row.add_widget(compare_btn)
        self.layout.add_widget(btn_row)

        self.add_widget(self.layout)

    # Helper to create aligned labels
    def create_label(self, text, align):
        lbl = Label(
            text=str(text),
            halign=align,
            size_hint=(None, None)
        )
        lbl.bind(texture_size=lbl.setter('size'))
        return lbl

    # Load a single team
    def load_team(self, team_name, year):
        self.team_name = team_name
        self.year = year
        self.compare_team = None
        self.label.text = f"{team_name} Stats"
        self.display_single_team()

    # Display stats for one team
    def display_single_team(self):
        try:
            stat, num = OffensivePerTeam.team_season(self.team_name, self.year)
            self.stats_grid.clear_widgets()
            self.stats_grid.cols = 2

            for s, n in zip(stat, num):
                self.stats_grid.add_widget(self.create_label(s, "left"))
                self.stats_grid.add_widget(self.create_label(n, "right"))

        except Exception as e:
            self.stats_grid.clear_widgets()
            self.stats_grid.add_widget(Label(text=f"Error: {e}"))

    # Display stats for two teams side-by-side
    def display_comparison(self):
        try:
            stat1, num1 = OffensivePerTeam.team_season(self.team_name, self.year)
            stat2, num2 = OffensivePerTeam.team_season(self.compare_team, self.year)

            self.stats_grid.clear_widgets()
            self.stats_grid.cols = 4

            # Optional headers
            self.stats_grid.add_widget(self.create_label(self.team_name, "center"))
            self.stats_grid.add_widget(Label(text=""))  # spacer
            self.stats_grid.add_widget(self.create_label(self.compare_team, "center"))
            self.stats_grid.add_widget(Label(text=""))  # spacer

            for i in range(len(stat1)):
                self.stats_grid.add_widget(self.create_label(stat1[i], "left"))
                self.stats_grid.add_widget(self.create_label(num1[i], "right"))
                self.stats_grid.add_widget(self.create_label(stat2[i], "left"))
                self.stats_grid.add_widget(self.create_label(num2[i], "right"))

        except Exception as e:
            self.stats_grid.clear_widgets()
            self.stats_grid.add_widget(Label(text=f"Error: {e}"))

    # Go to compare screen to pick another team
    def go_to_compare(self, instance):
        compare_screen = self.manager.get_screen("compare")
        compare_screen.set_main_team(self.team_name)
        self.manager.current = "compare"

    # Go back to stats menu
    def go_back(self, instance):
        self.manager.current = "stats"

class CompareScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_team = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Select Team to Compare", font_size=30))

        scroll = ScrollView()
        grid = GridLayout(cols=4, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        teams = MainFile.teams()
        for team in teams:
            btn = Button(text=team, size_hint_y=None, height=60)
            btn.bind(on_press=self.select_team)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def set_main_team(self, team):
        self.main_team = team

    def select_team(self, instance):
        compare_team = instance.text
        stats_screen = self.manager.get_screen("team_stats")
        stats_screen.compare_team = compare_team
        stats_screen.display_comparison()
        self.manager.current = "team_stats"


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
        sm.add_widget(CompareScreen(name="compare"))
        sm.add_widget(YearSelection(name="year_selection"))
        return sm


if __name__ == "__main__":
    MyApp().run()