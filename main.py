import os
import sys

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.textinput import TextInput

# ==========================================
# 1. ADMOB CONFIGURATION
# ==========================================
ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"
BANNER_AD_ID = "ca-app-pub-3940256099942544/6300978111"
INTERSTITIAL_AD_ID = "ca-app-pub-3940256099942544/1033173712"

try:
  from kivmob import KivMob

  KIVMOB_AVAILABLE = True
except ImportError:
  KIVMOB_AVAILABLE = False


def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)


# ==========================================
# 2. SPLASH SCREEN
# ==========================================
class SplashScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(20))

    logo_path = resource_path("logo.png")
    if os.path.exists(logo_path):
      self.logo = Image(
          source=logo_path,
          allow_stretch=True,
          keep_ratio=True,
          size_hint_y=0.7,
      )
      layout.add_widget(self.logo)
    else:
      self.title_label = Label(
          text="🧠 QuizNova 🧠",
          font_size="36sp",
          bold=True,
          color=(0.2, 0.6, 1, 1),
          size_hint_y=0.7,
      )
      layout.add_widget(self.title_label)

    self.loading_label = Label(
        text="Loading... Please Wait", font_size="16sp", size_hint_y=0.3
    )
    layout.add_widget(self.loading_label)
    self.add_widget(layout)

  def on_enter(self):
    Clock.schedule_once(self.go_to_login, 2)

  def go_to_login(self, dt):
    self.manager.current = "login"


# ==========================================
# 3. LOGIN SCREEN
# ==========================================
class LoginScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    layout = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(15))

    title = Label(
        text="WELCOME TO QUIZNOVA",
        font_size="24sp",
        bold=True,
        size_hint_y=0.2,
        color=(0.2, 0.7, 0.9, 1),
    )
    layout.add_widget(title)

    self.username_input = TextInput(
        hint_text="Enter Username",
        multiline=False,
        font_size="16sp",
        size_hint_y=0.15,
        padding=[dp(10), dp(10)],
    )
    layout.add_widget(self.username_input)

    start_btn = Button(
        text="CONTINUE TO LEVELS 🚀",
        font_size="18sp",
        bold=True,
        background_color=(0.1, 0.7, 0.3, 1),
        background_normal="",
        size_hint_y=0.15,
    )
    start_btn.bind(on_release=self.go_to_levels)
    layout.add_widget(start_btn)

    layout.add_widget(Label(size_hint_y=0.5))
    self.add_widget(layout)

  def go_to_levels(self, instance):
    username = self.username_input.text.strip() or "Player"
    app = App.get_running_app()
    app.username = username
    self.manager.current = "levels"


# ==========================================
# 4. LEVELS SCREEN (21 Levels)
# ==========================================
class LevelsScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    layout = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10))

    header = Label(
        text="SELECT LEVEL (1 - 21)",
        font_size="22sp",
        bold=True,
        size_hint_y=0.1,
        color=(0.2, 0.7, 0.9, 1),
    )
    layout.add_widget(header)

    scroll = ScrollView(size_hint=(1, 0.9))
    grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
    grid.bind(minimum_height=grid.setter("height"))

    for i in range(1, 22):
      btn = Button(
          text=f"Level {i}\n(500 Questions)",
          font_size="16sp",
          bold=True,
          background_color=(0.2, 0.5, 0.8, 1),
          background_normal="",
          size_hint_y=None,
          height=dp(70),
      )
      btn.level_num = i
      btn.bind(on_release=self.select_level)
      grid.add_widget(btn)

    scroll.add_widget(grid)
    layout.add_widget(scroll)
    self.add_widget(layout)

  def select_level(self, instance):
    quiz_screen = self.manager.get_screen("quiz")
    quiz_screen.start_level(instance.level_num)
    self.manager.current = "quiz"


