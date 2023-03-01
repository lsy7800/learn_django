from PIL import Image
from PIL import ImageDraw

img = Image.new(mode="RGB", size=(120, 30), color=(255, 255, 255))
# 画笔
# draw = ImageDraw.Draw(img, mode='RGB')

# 画点
# draw = ImageDraw.Draw(img, mode='RGB')

# 写入文本

"""
1. 第一个参数表示起始坐标
2. 第二个参数表示写入内容
3. 第三个参数表示颜色
"""
draw = ImageDraw.Draw(img, mode='RGB')
draw.text([0,0], 'Python', 'red')

img.show()


with open('code.png', 'wb') as f:
    img.save(f, format='png')
