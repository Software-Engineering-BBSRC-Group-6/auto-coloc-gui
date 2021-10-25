from datetime import datetime
import os
from PIL import Image


class pipeline_object():
    """Pipeline object class. Any image becomes an instance of this class.
    The class operates using its methods to move an image through the pipeline.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.timestamp = (datetime.now()).strftime('%Y%m%d-%H%M%S')
        self.temp_dir_path = os.path.join('./data/output/', 
                                          self.timestamp + '/')
        if not os.path.exists(self.temp_dir_paths):
            os.mkdir(self.temp_dir_path)

    def reshape_im(self):
        """Reshapes an image such that the dimensions are square, using the dimension
        of the smallest side.

        :param sourcefile: input multi-image .tiff
        :type sourcefile: string

        :return resized_file_path: Path to the new, downsized file.
        :type resized_file_path: string
        """
        im = Image.open(self.filepath)
        # Find smallest dimension n and set image size to square n x n.
        smallest_dim = min(im.size)
        im.resize([smallest_dim, smallest_dim], resample=Image.LANCZOS)
        resized_file_path = os.path.join(self.filepath, 'resized',
                                         os.path.basename(self.filepath))
        # Save and keep the new path as a class variable.
        im.save(resized_file_path)
        self.resized_file_path = resized_file_path

        return
    
    def split(self):
        """Split input .tiff file into separate RGB files and save to a sub-directory

        :param sourcefile: input multi-image .tiff
        :type sourcefile: string

        :return: list of file paths for image import'''
        """
        im = Image.open(self.resized_file_path)
        self.num_frames = im.n_frames

        for i in range(self.num_frames):
            im.save(os.path.join(self.temp_dir_path, 'page_{0}.tif'.format(i)))
        
        return

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
        
        
        

