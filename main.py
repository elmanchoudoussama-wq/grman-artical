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
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivy.uix.modalview import ModalView
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path, resource_find
import json
import random
import os
import time

# --- 1. IMPORT KIVMOB ---
try:
    from kivmob import KivMob
    HAS_KIVMOB = True
except ImportError:
    HAS_KIVMOB = False

# --- 2. ARABIC SUPPORT (ENHANCED CONFIG) ---
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
        # Force the reshaper to use ligatures (connections)
        configuration = {
            'delete_harakat': True,
            'support_ligatures': True,
            'unshaped_to_shaped': True
        }
        reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)
        reshaped_text = reshaper.reshape(text)
        # Fix the direction for Right-to-Left
        return get_display(reshaped_text)
    except Exception as e:
        print(f"Arabic Error: {e}")
        return text

# --- AD SETTINGS ---
class AdSettings:
    def __init__(self):
        self.AD_FILE = 'ad_data.json'
        self.default_ad_data = {'last_24h_ad': 0, 'question_count': 0}
        self.data = self.default_ad_data.copy()
        self.load_ad_data()
    
    def load_ad_data(self):
        if os.path.exists(self.AD_FILE):
            try:
                with open(self.AD_FILE, 'r') as f:
                    self.data = json.load(f)
            except: pass
    
    def save_ad_data(self):
        with open(self.AD_FILE, 'w') as f: json.dump(self.data, f)
    
    def increment_question_count(self):
        self.data['question_count'] = self.data.get('question_count', 0) + 1
        self.save_ad_data()

# --- KV LAYOUT ---
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
        MDScrollView:
            MDBoxLayout:
                id: stage_grid
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "15dp"

<MainScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 1, 1, 1, 1
        MDTopAppBar:
            title: app.question_number
            left_action_items: [["arrow-left", lambda x: app.handle_stage_quit()]]
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
                MDGridLayout:
                    cols: 3
                    spacing: "10dp"
                    size_hint_y: None
                    height: "60dp"
                    MDFillRoundFlatButton:
                        text: app.article_options[0]
                        size_hint_x: 1
                        on_release: app.select_article(self.text)
                    MDFillRoundFlatButton:
                        text: app.article_options[1]
                        size_hint_x: 1
                        on_release: app.select_article(self.text)
                    MDFillRoundFlatButton:
                        text: app.article_options[2]
                        size_hint_x: 1
                        on_release: app.select_article(self.text)
                MDLabel:
                    text: "Bedeutung:"
                    halign: "center"
                    font_style: "Subtitle1"
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "10dp"
                    adaptive_height: True
                    MDFillRoundFlatButton:
                        text: app.meaning_options[0]
                        font_style: "Button"
                        size_hint_x: 1
                        on_release: app.select_meaning(self.text)
                    MDFillRoundFlatButton:
                        text: app.meaning_options[1]
                        font_style: "Button"
                        size_hint_x: 1
                        on_release: app.select_meaning(self.text)
                    MDFillRoundFlatButton:
                        text: app.meaning_options[2]
                        font_style: "Button"
                        size_hint_x: 1
                        on_release: app.select_meaning(self.text)
                MDFillRoundFlatButton:
                    text: "PRÜFEN"
                    size_hint_x: 1
                    disabled: not app.submit_enabled
                    on_release: app.check_answer()
                MDLabel:
                    text: app.result_text
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0, 0.6, 0, 1
                    font_style: "H6"

<ResultScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "30dp"
        spacing: "20dp"
        MDLabel:
            text: "Erklärung"
            halign: "center"
            font_style: "H4"
        MDLabel:
            text: app.explanation_text
            halign: "center"
            font_style: "H6"
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
    question_number = StringProperty("")
    article_options = ListProperty(["", "", ""])
    meaning_options = ListProperty(["", "", ""])
    submit_enabled = BooleanProperty(False)
    result_text = StringProperty("")
    explanation_text = StringProperty("")
    arabic_title = StringProperty("")
    unlocked_stages = NumericProperty(1)
    QUESTIONS_PER_STAGE = 100
    
    APP_ID = "ca-app-pub-9298331856947532~1106493604"

    def build(self):
        # 1. Register Paths
        if os.path.exists('assets/fonts'):
            resource_add_path(os.path.abspath('assets/fonts'))
        
        font_path = resource_find('Amiri-Regular.ttf')
        
        if font_path:
            LabelBase.register(name='Amiri', fn_regular=font_path)
            # 2. FORCE GLOBAL FONT OVERWRITE FOR KIVYMD
            self.theme_cls.font_styles.update({
                "Button": ["Amiri", 14, False, 0.1],
                "H4": ["Amiri", 34, False, 0.25],
                "H5": ["Amiri", 24, False, 0],
                "H6": ["Amiri", 20, False, 0],
                "Subtitle1": ["Amiri", 16, False, 0],
                "Body1": ["Amiri", 16, False, 0],
            })
        
        self.arabic_title = fix_arabic("Artical lernen")
        self.theme_cls.primary_palette = "Blue"
        self.ad_settings = AdSettings()

        # Initialize Ads
        self.ads = None
        if platform == 'android' and HAS_KIVMOB:
            try:
                self.ads = KivMob(self.APP_ID)
                self.ads.request_banner()
            except: pass
        
        return Builder.load_string(KV_STRING)

    def on_start(self):
        self.load_progress()
        self.build_stage_menu()

    def load_progress(self):
        if os.path.exists('progress.json'):
            try:
                with open('progress.json', 'r') as f:
                    self.unlocked_stages = json.load(f).get('unlocked', 1)
            except: pass

    def save_progress(self):
        with open('progress.json', 'w') as f:
            json.dump({'unlocked': self.unlocked_stages}, f)

    def build_stage_menu(self):
        grid = self.root.get_screen('stage_select').ids.stage_grid
        grid.clear_widgets()
        button_grid = MDGridLayout(adaptive_height=True, spacing="10dp", cols=3)
        grid.add_widget(button_grid)

        for i in range(1, 101):
            is_locked = i > self.unlocked_stages
            btn = MDFillRoundFlatButton(
                text=str(i),
                disabled=is_locked,
                on_release=lambda x, s=i: self.load_stage(s)
            )
            button_grid.add_widget(btn)

    def load_stage(self, stage_number):
        self.current_stage = stage_number
        try:
            with open(f'data/stages/stage_{stage_number}.json', 'r', encoding='utf-8') as f:
                self.nouns = json.load(f)
            self.unused_nouns = list(self.nouns)
            random.shuffle(self.unused_nouns)
            self.question_count = 1
            self.correct_count = 0
            self.generate_question()
            self.root.current = 'main'
        except: print("Stage missing")

    def generate_question(self):
        noun_data = self.unused_nouns.pop() if self.unused_nouns else self.nouns[0]
        self.correct_art = noun_data['article']
        self.correct_mean = fix_arabic(noun_data['meaning'])

        all_art = ['der', 'die', 'das']
        self.article_options = all_art
        random.shuffle(self.article_options)

        other_m = [fix_arabic(n['meaning']) for n in self.nouns if n['meaning'] != noun_data['meaning']]
        self.meaning_options = random.sample([self.correct_mean] + other_m[:5], 3)
        random.shuffle(self.meaning_options)

        self.current_question = noun_data
        self.sentence = noun_data['sentences'].get('Nominativ', f"___ {noun_data['word']}")
        self.question_number = f"Stufe {self.current_stage} - {self.question_count}/100"
        self.submit_enabled = False
        self.result_text = ""

    def select_article(self, t):
        self.selected_art = t
        self.submit_enabled = hasattr(self, 'selected_art') and hasattr(self, 'selected_mean')

    def select_meaning(self, t):
        self.selected_mean = t
        self.submit_enabled = hasattr(self, 'selected_art') and hasattr(self, 'selected_mean')

    def check_answer(self):
        if self.selected_art == self.correct_art and self.selected_mean == self.correct_mean:
            self.result_text = "✅ Richtig!"
            self.correct_count += 1
            Clock.schedule_once(lambda dt: self.next_question(), 1.0)
        else:
            self.explanation_text = fix_arabic(f"Falsch! {self.current_question['word']} = {self.current_question['meaning']}")
            self.root.current = 'result'

    def next_question(self):
        if self.question_count >= 100:
            self.root.current = 'stage_select'
        else:
            self.question_count += 1
            self.generate_question()
            self.root.current = 'main'

    def handle_stage_quit(self):
        self.root.current = 'stage_select'

if __name__ == '__main__':
    GermanArticleTrainer().run()
