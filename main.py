import json
import os
import random
import webbrowser
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp

# KivMob को केवल एंड्रॉयड पर ही लोड करेंगे ताकि कंप्यूटर पर एरर न आए
if platform == 'android':
    try:
        from kivmob import KivMob
        KIVMOB_AVAILABLE = True
    except ImportError:
        KIVMOB_AVAILABLE = False
else:
    KIVMOB_AVAILABLE = False

# डेस्कटॉप विंडो साइज
if platform not in ('android', 'ios'):
    Window.size = (450, 750)

if platform == 'android':
    BASE_DIR = App().user_data_dir
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "quiznova_save.json")

# ⚠️ यहाँ अपनी असली ADMOB IDs डालें (जब आपके पास हों)
# अभी टेस्टिंग के लिए मैंने Google की "Test Interstitial ID" डाली है ताकि आपका ऐप तुरंत पैसे कमाने के लिए तैयार रहे
ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713" # Test App ID
INTERSTITIAL_AD_ID = "ca-app-pub-3940256099942544/1033173712" # Test Interstitial ID

USER_DATA = {
    "name": "",
    "scores": {str(i): {"best": 0, "last": 0} for i in range(1, 22)}
}

def load_game_data():
    global USER_DATA
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                if "name" in loaded_data and "scores" in loaded_data:
                    USER_DATA = loaded_data
        except Exception as e:
            print(f"Error loading data: {e}")

