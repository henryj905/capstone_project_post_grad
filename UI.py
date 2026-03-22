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
        print(f"Selected: {team_name}")

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


# ------------------ APP ------------------
class MyApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(StatsScreen(name="stats"))
        sm.add_widget(PredictorScreen(name="predictor"))

        return sm


if __name__ == "__main__":
    MyApp().run()