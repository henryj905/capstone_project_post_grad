from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

import InLists
import MainFile
import playerStatsSeasonal

stats = ['passing', 'rushing', 'receiving', 'sacks', 'special']


class PlayerListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.compare_mode = False
        self.main_player = None
        self.main_team = None
        self.main_stat = None

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title_label = Label(text="Pick Player", font_size=30, size_hint=(1, 0.1))
        self.main_layout.add_widget(self.title_label)

        self.scroll = ScrollView()

        self.grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.scroll.add_widget(self.grid)
        self.main_layout.add_widget(self.scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        self.main_layout.add_widget(back_btn)

        self.add_widget(self.main_layout)

    def load_team(self, team_name, year, stat):
        self.team = team_name
        self.year = year
        self.stat = stat

        self.title_label.text = f"{team_name} {stat.capitalize()} Players ({year})"

        self.grid.clear_widgets()

        stat_dic = {
            'passing': InLists.player_in_passing_season,
            'rushing': InLists.player_in_rushing_season,
            'receiving': InLists.player_in_receiving_season,
            'sacks': InLists.player_in_sacks_season,
            'special': InLists.player_in_special_season
        }

        func = stat_dic.get(self.stat)

        if func:
            players = func(self.year, self.team)

            for player in players["player_name"]:
                btn = Button(text=player, size_hint_y=None, height=60)

                btn.bind(on_press=lambda instance, p=player: self.load_stat(p))

                self.grid.add_widget(btn)

    def load_stat(self, player):
        stat_screen = self.manager.get_screen('player_stats')

        if not self.compare_mode:
            # normal behavior
            stat_screen.set_main_player(player)
            stat_screen.set_stat(self.stat)
            stat_screen.set_team(self.team)
            stat_screen.set_year(self.year)
            stat_screen.display_single_player()
        else:
            # 🔥 COMPARISON MODE
            stat1, num1 = playerStatsSeasonal.return_stats(
                self.year, self.main_team, self.main_player, self.main_stat
            )

            stat2, num2 = playerStatsSeasonal.return_stats(
                self.year, self.team, player, self.stat
            )

            stat_screen.stats_grid.clear_widgets()
            stat_screen.stats_grid.cols = 4  # ✅ match your desired layout

            # headers
            stat_screen.stats_grid.add_widget(stat_screen.create_label(self.main_player, "center"))
            stat_screen.stats_grid.add_widget(stat_screen.create_label("", "center"))
            stat_screen.stats_grid.add_widget(stat_screen.create_label(player, "center"))
            stat_screen.stats_grid.add_widget(stat_screen.create_label("", "center"))

            for i in range(len(stat1)):
                # left player
                stat_screen.stats_grid.add_widget(stat_screen.create_label(stat1[i], "left"))
                stat_screen.stats_grid.add_widget(stat_screen.create_label(num1[i], "right"))

                # right player
                stat_screen.stats_grid.add_widget(stat_screen.create_label(stat2[i], "left"))
                stat_screen.stats_grid.add_widget(stat_screen.create_label(num2[i], "right"))

        self.manager.current = 'player_stats'

    def go_back(self, instance):
        self.manager.current = "statistics"

# class ScreenForNone:
class PlayerStatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_player = None
        self.main_team = None
        self.main_year = None
        self.main_stat = None

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text="Player Stats", font_size=30, size_hint=(1, 0.1))
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

    def set_main_player(self, player):
        self.player = player
        self.main_player = player

    def set_team(self, team):
        self.team = team
        self.main_team = team

    def set_year(self, year):
        self.year = year
        self.main_year = year

    def set_stat(self, stat):
        self.stat = stat
        self.main_stat = stat

    def display_single_player(self):
        try:
            stat, num = playerStatsSeasonal.return_stats(self.year, self.team, self.player, self.stat)
            self.stats_grid.clear_widgets()
            self.stats_grid.cols = 2
            self.stats_grid.add_widget(self.create_label(self.player, 'left'))
            self.stats_grid.add_widget(self.create_label(' ', 'left'))
            for s, n in zip(stat, num):
                self.stats_grid.add_widget(self.create_label(s, "left"))
                self.stats_grid.add_widget(self.create_label(n, "right"))

        except Exception as e:
            self.stats_grid.clear_widgets()
            self.stats_grid.add_widget(Label(text=f"Error: {e}"))

    def go_to_compare(self, instance):
        team_screen = self.manager.get_screen("second_team")

        team_screen.set_year(self.year)

        # pass first player info
        team_screen.main_player = self.player
        team_screen.main_team = self.team
        team_screen.main_stat = self.stat

        self.manager.current = "second_team"

    def go_back(self, instance):
        self.manager.current = "which_one"


