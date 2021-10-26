from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from datetime import datetime
import cv2
from math import dist

inputdict = {
    'in_path': './data/in/test.tiff',
    'out_path': './data/out/test.tiff',
    'threshold': 0.3
    }

def generate_timestamp():
    """Generates a timestamp, based on the current time.

    :return timestamp: The current time, in format YYYYMMDD-hhmmss
    """
    timestamp = (datetime.now()).strftime('%Y%m%d-%H%M%S')
    return timestamp

def listfiles():
    return [file for file in os.listdir(os.getcwd())]

def split(sourcefile):
    """Load images from a stacked .tiff file

    :param sourcefile: source file
    :type sourcefile: string

    return: array of Z-stacked images"""

    im = Image.open(sourcefile)
    out=[]
    for i in range(im.n_frames):
        im.seek(i)
        out.append(np.asarray(im))
    return np.asarray(out)


def resize_ims(im_array):
    """Resize images from a Z-stack"""

    im_arr=[]
    for im in im_array:
        smallest_dim = min(np.shape(im)[:2])
        im=np.dstack([cv2.resize(im[:,:,i],dsize=(smallest_dim,smallest_dim), interpolation=cv2.INTER_CUBIC) for i in range(3)])
        im_arr.append(im)
    return np.asarray(im_arr)


def normalise(im_2D, threshold=False):
    """Minmax rescale a 2D image

    :param im_2D: input array
    :type im_2D: numpy array

    return: rescaled image"""

    if len(np.shape(im_2D)) != 2:
        raise ValueError("Input image should have two dimensions")
    if im_2D.all() == 0:
        return im_2D
    elif threshold:
        im_2D = (im_2D-im_2D.min())/(im_2D.max()-im_2D.min())
        trim = im_2D < threshold
        im_2D[trim] = 0
        return im_2D
    else:
        return (im_2D-im_2D.min())/(im_2D.max()-im_2D.min())


def rescale_stack(im_3d, threshold=False):
    """Rescale RGB image using minmax rescaling

    :param im_3d: input RGB image
    :type im_3d: numpy array

    :return: numpy array"""

    out = []
    s = 0
    for channel in [im_3d[:, :, i] for i in range(im_3d.shape[-1])]:
        out.append(normalise(channel, threshold))
        s += 1
    return np.dstack(out)

def preprocess(sourcefile, threshold, visualise=True):
    im_arr=resize_ims(split(sourcefile))
    scaled_ims = np.asarray(
        [rescale_stack(im, threshold=threshold) for im in im_arr])

    if visualise:
        for s,i in enumerate(len(im_arr)):
            plt.imshow(im_arr[i])
            plt.title("Original image %s" % (str(s+1)))
            plt.show()
            plt.imshow(scaled_ims[i])
            plt.title("Processed image %s" % (str(s+1)))
            plt.show()

    return im_arr, scaled_ims