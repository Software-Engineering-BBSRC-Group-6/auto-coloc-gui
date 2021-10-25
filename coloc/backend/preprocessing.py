from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.index_tricks import ix_
from numpy.lib.utils import source
import os
from datetime import datetime

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


def reshape_im(sourcefile, timestamp):
    """Reshapes an image such that the dimensions are square, using the dimension
    of the smallest side.

    :param sourcefile: input multi-image .tiff
    :type sourcefile: string

    :return resized_file_path: Path to the new, downsized file.
    :type resized_file_path: string
    """
    im = Image.open(sourcefile)
    temp_dir_path = os.path.join('./data/output/', timestamp + '/')
    if not os.path.exists(temp_dir_paths):
        os.mkdir(temp_dir_path)

    # Find smallest dimension n and set image size to square n x n.
    smallest_dim = min(im.size)
    im.resize([smallest_dim, smallest_dim], resample=Image.LANCZOS)
    resized_file_path = os.path.join(temp_dir_path, os.path.basename(filename))

    im.save(resized_file_path)

    return resized_file_path


def split(sourcefile):
    """Split input .tiff file into separate RGB files and save to a sub-directory

    :param sourcefile: input multi-image .tiff
    :type sourcefile: string

    :return: list of file paths for image import'''
    """
    im = Image.open(sourcefile)
    names = []
    if 'data' not in listfiles():
        os.mkdir('data/')
    files = [file for file in os.listdir(os.getcwd()+'/data')]

    for i in range(im.n_frames):
        n = 'data/page_%s.tif' % (i,)
        if n not in files:
            names.append(n)
            im.seek(i)
            im.save(names[i])
    return names

def parse_ims(sourcefile,outpath=False):
    """Load images from a stacked .tiff file

    :param sourcefile: source file
    :type sourcefile: string

    return: array of Z-stacked images"""
    if not outpath:
        outpath = "data/output"
    splitfiles=split(sourcefile, outpath)
    im_arr=[]
    for im in splitfiles:
        im_arr.append(np.asarray(Image.open(im)))
    return np.asarray(im_arr)


def rescale(im_2D, threshold=False):
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
    :type im_3d: numpy array"""

    stack = ['R', 'G', 'B']
    out = []
    s = 0
    for channel in [im_3d[:, :, i] for i in range(im_3d.shape[-1])]:
        out.append(rescale(channel, threshold))
        s += 1
    return np.dstack(out)

# Split source file

sourcefile = "./data/input/colocsample1bRGB_BG.tif"
threshold = 0.5


def preprocess(sourcefile, threshold, visualise=True):
    im_arr = parse_ims(sourcefile)
    scaled_ims = np.asarray(
        [rescale_stack(im, threshold=threshold) for im in im_arr])
    s = 0
    if visualise:
        for i in range(len(im_arr)):
            plt.imshow(im_arr[i])
            plt.title("Original image %s" % (str(s+1)))
            plt.show()
            plt.imshow(scaled_ims[i])
            plt.title("Processed image %s" % (str(s+1)))
            plt.show()
            s += 1
    return im_arr, scaled_ims


original, preprocessed = preprocess(sourcefile, threshold, visualise=False)

for image in preprocessed[8:10]:
    print(np.shape(image))
    r, g = [image[:, :, i] for i in range(2)]
    print(np.shape(r))
