from kivy.utils import platform
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty, ObjectProperty
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
from kivy.core.image import Image as CoreImage
import json
import random
import os
import time
import io

# --- 1. NEW IMPORTS FOR PIXEL RENDERING ---
try:
    from PIL import Image, ImageDraw, ImageFont
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

# --- 2. KIVMOB ---
try:
    from kivmob import KivMob
    HAS_KIVMOB = True
except ImportError:
    HAS_KIVMOB = False

# --- THE MAGIC TEXT-TO-IMAGE FUNCTION ---
def get_arabic_texture(text, font_size=45, color=(255, 255, 255, 255)):
    if not text or not HAS_LIBS:
        return None
    try:
        # Connect letters and fix direction
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        
        # Load the font for Pillow
        font_path = resource_find('Amiri-Regular.ttf')
        if not font_path: return None
        pil_font = ImageFont.truetype(font_path, font_size)
        
        # Measure text size
        dummy = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(dummy)
        bbox = draw.textbbox((0, 0), bidi_text, font=pil_font)
        w, h = bbox[2] - bbox[0] + 10, bbox[3] - bbox[1] + 10
        
        # Draw the text onto a transparent image
        img = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((5, 0), bidi_text, font=pil_font, fill=color)
        
        # Convert PIL image to Kivy Texture
        data = io.BytesIO()
        img.save(data, format='png')
        data.seek(0)
        kivy_img = CoreImage(io.BytesIO(data.read()), ext='png')
        return kivy_img.texture
    except Exception as e:
        print(f"Texture Error: {e}")
        return None

# Logic-only fix for titles/debug
def fix_arabic(text):
    if not text or not HAS_LIBS: return text
    return get_display(arabic_reshaper.reshape(text))

# --- AD SETTINGS ---
class AdSettings:
    def __init__(self):
        self.AD_FILE = 'ad_data.json'
        self.default_ad_data = {'last_24h_ad': 0, 'question_count': 0}
        self.load_ad_data()
    
    def load_ad_data(self):
        if os.path.exists(self.AD_FILE):
            try:
                with open(self.AD_FILE, 'r') as f: self.data = json.load(f)
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

class MockAdDialog(ModalView):
    def __init__(self, title, message, on_complete, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.4); self.auto_dismiss = False; self.on_complete = on_complete
        card = MDBoxLayout(orientation='vertical', padding="20dp", spacing="10dp")
        card.md_bg_color = (1, 1, 1, 1)
        card.add_widget(MDLabel(text=title, halign='center', font_style='H6'))
        card.add_widget(MDLabel(text=message, halign='center'))
        btn = MDFillRoundFlatButton(text="OK", pos_hint={'center_x': 0.5})
        btn.bind(on_release=self.finish)
        card.add_widget(btn); self.add_widget(card)
    def finish(self, *args):
        self.dismiss()
        if self.on_complete: self.on_complete()