def save_game_data():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(USER_DATA, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")


class LogoScreen(Screen):
    def on_enter(self):
        load_game_data()
        Clock.schedule_once(self.go_to_profile, 3.5)

    def go_to_profile(self, dt):
        if USER_DATA["name"].strip() != "":
            self.manager.get_screen('menu').refresh_levels()
            self.manager.current = 'menu'
        else:
            self.manager.current = 'profile'


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        
        logo_path = os.path.join(SRC_DIR, "logo.png")
        if os.path.exists(logo_path):
            layout.add_widget(Image(source=logo_path, size_hint_y=0.3, fit_mode='contain'))
        else:
            layout.add_widget(Label(text="✨ QUIZNOVA ✨", font_size='36sp', bold=True, color=(0.1, 0.7, 1, 1), size_hint_y=0.25))
            
        layout.add_widget(Label(text="Enter Your Name to Register:", font_size='18sp', color=(0.9, 0.9, 0.9, 1), size_hint_y=0.1))
        
        self.name_input = TextInput(
            text="", 
            hint_text="Your Name Here...", 
            multiline=False, 
            font_size='18sp',
            size_hint_y=None,
            height=dp(50),
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        layout.add_widget(self.name_input)
        
        start_btn = Button(
            text="START QUIZ 🎮", 
            font_size='20sp', 
            bold=True, 
            background_color=(0.1, 0.6, 0.4, 1),
            background_normal='',
            size_hint_y=None,
            height=dp(60)
        )
        start_btn.bind(on_release=self.save_profile)
        layout.add_widget(start_btn)
        
        layout.add_widget(Label(size_hint_y=0.2)) 
        self.add_widget(layout)

    def save_profile(self, instance):
        if self.name_input.text.strip():
            USER_DATA["name"] = self.name_input.text.strip()
            save_game_data()
            self.manager.get_screen('menu').refresh_levels()
            self.manager.current = 'menu'


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.add_widget(self.main_layout)

    def refresh_levels(self):
        self.main_layout.clear_widgets()
        
        profile_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        name_lbl = Label(text=f"👤 {USER_DATA['name']}", font_size='18sp', bold=True, halign='left', size_hint_x=0.55)
        name_lbl.bind(size=name_lbl.setter('text_size')) 
        
        prize_btn = Button(text="🏆 Claim ₹2000", font_size='14sp', bold=True, size_hint_x=0.45, background_color=(1, 0.7, 0, 1), background_normal='')
        prize_btn.bind(on_release=self.check_prize_claim)
        
        profile_bar.add_widget(name_lbl)
        profile_bar.add_widget(prize_btn)
        self.main_layout.add_widget(profile_bar)
        
        scroll = ScrollView(size_hint_y=1.0)
        grid = GridLayout(cols=1, spacing=dp(12), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for i in range(1, 22):
            level_box = BoxLayout(orientation='horizontal', spacing=dp(15), size_hint_y=None, height=dp(80))
            
            btn = Button(
                text=f"Level {i}",
                font_size='18sp',
                bold=True,
                background_color=(0.15, 0.25, 0.4, 1),
                background_normal='',
                size_hint_x=0.45
            )
            btn.bind(on_release=self.make_callback(i))
            
            best_s = USER_DATA["scores"][str(i)]["best"]
            last_s = USER_DATA["scores"][str(i)]["last"]
            
            score_lbl = Label(
                text=f"Best: {best_s}/50\nLast: {last_s}/50",
                font_size='14sp',
                color=(0.8, 0.8, 0.8, 1),
                halign='center',
                valign='middle',
                size_hint_x=0.55
            )
            score_lbl.bind(size=score_lbl.setter('text_size'))
            
            level_box.add_widget(btn)
            level_box.add_widget(score_lbl)
            grid.add_widget(level_box)
            
        scroll.add_widget(grid)
        self.main_layout.add_widget(scroll)

    def make_callback(self, level_num):
        return lambda instance: self.select_level(level_num)

    def select_level(self, level_num):
        quiz_screen = self.manager.get_screen('quiz')
        if quiz_screen.load_level(level_num):
            self.manager.current = 'quiz'

    def check_prize_claim(self, instance):
        has_won_all = True
        total_score_achieved = 0
        
        for l in range(1, 22):
            level_best = USER_DATA["scores"][str(l)]["best"]
            total_score_achieved += level_best
            if level_best < 50:
                has_won_all = False
        
        if has_won_all and total_score_achieved == 1050:
            self.manager.current = 'certificate'
        else:
            lock_screen = self.manager.get_screen('certificate_lock')
            lock_screen.update_status(total_score_achieved)
            self.manager.current = 'certificate_lock'


class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(15))
        
        header_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        self.info_label = Label(text="", font_size='15sp', color=(1, 0.8, 0.2, 1), halign='left')
        self.timer_label = Label(text="⏳ 5s", font_size='15sp', bold=True, color=(1, 0.3, 0.3, 1), halign='right')
        header_box.add_widget(self.info_label)
        header_box.add_widget(self.timer_label)
        self.layout.add_widget(header_box)
        
        self.question_label = Label(text="", font_size='22sp', bold=True, halign='center', valign='middle', size_hint_y=0.3)
        self.question_label.bind(size=self.question_label.setter('text_size'))
        self.layout.add_widget(self.question_label)
        
        self.options_layout = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=0.5)
        self.layout.add_widget(self.options_layout)
        
        self.back_btn = Button(text="Quit Game", font_size='16sp', size_hint_y=None, height=dp(50), background_color=(0.8, 0.2, 0.2, 1), background_normal='')
        self.back_btn.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_btn)
        
        self.add_widget(self.layout)
        
        self.questions = []
        self.current_q_index = 0
        self.score = 0
        self.level_num = 1
        self.time_left = 5
        self.timer_event = None
        self.clickable = True  
        self.questions_answered_count = 0  

    def load_level(self, level_num):
        self.level_num = level_num
        self.options_layout.clear_widgets()
        
        file_path = os.path.join(SRC_DIR, "levels", f"level{level_num}.json")
        
        if not os.path.exists(file_path):
            self.question_label.text = f"⚠️ File Missing! Level JSON not found."
            return False
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.questions = json.load(f)
            if len(self.questions) > 50:
                self.questions = random.sample(self.questions, 50)
            self.current_q_index = 0
            self.score = 0
            self.questions_answered_count = 0  
            self.show_question()
            return True
        except Exception as e:
            print(f"Error loading level JSON: {e}")
            return False

    def show_question(self):
        self.stop_timer()
        self.options_layout.clear_widgets()
        self.clickable = True
        
        if self.current_q_index < len(self.questions):
            q_data = self.questions[self.current_q_index]
            self.info_label.text = f"🏅 Lvl {self.level_num} | Q: {self.current_q_index + 1}/50 | Score: {self.score}"
            self.question_label.text = q_data["question"]
            
            options = list(q_data["options"])
            random.shuffle(options)
            for opt in options:
                btn = Button(text=opt, font_size='18sp', background_color=(0.15, 0.4, 0.6, 1), background_normal='')
                btn.bind(on_release=self.check_answer)
                self.options_layout.add_widget(btn)
                
            self.time_left = 5
            self.timer_label.text = f"⏳ {self.time_left}s"
            self.timer_event = Clock.schedule_interval(self.update_timer, 1.0)
        else:
            lvl_str = str(self.level_num)
            USER_DATA["scores"][lvl_str]["last"] = self.score
            if self.score > USER_DATA["scores"][lvl_str]["best"]:
                USER_DATA["scores"][lvl_str]["best"] = self.score
            
            save_game_data()
            
            stars = "⭐"
            if self.score >= 45:
                stars = "⭐⭐⭐"
            elif self.score >= 30:
                stars = "⭐⭐"
                
            self.timer_label.text = ""
            self.info_label.text = "🎉 Level Completed!"
            self.question_label.text = f"🏆 MATCH OVER! 🏆\n\nYour Score: {self.score} / 50\nRating: {stars}"
            
            App.get_running_app().show_three_ads()
            
            home_btn = Button(text="Back to Levels Menu", font_size='18sp', background_color=(0.1, 0.5, 0.8, 1), background_normal='')
            home_btn.bind(on_release=self.go_back)
            self.options_layout.add_widget(home_btn)

    def stop_timer(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"⏳ {self.time_left}s"
        if self.time_left <= 0:
            self.stop_timer()
            self.clickable = False
            self.questions_answered_count += 1  
            Clock.schedule_once(self.next_question, 1.0)

    def check_answer(self, instance):
        if not self.clickable or self.current_q_index >= len(self.questions):
            return
        self.clickable = False
        self.stop_timer()
        
        correct_ans = self.questions[self.current_q_index]["answer"]
        for btn in self.options_layout.children:
            if hasattr(btn, 'text') and btn.text == correct_ans:
                btn.background_color = (0.2, 0.7, 0.3, 1)
            if btn == instance and instance.text != correct_ans:
                btn.background_color = (0.85, 0.25, 0.25, 1)
                
        if instance.text == correct_ans:
            self.score += 1
            
        self.questions_answered_count += 1  
        Clock.schedule_once(self.next_question, 1.0)

    def next_question(self, dt):
        self.current_q_index += 1
        
        if self.questions_answered_count % 3 == 0 and self.current_q_index < len(self.questions):
            App.get_running_app().show_three_ads()
            
        self.show_question()

    def go_back(self, instance):
        self.stop_timer()
        App.get_running_app().show_three_ads()
        self.manager.get_screen('menu').refresh_levels()
        self.manager.current = 'menu'


class CertificateLockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        self.status_lbl = Label(text="", font_size='18sp', halign='center', valign='middle', size_hint_y=0.8)
        self.status_lbl.bind(size=self.status_lbl.setter('text_size'))
        self.layout.add_widget(self.status_lbl)
        
        back_btn = Button(text="Go Back & Complete Levels", font_size='18sp', size_hint_y=0.2, background_color=(0.8, 0.3, 0.3, 1), background_normal='')
        back_btn.bind(on_release=self.go_home)
        self.layout.add_widget(back_btn)
        self.add_widget(self.layout)

    def update_status(self, current_total):
        questions_left = 1050 - current_total
        self.status_lbl.text = (
            f"🔒 CERTIFICATE LOCKED 🔒\n\n"
            f"Hey {USER_DATA['name']},\n"
            f"सर्टिफिकेट और ₹2,000 जीतने के लिए आपको सभी 21 लेवल्स में पूरे 50/50 सवाल सही करने होंगे!\n\n"
            f"🎯 आपका मौजूदा कुल स्कोर: {current_total} / 1050\n"
            f"⏳ आपको अभी {questions_left} और सही सवालों की आवश्यकता है।"
        )

    def go_home(self, instance):
        self.manager.current = 'menu'


class CertificateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(20))
        self.add_widget(self.layout)

    def on_enter(self):
        self.layout.clear_widgets()
        
        title = Label(text="🏆 GRAND WINNER CERTIFICATE 🏆", font_size='22sp', bold=True, color=(1, 0.8, 0.2, 1), size_hint_y=0.15)
        self.layout.add_widget(title)
        
        certi_text = (
            f"This certifies that\n\n"
            f"🏅 {USER_DATA['name']} 🏅\n\n"
            f"has successfully cleared all 21 levels of Quiznova,\n"
            f"mastering the database of 1,05,000 Questions!\n\n"
            f"🎉 PRIZE WON: ₹2,000 Cash 🎉"
        )
        
        content = Label(text=certi_text, font_size='18sp', halign='center', valign='middle', size_hint_y=0.5)
        content.bind(size=content.setter('text_size'))
        self.layout.add_widget(content)
        
        claim_btn = Button(text="📧 Send Screenshot & Claim Reward", font_size='16sp', size_hint_y=0.15, background_color=(0.1, 0.6, 0.3, 1), background_normal='')
        claim_btn.bind(on_release=self.claim_reward)
        self.layout.add_widget(claim_btn)
        
        back_btn = Button(text="Back to Game", font_size='16sp', size_hint_y=0.12, background_color=(0.2, 0.5, 0.8, 1), background_normal='')
        back_btn.bind(on_release=self.go_home)
        self.layout.add_widget(back_btn)

    def claim_reward(self, instance):
        email_id = "your_email@gmail.com"
        subject = f"Quiznova Winner Reward Claim - {USER_DATA['name']}"
        body = f"Hello, I have successfully completed all 21 levels of Quiznova with a perfect 50/50 score! My registered name is {USER_DATA['name']}. Please review my attached screenshot for the ₹2,000 prize."
        
        url = f"mailto:{email_id}?subject={subject.replace(' ', '%20')}&body={body.replace(' ', '%20')}"
        webbrowser.open(url)

    def go_home(self, instance):
        self.manager.current = 'menu'


