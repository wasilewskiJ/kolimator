import sys
from PIL import Image, ImageDraw, ImageFont

# Załóżmy, że biblioteka OLED jest już prawidłowo dodana do ścieżki
sys.path.append('/home/kolimator/OLED_Module_Code/RaspberryPi/python/lib/waveshare_OLED')

import OLED_0in96

# Funkcja inicjalizująca wyświetlacz
def init_display():
    disp = OLED_0in96.OLED_0in96()
    disp.Init()
    disp.clear()
    return disp

# Funkcja do rysowania tekstu na wyświetlaczu
def display_text(text, disp):
    mid_width = int(disp.width / 2)
    mid_height = int(disp.height / 2)

    # Tworzenie obrazu z buforem
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)

    # Rysowanie celownika
    draw.line([(mid_width + 5, mid_height), (mid_width - 5, mid_height)], fill=0)
    draw.line([(mid_width, mid_height + 5), (mid_width, mid_height - 5)], fill=0)
    draw.arc((mid_width - 8, mid_height - 8, mid_width + 8, mid_height + 8), 0, 360, fill=0)

    # Dodanie tekstu "X MOA UP"
    #font = ImageFont.load_default()  # Używamy domyślnej czcionki PIL
    #draw.text((mid_width - 30, mid_height + 10), text, font=font, fill=0)

    # Obracanie obrazu o 180 stopni przed wyświetleniem
    image1 = image1.rotate(180)

    # Wyświetlanie obrazu na ekranie
    disp.ShowImage(disp.getbuffer(image1))


if __name__ == "__main__":
    disp = init_display()
    display_text("X MOA UP", disp)
