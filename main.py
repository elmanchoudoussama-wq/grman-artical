from kivy.utils import platform
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path, resource_find
import json
import random
import os
import time

# --- 1. IMPORT KIVMOB ---
try:
    from kivmob import KivMob, TestIds
    HAS_KIVMOB = True
except ImportError:
    HAS_KIVMOB = False

# --- 2. ARABIC SUPPORT (FIXED) ---
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_ARABIC_LIBS = True
except ImportError:
    HAS_ARABIC_LIBS = False

def fix_arabic(text):
    if not text or not HAS_ARABIC_LIBS:
        return text
    try:
        # Reshape connects the letters, get_display fixes the direction
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    except Exception as e:
        print(f"Arabic Error: {e}")
        return text

# --- AD SETTINGS ---
class AdSettings:
    def __init__(self):
        self.AD_FILE = 'ad_data.json'
        self.default_ad_data = {'last_24h_ad': 0, 'question_count': 0}
        self.load_ad_data()
    
    def load_ad_data(self):
        if os.path.exists(self.AD_FILE):
            try:
                with open(self.AD_FILE, 'r') as f:
                    self.data = json.load(f)
            except: self.data = self.default_ad_data.copy()
        else: self.data = self.default_ad_data.copy()
    
    def save_ad_data(self):
        with open(self.AD_FILE, 'w') as f: json.dump(self.data, f)
    
    def check_24h_ad_required(self):
        return (time.time() - self.data.get('last_24h_ad', 0)) >= 900 
    
    def update_24h_ad_watched(self):
        self.data['last_24h_ad'] = time.time()
        self.save_ad_data()
    
    def increment_question_count(self):
        self.data['question_count'] = self.data.get('question_count', 0) + 1
        self.save_ad_data()
    
    def check_stage_quit_ad(self):
        return self.data.get('question_count', 0) >= 1
    
    def reset_question_count(self):
        self.data['question_count'] = 0
        self.save_ad_data()

