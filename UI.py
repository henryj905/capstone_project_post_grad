from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import PlayerStatsUI
import PredictorUI
import TeamStatsUI

stats = ['passing', 'rushing', 'receiving', 'sacks', 'special']


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
        stats_btn.bind(on_press=self.go_to_years)
        layout.add_widget(stats_btn)

        predictor_btn = Button(
            text="Predictor",
            size_hint=(1, 0.25)
        )
        predictor_btn.bind(on_press=self.go_to_predictor)
        layout.add_widget(predictor_btn)

        self.add_widget(layout)

    def go_to_years(self, instance):
        self.manager.current = "years"

    def go_to_predictor(self, instance):
        self.manager.current = "predictor_main"


class YearScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        main_layout.add_widget(Label(text="Select a Year", font_size=30, size_hint=(1, 0.1)))

        scroll = ScrollView()

        grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        years = list(range(2017, 2025))

        for year in years:
            btn = Button(text=f"{year}", size_hint_y=None, height=60)
            btn.bind(on_press=self.load_year)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def load_year(self, instance):
        year = int(instance.text)

        stat_screen = self.manager.get_screen("statistics")
        stat_screen.load_year(year)

        self.manager.current = "statistics"

    def go_back(self, instance):
        self.manager.current = "main"


class WhichStatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.compare_mode = False
        self.main_player = None
        self.main_team = None
        self.main_stat = None

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title_label = Label(text="Pick Player's Stats", font_size=30, size_hint=(1, 0.1))
        main_layout.add_widget(self.title_label)

        scroll = ScrollView()

        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)  # cleaner layout
        grid.bind(minimum_height=grid.setter('height'))

        stats = ['passing', 'rushing', 'receiving', 'sacks', 'special']

        for stat in stats:
            btn = Button(text=stat.capitalize(), size_hint_y=None, height=60)

            # 👇 FIX: pass stat correctly
            btn.bind(on_press=lambda instance, s=stat: self.load_players(s))

            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def load_team(self, team_name, year):
        self.team = team_name
        self.year = year

        self.title_label.text = f"{team_name} Player Stats ({year})"

    def load_players(self, stat):
        player_list_screen = self.manager.get_screen('player_list')

        player_list_screen.load_team(self.team, self.year, stat)

        # 🚨 pass compare info
        player_list_screen.compare_mode = self.compare_mode
        player_list_screen.main_player = self.main_player
        player_list_screen.main_team = self.main_team
        player_list_screen.main_stat = self.main_stat

        self.manager.current = 'player_list'

    def go_back(self, instance):
        self.manager.current = "statistics"


class MyApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainMenu(name="main"))
        sm.add_widget(YearScreen(name="years"))
        sm.add_widget(TeamStatsUI.StatsScreen(name="statistics"))
        sm.add_widget(TeamStatsUI.StatTypeScreen(name="stat_type"))
        sm.add_widget(TeamStatsUI.TeamStatsScreen(name="team_stats"))
        sm.add_widget(WhichStatScreen(name="which_one"))
        sm.add_widget(TeamStatsUI.CompareScreen(name="compare_teams"))
        sm.add_widget(PlayerStatsUI.PlayerStatScreen(name='player_stats'))
        sm.add_widget(PlayerStatsUI.PlayerListScreen(name='player_list'))
        sm.add_widget(PlayerStatsUI.PlayerCompare(name='player_compare'))
        sm.add_widget(PlayerStatsUI.TeamPickPlayer(name='second_team'))
        sm.add_widget(PredictorUI.PredictorMain(name="predictor_main"))
        sm.add_widget(PredictorUI.WeekScreen(name='weeks'))
        sm.add_widget(PredictorUI.LoadTeams(name='teams'))
        sm.add_widget(PredictorUI.PredictorScreen(name='predictor'))
        return sm


if __name__ == "__main__":
    MyApp().run()
