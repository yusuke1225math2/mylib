#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python

from PIL import Image
from glob import glob
import sys

for src in glob('*.jpg'):
    im = Image.open(src)
    # macのスクショからLINE必要箇所を取得
    im_crop = im.crop((90, 0, 750, 1330))
    # 切り出した画像を保存
    im_crop.save('profilecut_{}.jpg'.format(src), quality=95)
