#!/Library/Frameworks/Python.framework/Versions/3.6/Resources/Python.app/Contents/MacOS/Python

from PIL import Image
from glob import glob
import sys

for src in glob('*.png'):
    im = Image.open(src)
    # macのスクショからトップのバー部分だけ削除
    # im_crop = im.crop((0, 48, 2870, 1790))
    im_crop = im.crop((0, 10, 638, 397))
    # 切り出した画像を保存
    im_crop.save('cropped_{}'.format(src), quality=95)
