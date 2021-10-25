from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.index_tricks import ix_
from numpy.lib.utils import source
import os
from sklearn.cluster import KMeans

def listfiles():
    return [file for file in os.listdir(os.getcwd())]

def split(sourcefile,outpath):
    '''Split input .tiff file into separate RGB files and save to an output directory

    :param sourcefile: input multi-image .tiff
    :type sourcefile: string
    
    :return: list of file paths for image import'''

    im=Image.open(sourcefile)
    names=[]
    files=[file for file in os.listdir(outpath)]
    for i in range(32):    # Need to genericise this for any length of multiimage array
        n=outpath+'/img_%s.tif'%(i,)
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
    :type im_3d: numpy array

    :return: numpy array"""

    out=[]
    s=0
    for channel in [im_3d[:,:,i] for i in range(im_3d.shape[-1])]:
        out.append(rescale(channel,threshold))
        s+=1
    return np.dstack(out)

# Split source file

sourcefile="data/input/colocsample1bRGB_BG.tif"
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

def fit_clusters(im,num_clusters):
    mask= im >0
    im[mask]=1
    xrange,yrange=np.shape(im)
    out=[]
    for x in range(xrange):
        for y in range(yrange):
            if im[x,y]==1:
                out.append([x,y])

    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(out)
    print("Clusters: ",np.shape(kmeans.cluster_centers_))
    return kmeans.cluster_centers_.astype(int)

from math import dist

def get_colocs(im,num_clusts,min_dist):
    r,g=[im[:,:,i] for i in [0,1]]
    r_clusters=fit_clusters(r,num_clusts)
    g_clusters=fit_clusters(g,num_clusts)
    euc_dists={}
    n=1
    for rclust in r_clusters:
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
        euc_dists=get_colocs(im,num_clusts,min_dist=10)
        ax[1].imshow(im)
        for pair in euc_dists.keys():
            coords= tuple(euc_dists[pair]["G"])
            circle= plt.Circle(coords,5,color='g',fill=False)
            ax[1].add_artist(circle)
        
        plt.show()

plot_colocs(original[8:10],preprocessed[8:10],10)
