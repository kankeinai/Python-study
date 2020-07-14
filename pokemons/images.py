import sys
import os
from PIL import Image, ImageFilter
from translate import Translator
translation = Translator(to_lang='ja')
# python3 pokemons/ new/

my_dir = sys.argv[1]
new_folder = sys.argv[2]
if not os.path.exists(new_folder):
    os.mkdir(new_folder)
for pictures in os.listdir(my_dir):
    if os.path.splitext(pictures)[-1] == ".jpg":
        img = Image.open(my_dir+pictures)
        img = img.filter(ImageFilter.SHARPEN)
        img = img.convert("L")
        img.thumbnail((100, 100))
        filename = os.path.splitext(pictures)[0]
        img.save(new_folder + translation.translate(filename) + ".png", 'png')
        print(f"{pictures} is done, {img.size}")
print("bye.")