class MockAdDialog(ModalView):
    def __init__(self, title, message, on_complete, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False
        self.on_complete = on_complete
        card = MDBoxLayout(orientation='vertical', padding="20dp", spacing="10dp")
        card.md_bg_color = (1, 1, 1, 1)
        card.add_widget(MDLabel(text=title, halign='center', font_style='H6'))
        card.add_widget(MDLabel(text=message, halign='center'))
        btn = MDFillRoundFlatButton(text="SIMULATE WATCH AD (PC ONLY)", pos_hint={'center_x': 0.5})
        btn.bind(on_release=self.finish)
        card.add_widget(btn)
        self.add_widget(card)

    def finish(self, *args):
        self.dismiss()
        if self.on_complete: self.on_complete()

# --- KV LAYOUT (FIXED SYNTAX) ---
KV_STRING = '''
ScreenManager:
    StageSelectScreen:
        name: 'stage_select'
    MainScreen:
        name: 'main'
    ResultScreen:
        name: 'result'

<StageSelectScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.95, 0.95, 1
        MDTopAppBar:
            title: app.arabic_title
            font_name: "Amiri"
        MDScrollView:
            MDBoxLayout:
                id: stage_grid
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "15dp"
        BoxLayout:
            size_hint_y: None
            height: "50dp"
            MDLabel:
                text: "Ad Space"
                halign: "center"
                theme_text_color: "Hint"

<MainScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1
        MDTopAppBar:
            title: app.question_number
            left_action_items: [["arrow-left", lambda x: app.handle_stage_quit()]]
            elevation: 2
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "20dp"
                MDLabel:
                    text: app.sentence
                    halign: "center"
                    font_style: "H5"
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                MDGridLayout:
                    cols: 3
                    spacing: "10dp"
                    size_hint_y: None
                    height: "60dp"
                    MDFillRoundFlatButton:
                        id: article_btn1
                        text: app.article_options[0]
                        size_hint_x: 1
                        on_release: app.select_article(self.text)
                    MDFillRoundFlatButton:
                        id: article_btn2
                        text: app.article_options[1]
                        size_hint_x: 1
                        on_release: app.select_article(self.text)
                    MDFillRoundFlatButton:
                        id: article_btn3
                        text: app.article_options[2]
                        size_hint_x: 1
                        on_release: app.select_article(self.text)
                MDLabel:
                    text: "Bedeutung:"
                    halign: "center"
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: "30dp"
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "10dp"
                    adaptive_height: True
                    MDFillRoundFlatButton:
                        id: meaning_btn1
                        text: app.meaning_options[0]
                        font_name: "Amiri"
                        size_hint_x: 1
                        on_release: app.select_meaning(self.text)
                    MDFillRoundFlatButton:
                        id: meaning_btn2
                        text: app.meaning_options[1]
                        font_name: "Amiri"
                        size_hint_x: 1
                        on_release: app.select_meaning(self.text)
                    MDFillRoundFlatButton:
                        id: meaning_btn3
                        text: app.meaning_options[2]
                        font_name: "Amiri"
                        size_hint_x: 1
                        on_release: app.select_meaning(self.text)
                MDFillRoundFlatButton:
                    text: "PRÜFEN"
                    size_hint_x: 1
                    disabled: not app.submit_enabled
                    md_bg_color: (0, 0.7, 0, 1) if self.disabled == False else (0.8, 0.8, 0.8, 1)
                    on_release: app.check_answer()
                MDLabel:
                    text: app.result_text
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0, 0.6, 0, 1
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
        BoxLayout:
            size_hint_y: None
            height: "50dp"

<ResultScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "30dp"
        spacing: "20dp"
        md_bg_color: 1, 0.95, 0.95, 1
        MDLabel:
            text: "Erklärung"
            halign: "center"
            font_style: "H4"
        MDLabel:
            text: app.explanation_text
            halign: "center"
            font_style: "Body1"
            font_name: "Amiri"
        MDFillRoundFlatButton:
            text: "Weiter"
            pos_hint: {"center_x": 0.5}
            on_release: app.next_question()
'''

class StageSelectScreen(Screen): pass
class MainScreen(Screen): pass
class ResultScreen(Screen): pass

class GermanArticleTrainer(MDApp):
    sentence = StringProperty("")
    question_number = StringProperty("Frage #1")
    article_options = ListProperty(["", "", ""])
    meaning_options = ListProperty(["", "", ""])
    submit_enabled = BooleanProperty(False)
    result_text = StringProperty("")
    explanation_text = StringProperty("")
    arabic_title = StringProperty("")
    current_stage = NumericProperty(1)
    unlocked_stages = NumericProperty(1)
    QUESTIONS_PER_STAGE = 100
    
    # --- AD CONFIGURATION (FIXED) ---
    APP_ID = "ca-app-pub-9298331856947532~1106493604"
    BANNER_ID = "ca-app-pub-3940256099942544/6300978111"
    INTERSTITIAL_ID = "ca-app-pub-3940256099942544/1033173712"

    def build(self):
        # 1. Tell Kivy where to look for fonts and images
        if os.path.exists('assets/fonts'):
            resource_add_path(os.path.abspath('assets/fonts'))
        
        # 2. Register the font correctly
        # We look for the filename only because resource_add_path handles the folder
        font_path = resource_find('Amiri-Regular.ttf')
        
        if font_path:
            LabelBase.register(name='Amiri', fn_regular=font_path)
            print(f"Font registered successfully from: {font_path}")
        else:
            print("ERROR: Could not find Amiri-Regular.ttf in assets/fonts/")

        self.arabic_title = fix_arabic("Artical lernen")
        self.theme_cls.primary_palette = "Blue"
        self.ad_settings = AdSettings()

        # Initialize Ads (KivMob)
        self.ads = None
        if platform == 'android' and HAS_KIVMOB:
            try:
                self.ads = KivMob(self.APP_ID)
                self.ads.new_banner(self.BANNER_ID, top_pos=False)
                self.ads.request_banner()
                self.ads.new_interstitial(self.INTERSTITIAL_ID)
                self.ads.request_interstitial()
            except Exception as e: 
                print(f"KivMob Error: {e}")
        
        return Builder.load_string(KV_STRING)

    def on_start(self):
        self.load_progress()
        self.ensure_data_exists()
        self.build_stage_menu()
        if self.ads: self.ads.show_banner()
        Clock.schedule_once(self.check_24h_ad, 1)

    def show_interstitial_ad(self, on_close_callback=None):
        if self.ads:
            if self.ads.is_interstitial_loaded():
                self.ads.show_interstitial()
                self.ads.request_interstitial()
            if on_close_callback: on_close_callback()
        else:
            MockAdDialog(title="Ad", message="Full screen ad.", on_complete=on_close_callback).open()

    def load_progress(self):
        if os.path.exists('progress.json'):
            try:
                with open('progress.json', 'r') as f:
                    self.unlocked_stages = json.load(f).get('unlocked', 1)
            except: self.unlocked_stages = 1

    def save_progress(self):
        with open('progress.json', 'w') as f:
            json.dump({'unlocked': self.unlocked_stages}, f)

    def build_stage_menu(self):
        screen = self.root.get_screen('stage_select')
        grid = screen.ids.stage_grid
        grid.clear_widgets()
        self.button_grid = MDGridLayout(adaptive_height=True, spacing="10dp")
        grid.add_widget(self.button_grid)

        for i in range(1, 101):
            is_locked = i > self.unlocked_stages
            btn = MDFillRoundFlatButton(
                text=f"Stage {i}" if not is_locked else f"{i} Locked",
                size_hint=(1, None),
                disabled=is_locked,
                on_release=lambda x, s=i: self.load_stage(s)
            )
            self.button_grid.add_widget(btn)
        self.update_grid_cols()
        Window.bind(on_resize=self.update_grid_cols)

    def update_grid_cols(self, *args):
        new_cols = max(2, int(Window.width / dp(110)))
        if hasattr(self, 'button_grid'): self.button_grid.cols = new_cols

    def load_stage(self, stage_number):
        self.current_stage = stage_number
        try:
            path = f'data/stages/stage_{stage_number}.json'
            with open(path, 'r', encoding='utf-8') as f:
                self.nouns = json.load(f)
            self.unused_nouns = list(self.nouns)
            random.shuffle(self.unused_nouns)
            self.question_count = 1
            self.correct_count = 0
            self.ad_settings.increment_question_count()
            self.generate_question()
            self.root.current = 'main'
        except: print("Stage File Missing")

    def generate_question(self):
        if not self.unused_nouns:
            self.unused_nouns = list(self.nouns)
            random.shuffle(self.unused_nouns)
        
        noun_data = self.unused_nouns.pop()
        cases = {'Nominativ': {'der':'der','die':'die','das':'das'},
                 'Akkusativ': {'der':'den','die':'die','das':'das'},
                 'Dativ': {'der':'dem','die':'der','das':'dem'}}
        
        case = random.choice(['Nominativ', 'Akkusativ', 'Dativ'])
        self.correct_art = cases[case][noun_data['article']]
        self.correct_mean = fix_arabic(noun_data['meaning'])

        # Options
        all_art = ['der', 'die', 'das', 'den', 'dem']
        self.article_options = random.sample(all_art, 3)
        if self.correct_art not in self.article_options: self.article_options[0] = self.correct_art
        random.shuffle(self.article_options)

        other_m = [fix_arabic(n['meaning']) for n in self.nouns if n['meaning'] != noun_data['meaning']]
        self.meaning_options = [self.correct_mean] + random.sample(other_m, 2) if len(other_m) >= 2 else [self.correct_mean, "X", "Y"]
        random.shuffle(self.meaning_options)

        self.current_question = noun_data
        self.sentence = noun_data['sentences'].get(case, "")
        self.question_number = f"Stufe {self.current_stage} - {self.question_count}/{self.QUESTIONS_PER_STAGE}"
        self.submit_enabled = False
        self.result_text = ""
        self.reset_button_colors()

    def select_article(self, t):
        self.selected_art = t
        self.update_colors('article_btn', t)
        self.submit_enabled = hasattr(self, 'selected_art') and hasattr(self, 'selected_mean')

    def select_meaning(self, t):
        self.selected_mean = t
        self.update_colors('meaning_btn', t)
        self.submit_enabled = hasattr(self, 'selected_art') and hasattr(self, 'selected_mean')

    def check_answer(self):
        is_correct = (self.selected_art == self.correct_art and self.selected_mean == self.correct_mean)
        if is_correct:
            self.result_text = "✅ Richtig!"
            self.correct_count += 1
            Clock.schedule_once(lambda dt: self.next_question(), 1.0)
        else:
            self.result_text = "❌ Falsch"
            self.explanation_text = fix_arabic(f"Wort: {self.current_question['word']}\nBedeutung: {self.current_question['meaning']}\nRichtig: {self.correct_art}")
            Clock.schedule_once(lambda dt: setattr(self.root, 'current', 'result'), 1.0)

    def next_question(self):
        if self.question_count >= self.QUESTIONS_PER_STAGE:
            self.finish_stage()
        else:
            self.question_count += 1
            self.generate_question()
            self.root.current = 'main'

    def finish_stage(self):
        score = (self.correct_count / self.QUESTIONS_PER_STAGE) * 100
        if score >= 95:
            if self.current_stage == self.unlocked_stages:
                self.unlocked_stages += 1
                self.save_progress()
            msg = "Bestanden! 🎉"
        else: msg = "Nicht genug Punkte (95% benötigt)"
        
        MDDialog(title="Ergebnis", text=msg, buttons=[MDFlatButton(text="OK", on_release=lambda x: self.go_back_to_menu())]).open()
        self.show_interstitial_ad()

    def go_back_to_menu(self, *args):
        self.root.current = 'stage_select'
        self.build_stage_menu()

    def handle_stage_quit(self):
        self.show_interstitial_ad(on_close_callback=self.go_back_to_menu)

    def reset_button_colors(self):
        screen = self.root.get_screen('main')
        for i in range(1, 4):
            for p in ['article_btn', 'meaning_btn']:
                btn = screen.ids.get(f'{p}{i}')
                if btn: btn.md_bg_color = self.theme_cls.primary_color

    def update_colors(self, prefix, txt):
        screen = self.root.get_screen('main')
        for i in range(1, 4):
            btn = screen.ids.get(f'{prefix}{i}')
            if btn: btn.md_bg_color = (0.1, 0.1, 0.4, 1) if btn.text == txt else self.theme_cls.primary_color

    def check_24h_ad(self, dt):
        if self.ad_settings.check_24h_ad_required():
            self.show_interstitial_ad(lambda: self.ad_settings.update_24h_ad_watched())

    def ensure_data_exists(self):
        os.makedirs('data/stages', exist_ok=True)

if __name__ == '__main__':
    GermanArticleTrainer().run()
