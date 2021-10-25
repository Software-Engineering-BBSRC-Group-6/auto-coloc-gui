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

""" ML section """

def fit_clusters(im,num_clusters):
    mask= im >0
    im[mask]=1
    xrange,yrange=np.shape(im)
    out=[]
    # Reconfigure kmeans to out xox1 cluster vectors + y prediction
    for x in range(xrange):
        for y in range(yrange):
            if im[x,y]==1:
                out.append([x,y])       # Check coordinates vs output in case it should be max - coord

    kmeans = KMeans(n_clusters=num_clusters,n_init=10,init='k-means++').fit(out)        # Add function to capture global distances for param optimisation
    
    return kmeans.cluster_centers_.astype(int)


def get_colocs(im,num_clusts,min_dist):
    r,g=[im[:,:,i] for i in [0,1]]      # Modify to use the full number of channels
    print("Getting clusters")
    r_clusters=fit_clusters(r,num_clusts)
    "Red clusters found"
    g_clusters=fit_clusters(g,num_clusts)
    "Green clusters founds"
    euc_dists={}
    n=1
    for rclust in r_clusters:       # There might be a more logical way of doing this
        for gclust in g_clusters:
            if dist(rclust,gclust) < min_dist:
                euc_dists["Pair %s"%(n)]={}
                euc_dists["Pair %s"%(n)]["R"]=rclust
                euc_dists["Pair %s"%(n)]["G"]=gclust
                euc_dists["Pair %s"%(n)]["Dist"]=dist(rclust,gclust)
                euc_dists["Pair %s"%(n)]["Avg"]=np.mean([rclust,gclust],axis=0).astype(int)
                n+=1
    return euc_dists

def plot_colocs(originals,preprocessed,num_clusts):
    for i,im in enumerate(preprocessed):
        fig, ax = plt.subplots(1,2)
        ax[0].imshow(originals[i])
        # ax[0].axis('off')
        euc_dists=get_colocs(im,num_clusts,min_dist=3)
        print(euc_dists)
        ax[1].imshow(im)
        for pair in euc_dists.keys():
            coords= tuple(euc_dists[pair]["Avg"])
            circle= plt.Circle(coords,5,color='g',fill=False)
            ax[1].add_artist(circle)
            # ax[1].axis('off')
        circletest=plt.Circle((80,80),5,color='pink',fill=False)
        
        plt.show()

sourcefile="./data/input/colocsample1bRGB_BG.tif"
threshold = 0.5
original, preprocessed = preprocess(sourcefile, threshold, visualise=False)
print(np.shape(original))
plot_colocs(original[8:10],preprocessed[8:10],40)
