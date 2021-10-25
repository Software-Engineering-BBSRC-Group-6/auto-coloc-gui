from datetime import datetime
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


class pipeline_object():
    """Pipeline object class. Any image becomes an instance of this class.
    The class operates using its methods to move an image through the pipeline.
    """
    def __init__(self, inpath, outpath, threshold=False):
        self.filepath = inpath
        self.outpath = outpath
        self.timestamp = (datetime.now()).strftime('%Y%m%d-%H%M%S')
        self.threshold = threshold

    def split(self):
        """Split input .tiff file into separate RGB slices
        """
        im = Image.open(self.filepath)
        self.image_obj = im
        self.num_frames = self.image_obj.n_frames
        self.smallest_dim = min(self.image_obj.size)
        self.frames = np.empty((self.num_frames, 3,
                                self.smallest_dim, self.smallest_dim,))
        for i in range(self.num_frames):
            self.frames[i, :, :, :] = np.moveaxis(np.asarray(self.reshape_frame(i)),-1,0)

        return

    def reshape_frame(self, i):
        """Reshapes an image such that the dimensions are square, using the dimension
        of the smallest side.
        """
        self.image_obj.seek(i)
        # Find smallest dimension n and set image size to square n x n.
        resized = self.image_obj.resize((self.smallest_dim, self.smallest_dim),
                                        resample=Image.LANCZOS)

        # Keep the new image array as a class variable.

        return resized

    def rescale(self, j, i):
        """Minmax rescale a 2D image at indices (i, j), where
        j is the channel index and i the frame index.

        :param j: index of channel
        :type j: integer
        :param i: index of frame
        :type i: integer"""
        im_2D = self.frames[i, j, :, :]

        if len(np.shape(im_2D)) != 2:
            raise ValueError("Input image should have two dimensions")
        if im_2D.all() == 0:
            return False
        elif self.threshold:
            self.frames[i, j, :, :] = (im_2D-im_2D.min())/(im_2D.max()-im_2D.min())
            trim = self.frames[i, j, :, :] < self.threshold
            self.frames[i, j, trim] = 0
            return True
        else:
            self.frames[i, j, :, :] = (im_2D-im_2D.min())/(im_2D.max()-im_2D.min())
            return True
    
    def rescale_all(self):
        """Rescale RGB image using minmax rescaling

        :param im_3d: input RGB image
        :type im_3d: numpy array"""

        for i in range(self.frames.shape[0]):
            for j in range(self.frames.shape[1]):
                self.rescale(j, i)

        return True

    def visualise(self):
        """Visualise the stack of RGB images."""
        im = Image.open(self.filepath)
        for i in range(self.frames.shape[-1]):
            im.seek(i)
            plt.imshow(np.asarray(im))
            plt.title("Original image {0}".format(str(i+1)))
            plt.colorbar
            plt.show()
            plt.imshow(np.moveaxis(self.frames[i, :, :, :],0,-1))
            plt.title("Processed image {0}".format(str(i+1)))
            plt.colorbar
            plt.show()
        


    
        
        
        

