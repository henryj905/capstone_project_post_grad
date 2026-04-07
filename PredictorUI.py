from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import threading
import MainFile
import Algorithm


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

        main_layout.add_widget(Label(text="Select a Week", font_size=30, size_hint=(1, 0.1)))

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
        stat_screen.load_year(self.year)

        self.manager.current = "teams"

    def load_year(self, year):
        self.year = year

    def go_back(self, instance):
        self.manager.current = "predictor_main"


class LoadTeams(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = None
        self.week = None

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        main_layout.add_widget(Label(text="Select a Team", font_size=30, size_hint=(1, 0.1)))

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
        stat_screen.load_week(self.week)
        stat_screen.load_year(self.year)

        self.manager.current = "predictor"

    def go_back(self, instance):
        self.manager.current = "weeks"


class PredictorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.year = None
        self.week = None
        self.team = None
        self.spinner_event = None

        self.spinner_states = ["|", "/", "-", "\\"]
        self.spinner_index = 0

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.title_label = Label(
            text="Predictor",
            font_size=30,
            size_hint=(1, 0.2)
        )
        main_layout.add_widget(self.title_label)

        self.result_label = Label(
            text=".........",
            font_size=20,
            size_hint=(1, 0.2)
        )
        main_layout.add_widget(self.result_label)

        self.wait_label = Label(
            text="The later the week, the longer the wait",
            font_size=16,
            italic=True,
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(self.wait_label)

        self.spinner_label = Label(
            text="",
            font_size=40,
            size_hint=(1, 0.2)
        )
        main_layout.add_widget(self.spinner_label)

        back_btn = Button(text="Back", size_hint=(1, 0.2))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def load_year(self, year):
        self.year = year
        self.try_predict()

    def load_week(self, week):
        self.week = week
        self.try_predict()

    def load_team(self, team):
        self.team = team
        self.try_predict()

    def try_predict(self):
        if self.year is not None and self.week is not None and self.team is not None:
            self.display_winner()

    def display_winner(self):
        self.result_label.text = f"Loading {self.team}..."

        self.spinner_event = Clock.schedule_interval(self.animate_spinner, 0.1)

        threading.Thread(target=self._run_algorithm, daemon=True).start()

    def animate_spinner(self, dt):
        self.spinner_label.text = self.spinner_states[self.spinner_index]
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_states)

    def _run_algorithm(self):
        print("RUNNING ALGORITHM")
        df = Algorithm.run(self.year, self.week, self.team)
        print("ALGORITHM FINISHED")

        Clock.schedule_once(lambda dt: self.finish_loading(df))

    def finish_loading(self, df):
        # Stop spinner
        if self.spinner_event:
            self.spinner_event.cancel()

        self.spinner_label.text = ""

        self.update_result(df)

    def update_result(self, df):
        if df is None or df.empty:
            self.result_label.text = "No data available"
            return

        row = df.iloc[0]

        team = row["team"]
        team_score = row["team_score"]
        opponent = row["opponent"]
        opponent_score = row["opponent_score"]
        winner = row["predicted_winner"]

        if opponent is None:
            self.result_label.text = f"{team} has a BYE week"
        else:
            self.result_label.text = (
                f"{team} ({team_score}) vs {opponent} ({opponent_score})\n"
                f"Predicted Winner: {winner}"
            )

    def go_back(self, instance):
        self.manager.current = "teams"