# ==========================================
# 5. QUIZ SCREEN (5s TIMER + RIGHT/WRONG FEEDBACK)
# ==========================================
class QuizScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.score = 0
    self.current_q_index = 0
    self.level_num = 1
    self.questions = []
    self.time_left = 5
    self.timer_event = None

    layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15))

    self.info_label = Label(
        text="Score: 0", font_size="16sp", bold=True, size_hint_y=0.08
    )
    layout.add_widget(self.info_label)

    # 5 Sec Timer Header
    self.timer_label = Label(
        text="⏱️ Time Left: 5s",
        font_size="18sp",
        bold=True,
        color=(1, 0.3, 0.3, 1),
        size_hint_y=0.08,
    )
    layout.add_widget(self.timer_label)

    self.question_label = Label(
        text="Question Here",
        font_size="22sp",
        bold=True,
        halign="center",
        valign="middle",
        size_hint_y=0.3,
    )
    self.question_label.bind(size=self.question_label.setter("text_size"))
    layout.add_widget(self.question_label)

    self.option_buttons = []
    for i in range(4):
      btn = Button(
          text=f"Option {i+1}",
          font_size="16sp",
          background_color=(0.2, 0.5, 0.8, 1),
          background_normal="",
          size_hint_y=0.12,
      )
      btn.bind(on_release=self.check_answer)
      self.option_buttons.append(btn)
      layout.add_widget(btn)

    self.add_widget(layout)

  def start_level(self, level_num):
    self.level_num = level_num
    self.current_q_index = 0
    self.score = 0
    self.generate_500_level_questions()
    self.load_question()

  def generate_500_level_questions(self):
    base_questions = [
        {
            "q": "Python kya hai?",
            "options": ["Programming Language", "Snake", "Car", "Movie"],
            "ans": "Programming Language",
        },
        {
            "q": "Kivy ka upyog kiske liye hota hai?",
            "options": ["GUI App", "Database", "Operating System", "Hardware"],
            "ans": "GUI App",
        },
        {
            "q": "AdMob kya hai?",
            "options": [
                "Google Ad Network",
                "Social Media",
                "Search Engine",
                "Game Engine",
            ],
            "ans": "Google Ad Network",
        },
        {
            "q": "HTML ka full form kya hai?",
            "options": [
                "HyperText Markup Language",
                "HighText Machine Language",
                "Hyper Text Main Link",
                "None",
            ],
            "ans": "HyperText Markup Language",
        },
        {
            "q": "APK kiska installer hai?",
            "options": ["Android", "Windows", "iOS", "Linux"],
            "ans": "Android",
        },
    ]

    self.questions = []
    for i in range(1, 501):
      base = base_questions[(i - 1) % len(base_questions)]
      self.questions.append({
          "q": f"[{i}/500] {base['q']}",
          "options": base["options"],
          "ans": base["ans"],
      })

  def load_question(self):
    if self.timer_event:
      self.timer_event.cancel()

    # Har 3 questions par Full-Screen Ad
    if self.current_q_index > 0 and self.current_q_index % 3 == 0:
      app = App.get_running_app()
      app.show_interstitial_ad()

    if self.current_q_index < len(self.questions):
      q_data = self.questions[self.current_q_index]
      app = App.get_running_app()

      self.question_label.text = q_data["q"]
      self.info_label.text = (
          f"Lvl: {self.level_num} | Player: {app.username} | Q:"
          f" {self.current_q_index + 1}/500 | Score: {self.score}"
      )

      # Option Buttons Default Color (Blue) aur Active State Reset
      for i, option in enumerate(q_data["options"]):
        self.option_buttons[i].text = option
        self.option_buttons[i].background_color = (0.2, 0.5, 0.8, 1)
        self.option_buttons[i].disabled = False

      # 5 Second Timer Reset & Start
      self.time_left = 5
      self.timer_label.text = f"⏱️ Time Left: {self.time_left}s"
      self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    else:
      self.timer_label.text = "⏱️ Time Left: 0s"
      self.question_label.text = (
          f"🎉 Level {self.level_num} Complete!\nFinal Score: {self.score}"
      )
      for btn in self.option_buttons:
        btn.disabled = True

  def update_timer(self, dt):
    self.time_left -= 1
    self.timer_label.text = f"⏱️ Time Left: {self.time_left}s"

    # Time Over -> Correct Option Dikhakar Agla Question Lana
    if self.time_left <= 0:
      self.timer_event.cancel()
      self.highlight_correct_answer()
      Clock.schedule_once(self.next_question, 1)

  def check_answer(self, instance):
    if self.timer_event:
      self.timer_event.cancel()

    # Disable buttons temporarily during color feedback
    for btn in self.option_buttons:
      btn.disabled = True

    correct_ans = self.questions[self.current_q_index]["ans"]

    if instance.text == correct_ans:
      # Sahi Jawab -> Green Color
      instance.background_color = (0, 0.8, 0.2, 1)
      self.score += 10
    else:
      # Galat Jawab -> Red Color & Right Answer Green
      instance.background_color = (0.9, 0.1, 0.1, 1)
      self.highlight_correct_answer()

    # 1 Sec Delay to show feedback then load next
    Clock.schedule_once(self.next_question, 1)

  def highlight_correct_answer(self):
    correct_ans = self.questions[self.current_q_index]["ans"]
    for btn in self.option_buttons:
      if btn.text == correct_ans:
        btn.background_color = (0, 0.8, 0.2, 1)

  def next_question(self, dt):
    self.current_q_index += 1
    self.load_question()


# ==========================================
# 6. MAIN APP CLASS
# ==========================================
class QuizNovaApp(App):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.username = "Player"

  def build(self):
    self.title = "QuizNova"

    if KIVMOB_AVAILABLE:
      self.ads = KivMob(ADMOB_APP_ID)
      self.ads.new_banner(BANNER_AD_ID, top_pos=False)
      self.ads.new_interstitial(INTERSTITIAL_AD_ID)
      self.ads.request_banner()
      self.ads.request_interstitial()
      self.ads.show_banner()

    sm = ScreenManager(transition=FadeTransition())
    sm.add_widget(SplashScreen(name="splash"))
    sm.add_widget(LoginScreen(name="login"))
    sm.add_widget(LevelsScreen(name="levels"))
    sm.add_widget(QuizScreen(name="quiz"))
    return sm

  def show_interstitial_ad(self):
    if KIVMOB_AVAILABLE:
      if self.ads.is_interstitial_loaded():
        self.ads.show_interstitial()
        self.ads.request_interstitial()


if __name__ == "__main__":
  QuizNovaApp().run()