class PlayerCompare(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_team = None
        self.year = None
        self.main_player = None
        self.stat = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title = Label(text="Select Player to Compare", font_size=30)
        layout.add_widget(self.title)

        scroll = ScrollView()
        self.grid = GridLayout(cols=2, size_hint_y=None, spacing=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        scroll.add_widget(self.grid)
        layout.add_widget(scroll)

        back_btn = Button(text="Back")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def gather(self, main_team, year, player, stat):
        self.main_team = main_team
        self.year = year
        self.main_player = player
        self.stat = stat

        self.load_players()

    def load_players(self):
        self.grid.clear_widgets()

        stat_dic = {
            'passing': InLists.player_in_passing_season,
            'rushing': InLists.player_in_rushing_season,
            'receiving': InLists.player_in_receiving_season,
            'sacks': InLists.player_in_sacks_season,
            'special': InLists.player_in_special_season
        }

        func = stat_dic.get(self.stat)

        if func:
            players = func(self.year, self.main_team)

            for player in players["player_name"]:
                if player != self.main_player:  # don't compare same player
                    btn = Button(text=player, size_hint_y=None, height=60)
                    btn.bind(on_press=lambda instance, p=player: self.compare(p))
                    self.grid.add_widget(btn)

    def compare(self, second_player):
        stat1, num1 = playerStatsSeasonal.return_stats(
            self.year, self.main_team, self.main_player, self.stat
        )

        stat2, num2 = playerStatsSeasonal.return_stats(
            self.year, self.main_team, second_player, self.stat
        )

        stats_screen = self.manager.get_screen('player_stats')

        stats_screen.stats_grid.clear_widgets()
        stats_screen.stats_grid.cols = 4

        # headers
        stats_screen.stats_grid.add_widget(Label(text=self.main_player))
        stats_screen.stats_grid.add_widget(Label(text=""))
        stats_screen.stats_grid.add_widget(Label(text=second_player))
        stats_screen.stats_grid.add_widget(Label(text=""))

        for i in range(len(stat1)):
            stats_screen.stats_grid.add_widget(Label(text=stat1[i]))
            stats_screen.stats_grid.add_widget(Label(text=str(num1[i])))
            stats_screen.stats_grid.add_widget(Label(text=stat2[i]))
            stats_screen.stats_grid.add_widget(Label(text=str(num2[i])))

        self.manager.current = 'player_stats'

    def go_back(self, instance):
        self.manager.current = "player_stats"


class TeamPickPlayer(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_year = None
        self.main_player = None
        self.main_team = None
        self.main_stat = None

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        main_layout.add_widget(Label(text="Select a Team", font_size=30, size_hint=(1, 0.1)))

        scroll = ScrollView()

        grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        teams = MainFile.teams()

        for team in teams:
            btn = Button(text=team, size_hint_y=None, height=60)
            btn.bind(on_press=self.second_team)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def set_year(self, year):
        self.selected_year = year

    def second_team(self, instance):
        compare_team = instance.text

        player_list = self.manager.get_screen("player_list")

        # load directly into player list with SAME stat
        player_list.load_team(compare_team, self.selected_year, self.main_stat)

        # enable compare mode
        player_list.compare_mode = True
        player_list.main_player = self.main_player
        player_list.main_team = self.main_team
        player_list.main_stat = self.main_stat

        self.manager.current = "player_list"

    def go_back(self, instance):
        self.manager.current = "player_compare"
    # def pick_next_player(self, instance):
    #