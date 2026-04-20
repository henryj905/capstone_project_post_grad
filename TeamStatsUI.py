from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import MainFile
import OffensivePerTeam


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
            logo_path = f"Logos/{team}.jpg"

            btn = TeamButtonTeamStats(
                team=team,
                image_path=logo_path,
                callback=self.selected,
                size_hint_y=None,
                height=90
            )

            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def selected(self, instance):
        stat_type = self.manager.get_screen("stat_type")
        stat_type.load_selects(instance, self.selected_year)

        self.manager.current = "stat_type"

    def load_year(self, year):
        self.selected_year = year

    def go_back(self, instance):
        self.manager.current = "years"


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
        player_btn.bind(on_press=self.go_to_which_stat)
        layout.add_widget(player_btn)

        back_btn = Button(text="Back")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def load_selects(self, team_name, year):
        self.selected_team = team_name
        self.selected_year = year
        self.title.text = f"{team_name} ({year})"

    def go_to_team_stats(self, instance):
        screen = self.manager.get_screen("team_stats")

        screen.year = self.selected_year
        screen.load_team(self.selected_team)
        self.manager.current = "team_stats"

    def go_to_which_stat(self, instance):
        screen = self.manager.get_screen("which_one")

        screen.year = self.selected_year
        screen.load_team(self.selected_team, self.selected_year)
        self.manager.current = "which_one"

    def go_back(self, instance):
        self.manager.current = "statistics"


class TeamStatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.team_name = None
        self.year = None
        self.compare_team = None

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text="Team Stats", font_size=30, size_hint=(1, 0.1))
        self.layout.add_widget(self.label)

        scroll = ScrollView()
        self.stats_grid = GridLayout(
            cols=2,
            spacing=5,
            size_hint_y=None
        )
        self.stats_grid.bind(minimum_height=self.stats_grid.setter('height'))
        scroll.add_widget(self.stats_grid)
        self.layout.add_widget(scroll)

        btn_row = BoxLayout(size_hint=(1, 0.1), spacing=10)
        back_btn = Button(text="Back")
        back_btn.bind(on_press=self.go_back)
        compare_btn = Button(text="Compare")
        compare_btn.bind(on_press=self.go_to_compare)
        btn_row.add_widget(back_btn)
        btn_row.add_widget(compare_btn)
        self.layout.add_widget(btn_row)

        self.add_widget(self.layout)

    def create_label(self, text, align):
        lbl = Label(
            text=str(text),
            halign=align,
            size_hint=(None, None)
        )
        lbl.bind(texture_size=lbl.setter('size'))
        return lbl

    def load_team(self, team_name):
        self.team_name = team_name
        self.compare_team = None
        self.label.text = f"{team_name} Stats"
        self.display_single_team()

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

    def display_comparison(self):
        try:
            stat1, num1 = OffensivePerTeam.team_season(self.team_name, self.year)
            stat2, num2 = OffensivePerTeam.team_season(self.compare_team, self.year)

            self.stats_grid.clear_widgets()
            self.stats_grid.cols = 4

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

    def go_to_compare(self, instance):
        compare_screen = self.manager.get_screen("compare_teams")
        compare_screen.set_main_team(self.team_name)
        compare_screen.year = self.year
        self.manager.current = "compare_teams"

    def go_back(self, instance):
        self.manager.current = "statistics"


class CompareScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_team = None
        self.year = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Select Team to Compare", font_size=30))

        scroll = ScrollView()
        grid = GridLayout(cols=4, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        teams = MainFile.teams()
        for team in teams:
            logo_path = f"Logos/{team}.jpg"

            btn = TeamButtonTeamStats(
                team=team,
                image_path=logo_path,
                callback=self.select_team,
                size_hint_y=None,
                height=90
            )

            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def set_main_team(self, team):
        self.main_team = team

    def select_team(self, instance):
        compare_team = instance
        stats_screen = self.manager.get_screen("team_stats")

        stats_screen.team_name = self.main_team
        stats_screen.compare_team = compare_team
        stats_screen.year = self.year

        stats_screen.display_comparison()

        self.manager.current = "team_stats"


class TeamButtonTeamStats(ButtonBehavior, BoxLayout):
    def __init__(self, team, image_path, callback, **kwargs):
        super().__init__(**kwargs)

        self.team = team
        self.callback = callback

        img = Image(
            source=image_path,
            keep_ratio=True,
            allow_stretch=True
        )

        self.add_widget(img)

    def on_press(self):
        self.callback(self.team)