class QuizNovaApp(App):
    def build(self):
        # एंड्रॉयड पर AdMob शुरू करना
        if KIVMOB_AVAILABLE:
            self.ads = KivMob(ADMOB_APP_ID)
            self.ads.new_interstitial(INTERSTITIAL_AD_ID)
            self.ads.request_interstitial()
        else:
            self.ads = None

        sm = ScreenManager()
        sm.add_widget(LogoScreen(name='logo'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(CertificateLockScreen(name='certificate_lock'))
        sm.add_widget(CertificateScreen(name='certificate'))
        return sm

    def show_three_ads(self):
        # 3 विज्ञापन दिखाने का लॉजिक (असली और नकली दोनों सपोर्ट के साथ)
        print("[ADS LOG]: --- AD BLOCK START ---")
        
        for i in range(1, 4):
            if self.ads and KIVMOB_AVAILABLE:
                # मोबाइल पर असली विज्ञापन दिखाना और नया विज्ञापन लोड करना
                if self.ads.is_interstitial_loaded():
                    self.ads.show_interstitial()
                    self.ads.request_interstitial() # अगले ऐड के लिए लोड करना
                    print(f"[ADS LOG]: Real Ad {i} Displayed on Mobile.")
                else:
                    self.ads.request_interstitial()
                    print(f"[ADS LOG]: Real Ad {i} requested (Not loaded yet).")
            else:
                # कंप्यूटर/डेस्कटॉप पर नकली (Mock) एड प्रिंट होगा ताकि एरर न आए
                print(f"[ADS LOG]: Ad {i} Triggered successfully (Desktop Sim mode).")
                
        print("[ADS LOG]: --- AD BLOCK END ---")


if __name__ == '__main__':
    QuizNovaApp().run()
