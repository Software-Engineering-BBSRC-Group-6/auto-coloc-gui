from PIL import Image
import numpy as np

im = Image.open('./data/input/colocsample1bRGB_BG.tif')
# im = Image.open('./data/input/Composite_12156.tif')
im=np.array(im.convert('RGB'))
print(im.shape)
