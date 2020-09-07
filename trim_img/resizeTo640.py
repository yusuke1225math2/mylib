#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python
from glob import glob
from PIL import Image

for src in glob('*.png'):
    img = Image.open(src)
    aspect = img.height / img.width
    img_resize_lanczos = img.resize((640, int(640 * aspect)), Image.LANCZOS)
    img_resize_lanczos.save('resized_{}.png'.format(src))
