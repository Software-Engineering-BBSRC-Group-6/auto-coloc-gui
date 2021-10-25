from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.index_tricks import ix_
from numpy.lib.utils import source
import os


def listfiles():
    return [file for file in os.listdir(os.getcwd())]

def split(sourcefile):
    '''Split input .tiff file into separate RGB files and save to a sub-directory

    :param sourcefile: input multi-image .tiff
    :type sourcefile: string
    
    :return: list of file paths for image import'''

    im=Image.open(sourcefile)
    names=[]
    if 'data' not in listfiles():
        os.mkdir('data/')
    files=[file for file in os.listdir(os.getcwd()+'/data')]
    print(files)
    for i in range(32):    # Need to genericise this for any length of multiimage array
        n='data/page_%s.tif'%(i,)
        if n not in files:
            names.append(n)
            im.seek(i)
            im.save(names[i])
    return names

def parse_ims(sourcefile):
    """Load images from a stacked .tiff file
    
    :param sourcefile: source file
    :type sourcefile: string
    
    return: array of Z-stacked images"""

    splitfiles=split(sourcefile)
    im_arr=[]
    for im in splitfiles:
        im_arr.append(np.asarray(Image.open(im)))
    return np.asarray(im_arr)

def rescale(im_2D,threshold=False):
    """Minmax rescale a 2D image
    
    :param im_2D: input array
    :type im_2D: numpy array
    
    return: rescaled image"""

    if len(np.shape(im_2D))!=2:
        raise ValueError("Input image should have two dimensions")
    if im_2D.all() == 0:
        return im_2D
    elif threshold:
        im_2D= (im_2D-im_2D.min())/(im_2D.max()-im_2D.min())
        trim=im_2D<threshold
        im_2D[trim]=0
        return im_2D
    else:
        return (im_2D-im_2D.min())/(im_2D.max()-im_2D.min()) 

def rescale_stack(im_3d,threshold=False):
    """Rescale RGB image using minmax rescaling
    
    :param im_3d: input RGB image
    :type im_3d: numpy array"""

    stack = ['R','G','B']
    out=[]
    s=0
    for channel in [im_3d[:,:,i] for i in range(im_3d.shape[-1])]:
        out.append(rescale(channel,threshold))
        s+=1
    return np.dstack(out)

# Split source file

sourcefile="colocsample1bRGB_BG.tif"
threshold=0.5

def preprocess(sourcefile,threshold,visualise=True):
    im_arr=parse_ims(sourcefile)
    scaled_ims=np.asarray([rescale_stack(im,threshold=threshold) for im in im_arr])
    s=0
    if visualise:
        for i in range(len(im_arr)):
            plt.imshow(im_arr[i])
            plt.title("Original image %s"%(str(s+1)))
            plt.show()
            plt.imshow(scaled_ims[i])
            plt.title("Processed image %s"%(str(s+1)))
            plt.show()
            s+=1
    return im_arr, scaled_ims

original, preprocessed = preprocess(sourcefile,threshold,visualise=False)

for image in preprocessed[8:10]:
    print(np.shape(image))
    r,g = [image[:,:,i] for i in range(1)]
    print(np.shape(r))

