from datetime import datetime
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tifffile
import exifread


class pipeline_object():
    """Pipeline object class. Any input .tiff image becomes an instance of this class.
    The class operates using its methods to move an image through the pipeline.


    :param inpath: File path of image in directory
    :type inpath: string or os.path
    :param outpath:
    :type outpath:
    :param threshold: threshold, defaults to False
    :type threshold: bool, optional
    """
    def __init__(self, inpath, outpath, threshold=False):
        # Some error handling to make sure the image file exists.
        if not os.path.exists(inpath):
            raise ValueError('File to be accessed does not exist.')
        elif not(inpath[-3:] != 'tif' or inpath[-4:] != 'tiff'):
            raise ValueError('File is not a .tif or .tiff.')

        self.filepath = inpath
        self.outpath = outpath
        self.timestamp = (datetime.now()).strftime('%Y%m%d-%H%M%S')
        if ((not isinstance(threshold, float)) and (threshold is not False)):
            raise TypeError('Invalid type for threshold.')
        self.threshold = threshold
        im = tifffile.imread(self.filepath)

        # Find out which dimensions are which and order correctly.
        with open(self.filepath, 'rb') as f:
            tags = exifread.process_file(f)

        dims_xyc = {'h': int(tags['Image ImageLength'].printable),
                    'w': int(tags['Image ImageWidth'].printable),
                    'c': 3}
        old_pos = {}

        for k, v in dims_xyc.items():
            found_idx = im.shape.index(v)
            if found_idx in old_pos.values():
                shapecopy = list(im.shape)
                del shapecopy[found_idx]
                new_idx = shapecopy.index(v)
                if new_idx >= found_idx:
                    old_pos[k] = new_idx + 1
                else:
                    old_pos[k] = new_idx
            else:    
                old_pos[k] = found_idx

        for v in im.shape:
            if v not in dims_xyc.values():
                old_pos['f'] = im.shape.index(v)

        self.frames = np.moveaxis(im, (old_pos['f'], old_pos['c'],
                                       old_pos['h'], old_pos['w']),
                                  (3, 2, 0, 1))

        self.smallest_dim = min(self.frames.shape[0:2])

    def reshape(self):
        """Reshapes an image such that the dimensions are square, using the dimension
        of the smallest side.

        :return: resized image
        :rtype: class object, image array
        """

        # Find smallest dimension n and set image size to square n x n.
        newframes = np.empty((self.smallest_dim, self.smallest_dim,
                             self.frames.shape[2], self.frames.shape[3]))
        for i in range(self.frames.shape[3]):
            for j in range(self.frames.shape[2]):
                newframes[:, :, j, i] = cv2.resize(self.frames[:, :, j, i],
                            (self.smallest_dim, self.smallest_dim),
                             interpolation=cv2.INTER_CUBIC)
        self.frames = newframes
        return

    def normalise(self, j):
        """Minmax rescale a 2D image at index j, where
        j is the channel index.

        :param j: index of channel
        :type j: integer

        :raises ValueError: Cannot process images that have less or more than 2 dimensions

        :return: boolean value indicating if the image was rescaled
        :rtype: bool
        """
        im_3D = self.frames[:, :, j, :]

        if len(np.shape(im_3D)) != 3:
            raise ValueError("Input image should have three dimensions")
        if im_3D.all() == 0 or (im_3D.max()-im_3D.min() == 0):
            return False
        elif self.threshold:
            im_3D = (im_3D-im_3D.min())/(im_3D.max()-im_3D.min())
            trim = im_3D < self.threshold
            im_3D[trim] = 0
            self.frames[:, :, j, :] = im_3D
            return True
        else:
            self.frames[:, :, j, :] = (im_3D-im_3D.min())/(im_3D.max()-im_3D.min())
            return True

    def normalise_all(self):
        """Rescale RGB image using minmax rescaling

        :param im_3d: input RGB image
        :type im_3d: numpy array

        :return:
        :rtype: bool
        """

        for j in range(self.frames.shape[2]):
            self.normalise(j)

        return True

    def visualise(self):
        """Visualise the stack of RGB images
        """
        im = Image.open(self.filepath)
        for i in range(self.frames.shape[-1]):
            im.seek(i)
            plt.imshow(np.asarray(im))
            plt.title("Original image {0}".format(str(i+1)))
            plt.colorbar()
            plt.show()
            plt.imshow(self.frames[:, :, :, i])
            plt.title("Processed image {0}".format(str(i+1)))
            plt.colorbar()
            plt.show()
