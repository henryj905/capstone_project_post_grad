from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import MainFile

class PredictorMain(Screen):
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

        week_screen = self.manager.get_screen("weeks")
        week_screen.load_year(year)

        self.manager.current = "weeks"


    def go_back(self, instance):
        self.manager.current = "main"

class WeekScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = None

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        main_layout.add_widget(Label(text="Select a Year", font_size=30, size_hint=(1, 0.1)))

        scroll = ScrollView()

        grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        weeks = list(range(1, 19))

        for week in weeks:
            btn = Button(text=f"{week}", size_hint_y=None, height=60)
            btn.bind(on_press=self.load_week)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def load_week(self, instance):
        week = int(instance.text)

        stat_screen = self.manager.get_screen("teams")
        stat_screen.load_week(week)

        self.manager.current = "teams"

    def load_year(self, year):
        self.year = year

    def go_back(self, instance):
        self.manager.current = "years"

class LoadTeams(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = None
        self.week = None

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        main_layout.add_widget(Label(text="Select a Year", font_size=30, size_hint=(1, 0.1)))

        scroll = ScrollView()

        grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        teams = MainFile.teams()

        for team in teams:
            btn = Button(text=f"{team}", size_hint_y=None, height=60)
            btn.bind(on_press=self.load_team)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)
    def load_year(self, year):
        self.year = year

    def load_week(self, week):
        self.week = week

    def load_team(self, instance):
        team = instance.text

        stat_screen = self.manager.get_screen("predictor")
        stat_screen.load_team(team)

        self.manager.current = "predictor"

    def go_back(self, instance):
        self.manager_current = "years"

class PredictorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = None
        self.week = None
        self.team = None

    def load_year(self, year):
        self.year = year

    def load_week(self, week):
        self.week = week

    def load_team(self, team):
        self.team = team

    def go_back(self, instance):
        self.manager_current = "years"