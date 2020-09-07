#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python

from PIL import Image
from glob import glob
import sys

for src in glob('*.PNG'):
    im = Image.open(src)
    # macのスクショから上部をカット
    im_crop = im.crop((0, 50, 750, 1334))
    # 切り出した画像を保存
    im_crop.save('topcut_{}.png'.format(src), quality=95)
