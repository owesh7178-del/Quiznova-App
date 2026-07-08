import json
import os
import random
import webbrowser  # ईमेल या लिंक खोलने के लिए
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
from kivmob import KivMob  # विज्ञापन के लिए KivMob

Window.size = (400, 650)

# सेव फाइल का नाम
SAVE_FILE = "quiznova_save.json"

# ग्लोबल डेटा डिक्शनरी
USER_DATA = {
    "name": "Guest",
    "scores": {str(i): {"best": 0, "last": 0} for i in range(1, 22)}
}

# 📁 डेटा लोड करने का फ़ंक्शन
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

# 📁 डेटा सेव करने का फ़ंक्शन
def save_game_data():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(USER_DATA, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")


class LogoScreen(Screen):
    def on_enter(self):
        load_game_data()
        Clock.schedule_once(self.go_to_profile, 2.5)

    def go_to_profile(self, dt):
        if USER_DATA["name"] != "Guest" and USER_DATA["name"].strip() != "":
            self.manager.get_screen('menu').refresh_levels()
            self.manager.current = 'menu'
        else:
            self.manager.current = 'profile'


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=25)
        
        if os.path.exists("logo.png"):
            layout.add_widget(Image(source="logo.png", size_hint_y=0.25, fit_mode='contain'))
        else:
            layout.add_widget(Label(text="✨ QUIZNOVA ✨", font_size='38sp', bold=True, color=(0.1, 0.7, 1, 1), size_hint_y=0.2))
            
        layout.add_widget(Label(text="Enter Your Name to Register:", font_size='18sp', color=(0.9, 0.9, 0.9, 1)))
        
        self.name_input = TextInput(
            text="", 
            hint_text="Your Name Here...", 
            multiline=False, 
            font_size='20sp',
            size_hint_y=0.08,
            padding=[10, 10, 10, 10]
        )
        layout.add_widget(self.name_input)
        
        start_btn = Button(
            text="START QUIZ 🎮", 
            font_size='22sp', 
            bold=True, 
            background_color=(0.1, 0.6, 0.4, 1),
            background_normal='',
            size_hint_y=0.12
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
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.add_widget(self.main_layout)

    def refresh_levels(self):
        self.main_layout.clear_widgets()
        
        profile_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        profile_bar.add_widget(Label(text=f"👤 {USER_DATA['name']}", font_size='18sp', bold=True, halign='left'))
        
        prize_btn = Button(text="🏆 Claim ₹2000", font_size='14sp', size_hint_x=0.4, background_color=(1, 0.7, 0, 1), background_normal='')
        prize_btn.bind(on_release=self.check_prize_claim)
        profile_bar.add_widget(prize_btn)
        self.main_layout.add_widget(profile_bar)
        
        scroll = ScrollView(size_hint_y=0.9)
        grid = GridLayout(cols=1, spacing=12, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for i in range(1, 22):
            level_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
            
            btn = Button(
                text=f"Level {i}",
                font_size='16sp',
                bold=True,
                background_color=(0.15, 0.25, 0.4, 1),
                background_normal='',
                size_hint_x=0.35
            )
            btn.bind(on_release=self.make_callback(i))
            
            best_s = USER_DATA["scores"][str(i)]["best"]
            last_s = USER_DATA["scores"][str(i)]["last"]
            score_lbl = Label(
                text=f"Best: {best_s}/20  |  Last: {last_s}/20",
                font_size='14sp',
                color=(0.8, 0.8, 0.8, 1),
                halign='center'
            )
            
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
            if level_best < 20:
                has_won_all = False
        
        if has_won_all and total_score_achieved == 420:
            self.manager.current = 'certificate'
        else:
            lock_screen = self.manager.get_screen('certificate_lock')
            lock_screen.update_status(total_score_achieved)
            self.manager.current = 'certificate_lock'


class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        header_box = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        self.info_label = Label(text="", font_size='16sp', color=(1, 0.8, 0.2, 1), halign='left')
        self.timer_label = Label(text="⏳ 15s", font_size='16sp', bold=True, color=(1, 0.3, 0.3, 1), halign='right')
        header_box.add_widget(self.info_label)
        header_box.add_widget(self.timer_label)
        self.layout.add_widget(header_box)
        
        self.question_label = Label(text="", font_size='24sp', bold=True, halign='center', valign='middle', size_hint_y=0.32)
        self.question_label.bind(size=self.question_label.setter('text_size'))
        self.layout.add_widget(self.question_label)
        
        self.options_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.5)
        self.layout.add_widget(self.options_layout)
        
        self.back_btn = Button(text="Quit Game", font_size='16sp', size_hint_y=0.1, background_color=(0.8, 0.2, 0.2, 1), background_normal='')
        self.back_btn.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_btn)
        
        self.add_widget(self.layout)
        
        self.questions = []
        self.current_q_index = 0
        self.score = 0
        self.level_num = 1
        self.time_left = 15
        self.timer_event = None
        self.clickable = True  
        self.questions_answered_count = 0  # 👈 हर 5 सवालों को गिनने के लिए काउंटर लगाया

    def load_level(self, level_num):
        self.level_num = level_num
        self.options_layout.clear_widgets()
        file_path = f"levels/level{level_num}.json"
        
        if not os.path.exists(file_path):
            self.question_label.text = "⚠️ File Missing! Run generator."
            return False
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.questions = json.load(f)
            if len(self.questions) > 20:
                self.questions = random.sample(self.questions, 20)
            self.current_q_index = 0
            self.score = 0
            self.questions_answered_count = 0  # लेवल शुरू होते ही काउंटर रीसेट
            self.show_question()
            return True
        except:
            return False

    def show_question(self):
        self.stop_timer()
        self.options_layout.clear_widgets()
        self.clickable = True
        
        if self.current_q_index < len(self.questions):
            q_data = self.questions[self.current_q_index]
            self.info_label.text = f"🏅 Lvl {self.level_num} | Q: {self.current_q_index + 1}/20 | Score: {self.score}"
            self.question_label.text = q_data["question"]
            
            options = list(q_data["options"])
            random.shuffle(options)
            for opt in options:
                btn = Button(text=opt, font_size='19sp', background_color=(0.15, 0.4, 0.6, 1), background_normal='')
                btn.bind(on_release=self.check_answer)
                self.options_layout.add_widget(btn)
                
            self.time_left = 15
            self.timer_label.text = f"⏳ {self.time_left}s"
            self.timer_event = Clock.schedule_interval(self.update_timer, 1.0)
        else:
            lvl_str = str(self.level_num)
            USER_DATA["scores"][lvl_str]["last"] = self.score
            if self.score > USER_DATA["scores"][lvl_str]["best"]:
                USER_DATA["scores"][lvl_str]["best"] = self.score
            
            save_game_data()
            
            stars = "⭐"
            if self.score >= 18:
                stars = "⭐⭐⭐"
            elif self.score >= 12:
                stars = "⭐⭐"
                
            self.timer_label.text = ""
            self.info_label.text = "🎉 Level Completed!"
            self.question_label.text = f"🏆 MATCH OVER! 🏆\n\nYour Score: {self.score} / 20\nRating: {stars}"
            
            # मैच खत्म होने पर भी विज्ञापन दिखाएं
            App.get_running_app().show_interstitial_ad()
            
            home_btn = Button(text="Back to Levels Menu", font_size='18sp', background_color=(0.1, 0.5, 0.8, 1), background_normal='')
            home_btn.bind(on_release=self.go_back)
            self.options_layout.add_widget(home_btn)

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"⏳ {self.time_left}s"
        if self.time_left <= 0:
            self.stop_timer()
            self.clickable = False
            self.questions_answered_count += 1  # टाइमर खत्म होने को भी जवाब माना जाएगा
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
            
        self.questions_answered_count += 1  # खिलाड़ी ने जवाब दिया, काउंटर बढ़ाएं
        Clock.schedule_once(self.next_question, 1.0)

    def next_question(self, dt):
        self.current_q_index += 1
        
        # 💰 मुख्य बदलाव: अगर 5 सवाल पूरे हो गए हैं (और अभी गेम खत्म नहीं हुआ है) तो विज्ञापन दिखाओ!
        if self.questions_answered_count % 5 == 0 and self.current_q_index < len(self.questions):
            App.get_running_app().show_interstitial_ad()
            
        self.show_question()

    def go_back(self, instance):
        self.stop_timer()
        App.get_running_app().show_interstitial_ad()
        self.manager.get_screen('menu').refresh_levels()
        self.manager.current = 'menu'


class CertificateLockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.status_lbl = Label(text="", font_size='18sp', halign='center', valign='middle', size_hint_y=0.8)
        self.status_lbl.bind(size=self.status_lbl.setter('text_size'))
        self.layout.add_widget(self.status_lbl)
        
        back_btn = Button(text="Go Back & Complete Levels", font_size='18sp', size_hint_y=0.2, background_color=(0.8, 0.3, 0.3, 1), background_normal='')
        back_btn.bind(on_release=self.go_home)
        self.layout.add_widget(back_btn)
        self.add_widget(self.layout)

    def update_status(self, current_total):
        questions_left = 420 - current_total
        self.status_lbl.text = (
            f"🔒 CERTIFICATE LOCKED 🔒\n\n"
            f"Hey {USER_DATA['name']},\n"
            f"सर्टिफिकेट और ₹2,000 जीतने के लिए आपको सभी 21 लेवल्स में पूरे 20/20 सवाल सही करने होंगे!\n\n"
            f"🎯 आपका मौजूदा कुल स्कोर: {current_total} / 420\n"
            f"⏳ आपको अभी {questions_left} और सही सवालों की आवश्यकता है।"
        )

    def go_home(self, instance):
        self.manager.current = 'menu'


class CertificateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.add_widget(self.layout)

    def on_enter(self):
        self.layout.clear_widgets()
        
        title = Label(text="🏆 GRAND WINNER CERTIFICATE 🏆", font_size='24sp', bold=True, color=(1, 0.8, 0.2, 1), size_hint_y=0.15)
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
        body = f"Hello, I have successfully completed all 21 levels of Quiznova with a perfect 20/20 score! My registered name is {USER_DATA['name']}. Please review my attached screenshot for the ₹2,000 prize."
        
        url = f"mailto:{email_id}?subject={subject.replace(' ', '%20')}&body={body.replace(' ', '%20')}"
        webbrowser.open(url)

    def go_home(self, instance):
        self.manager.current = 'menu'


class QuizNovaApp(App):
    def build(self):
        self.ads = None
        try:
            self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")  # Test App ID
            self.ads.new_interstitial("ca-app-pub-3940256099942544/1033173712")  # Test Interstitial ID
            self.ads.request_interstitial()
        except Exception as e:
            print(f"Ads initialization failed: {e}")

        sm = ScreenManager()
        sm.add_widget(LogoScreen(name='logo'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(CertificateLockScreen(name='certificate_lock'))
        sm.add_widget(CertificateScreen(name='certificate'))
        return sm

    def show_interstitial_ad(self):
        try:
            if self.ads and self.ads.is_interstitial_loaded():
                self.ads.show_interstitial()
                self.ads.request_interstitial()  # अगला विज्ञापन पहले से लोड करके रखें
        except Exception as e:
            print(f"Failed to show ad: {e}")


if __name__ == '__main__':
    QuizNovaApp().run()
