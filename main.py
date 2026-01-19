import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
import io
from kivy.core.image import Image as CoreImage
from kivy.resources import resource_find

def get_arabic_texture(text, font_size=50, color=(255, 255, 255, 255)):
    if not text:
        return None
    try:
        # 1. THE LOGIC FIX: Manually connect and flip
        # This is what works on your PC; we are forcing it for Android
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)

        # 2. THE PATH FIX: Find the font inside the APK
        font_path = resource_find('Amiri-Regular.ttf')
        if not font_path:
            return None
            
        # 3. THE PIXEL FIX: Draw the text to a 'Picture' (Texture)
        # We render at 2x size for "Deep Precision" (Retina-like quality)
        render_font = ImageFont.truetype(font_path, font_size * 2)
        
        # Calculate the box for the pixels
        dummy = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(dummy)
        bbox = draw.textbbox((0, 0), bidi_text, font=render_font)
        w, h = (bbox[2] - bbox[0]) + 20, (bbox[3] - bbox[1]) + 20

        # Create the image buffer in RAM
        img = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((10, 5), bidi_text, font=render_font, fill=color)

        # 4. THE HANDOFF: Send the pixels to Kivy
        data = io.BytesIO()
        img.save(data, format='png')
        data.seek(0)
        return CoreImage(io.BytesIO(data.read()), ext='png').texture
    except Exception as e:
        print(f"Android Rendering Error: {e}")
        return None
