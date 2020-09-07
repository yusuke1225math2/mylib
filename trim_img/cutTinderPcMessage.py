#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python

from PIL import Image
from glob import glob
import sys

for src in glob('*.png'):
    im = Image.open(src)
    # macの画面スクショからtinderやり取り部分だけを切り取り
    im_crop = im.crop((879, 477, 2169, 1683))
    # 切り出した画像を保存
    im_crop.save('cropped_{}.png'.format(src), quality=95)