# --- KV LAYOUT (MODIFIED FOR TEXTURES) ---
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
                
                # ARABIC MEANING BUTTONS (TEXTURE BASED)
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "10dp"
                    adaptive_height: True
                    
                    MDFillRoundFlatButton:
                        id: meaning_btn1
                        size_hint_x: 1
                        height: "56dp"
                        on_release: app.select_meaning(0)
                        Image:
                            texture: app.tex_m1
                            size_hint: None, None
                            size: self.texture_size
                            center: self.parent.center
                    
                    MDFillRoundFlatButton:
                        id: meaning_btn2
                        size_hint_x: 1
                        height: "56dp"
                        on_release: app.select_meaning(1)
                        Image:
                            texture: app.tex_m2
                            size_hint: None, None
                            size: self.texture_size
                            center: self.parent.center

                    MDFillRoundFlatButton:
                        id: meaning_btn3
                        size_hint_x: 1
                        height: "56dp"
                        on_release: app.select_meaning(2)
                        Image:
                            texture: app.tex_m3
                            size_hint: None, None
                            size: self.texture_size
                            center: self.parent.center

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
        
        # Explanation Image (Texture based)
        MDBoxLayout:
            size_hint_y: None
            height: "100dp"
            Image:
                texture: app.tex_expl
                size_hint: None, None
                size: self.texture_size
                pos_hint: {"center_x": 0.5}

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
    submit_enabled = BooleanProperty(False)
    result_text = StringProperty("")
    arabic_title = StringProperty("")
    
    # Texture properties for Arabic
    tex_m1 = ObjectProperty(None)
    tex_m2 = ObjectProperty(None)
    tex_m3 = ObjectProperty(None)
    tex_expl = ObjectProperty(None)
    
    current_stage = NumericProperty(1)
    unlocked_stages = NumericProperty(1)
    QUESTIONS_PER_STAGE = 100
    
    APP_ID = "ca-app-pub-9298331856947532~1106493604"

    def build(self):
        if os.path.exists('assets/fonts'):
            resource_add_path(os.path.abspath('assets/fonts'))
        
        self.arabic_title = fix_arabic("Artical lernen")
        self.theme_cls.primary_palette = "Blue"
        self.ad_settings = AdSettings()

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
        cols = max(2, int(Window.width / dp(120)))
        button_grid = MDGridLayout(adaptive_height=True, spacing="10dp", cols=cols)
        grid.add_widget(button_grid)

        for i in range(1, 101):
            is_locked = i > self.unlocked_stages
            btn = MDFillRoundFlatButton(
                text=str(i), disabled=is_locked,
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
            self.question_count = 1; self.correct_count = 0
            self.generate_question()
            self.root.current = 'main'
        except: print("Stage missing")

    def generate_question(self):
        if not self.unused_nouns: self.unused_nouns = list(self.nouns)
        noun_data = self.unused_nouns.pop()
        
        self.correct_art = noun_data['article']
        self.raw_meaning = noun_data['meaning'] # Raw Arabic string

        # Options
        self.article_options = random.sample(['der', 'die', 'das', 'den', 'dem'], 3)
        if self.correct_art not in self.article_options: self.article_options[0] = self.correct_art
        random.shuffle(self.article_options)

        other_m = [n['meaning'] for n in self.nouns if n['meaning'] != self.raw_meaning]
        self.raw_meanings_list = random.sample([self.raw_meaning] + other_m[:5], 3)
        random.shuffle(self.raw_meanings_list)

        # GENERATE TEXTURES
        self.tex_m1 = get_arabic_texture(self.raw_meanings_list[0])
        self.tex_m2 = get_arabic_texture(self.raw_meanings_list[1])
        self.tex_m3 = get_arabic_texture(self.raw_meanings_list[2])

        self.current_question = noun_data
        self.sentence = noun_data['sentences'].get('Nominativ', f"___ {noun_data['word']}")
        self.question_number = f"Stufe {self.current_stage} - {self.question_count}/100"
        self.submit_enabled = False; self.result_text = ""
        self.reset_colors()

    def select_article(self, t):
        self.selected_art = t
        self.submit_enabled = hasattr(self, 'selected_art') and hasattr(self, 'selected_mean_idx')

    def select_meaning(self, idx):
        self.selected_mean_idx = idx
        self.submit_enabled = hasattr(self, 'selected_art') and hasattr(self, 'selected_mean_idx')
        # Visual feedback for selection
        self.reset_colors()
        btn = self.root.get_screen('main').ids.get(f'meaning_btn{idx+1}')
        if btn: btn.md_bg_color = (0, 0, 0.5, 1)

    def reset_colors(self):
        screen = self.root.get_screen('main')
        for i in range(1, 4):
            btn = screen.ids.get(f'meaning_btn{i}')
            if btn: btn.md_bg_color = self.theme_cls.primary_color

    def check_answer(self):
        chosen_meaning = self.raw_meanings_list[self.selected_mean_idx]
        if self.selected_art == self.correct_art and chosen_meaning == self.raw_meaning:
            self.result_text = "✅ Richtig!"
            self.correct_count += 1
            Clock.schedule_once(lambda dt: self.next_question(), 1.0)
        else:
            expl_str = f"{self.current_question['word']} = {self.raw_meaning}"
            self.tex_expl = get_arabic_texture(expl_str, font_size=35, color=(0,0,0,255))
            self.root.current = 'result'

    def next_question(self):
        if self.question_count >= 100: self.root.current = 'stage_select'
        else:
            self.question_count += 1
            self.generate_question()
            self.root.current = 'main'

    def handle_stage_quit(self): self.root.current = 'stage_select'

if __name__ == '__main__':
    GermanArticleTrainer().run()
