from cv2 import kmeans
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.stats import pearsonr
from scipy import signal
import numpy as np
from math import dist

def annotate(ax, title,coords=False):
    if coords:
        for y,x in coords:
            circle= plt.Circle((x,y), 5, color='white', fill=False)
            ax.add_artist(circle)
            ax.set_title(title)
            ax.axis("off")
    else:
        ax.set_title(title)
        ax.axis("off")

def correlate(original,preprocessed,channels,num_clusts):

    chan1, chan2 = [preprocessed[:,:,c] for c in channels]
    shape=np.shape(chan1)
    if np.shape(chan2)!=shape:
        raise ValueError("Input arrays must have the same shape")
    mu1=np.mean(chan1)
    mu2=np.mean(chan2)
    out=np.zeros(shape)
    for x in range(shape[0]):
        for y in range(shape[1]):
            out[x,y]=(chan1[x,y]-mu1)*(chan2[x,y]-mu2)

    idx = np.unravel_index(np.argsort(out.ravel())[-num_clusts:], shape) # Pull out the locations of the max values
    clusts = [(idx[0][i],idx[1][i]) for i in range(num_clusts)]
    return clusts, out

import os

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

def compare_dists(ch1_clusters,ch2_clusters,min_dist):
    n=0
    euc_dists={}
    for c1_clust in ch1_clusters:      
        for c2_clust in ch2_clusters:
            centroid_dist=dist(c1_clust,c2_clust) # Compute euclidean distance
            if centroid_dist < min_dist:          # Check vs. threshold distance criterion
                euc_dists["Pair %s"%(n)]={}
                # Record distance between cluster centroids. NB Reversing is necessary here to get the correct [x,y] output coords
                euc_dists["Pair %s"%(n)]["Avg"]=reversed(np.mean([c1_clust,c2_clust],axis=0).astype(int))
                n+=1      
    return euc_dists

def get_colocs(im,channels,num_clusts,min_dist):
    """Compare two chanels of an image and return the set of KMeans cluster centroids falling within a minimum distance of one another"""
    if len(channels)!=2:
        raise ValueError("This function can only compare two channels at a time")

    chan1, chan2 = [im[:,:,c] for c in channels]
    if chan1.shape!=chan2.shape:
        raise ValueError("Input arrays must have the same shape")
    
    print("Getting KMeans clusters..")
    c1_clusters=fit_clusters(chan1,num_clusts)
    c2_clusters=fit_clusters(chan2,num_clusts)
    print("Complete")
    return compare_dists(c1_clusters,c2_clusters,min_dist)

def plot_corr(image,clusters,title,output_dir,filename,visualise=False):
    _, ax =plt.subplots(1,1)
    ax.imshow(image)
    annotate(ax,title,clusters)

    plt.savefig(os.path.join(output_dir,filename))
    if visualise:
        plt.show()

def plot_kmeans(image,clusters,title, output_dir,filename,min_dist=False,visualise=False):
    if not min_dist:
        min_dist=5
    _, ax =plt.subplots(1,1)
    ax.imshow(image)
    for pair in clusters.keys():
        coords= tuple(clusters[pair]["Avg"])
        circle= plt.Circle(coords,5,color='g',fill=False)
        ax.add_artist(circle)
    ax.axis("off")
    ax.set_title(title)
    plt.savefig(os.path.join(output_dir,filename))
    if visualise:
        plt.show()

from preprocessing import preprocess

def run_visualiser(input_dict):
    # Get parameters from user input

    sourcefile,output_dir = [input_dict[key] for key in ["in_path","out_path"]]
    if not input_dict['threshold']:
        threshold = 0.5
    else:
        threshold=input_dict['threshold']

    if not input_dict['channels']:
        channels=[0,1]
    else:
        channels=input_dict['channels']

    if not input_dict['num_clusts']:
        num_clusts = 10
    else:
        num_clusts=input_dict['num_clusts']

    if not input_dict['min_dist']:
        min_dist=15
    else:
        min_dist=input_dict['min_dist']

    visualise = True # This is for development only
    
    print("Preprocessing")

    original, preprocessed = preprocess(sourcefile, threshold, visualise=False)

    if (input_dict["Run Intensity Correlation Analysis"] =='Y') and (input_dict["Run KMeans"] =='Y'):
        for n,orig in enumerate(original):
            orig= original[n]
            denoised=preprocessed[n]

            corr_clusts,_=correlate(orig,denoised,channels,num_clusts)
            kmeans_clusts=get_colocs(denoised,channels,num_clusts,min_dist)

            plot_corr(orig,corr_clusts,"Original - ICA",output_dir,"img%s_original_corr"%n,visualise)
            plot_corr(denoised,corr_clusts,"Denoised - ICA",output_dir,"img%s_denoised_corr"%n,visualise)
            plot_kmeans(orig, kmeans_clusts, "Original - KMeans", output_dir,"/img%s_original_kmeans"%n,visualise)
            plot_kmeans(denoised, kmeans_clusts, "Denoised - KMeans", output_dir,"/img%s_denoised_kmeans"%n,visualise) 
        
    elif (input_dict["Run Intensity Correlation Analysis"] =='Y') and (input_dict["Run KMeans"] =='N'):
        for n,orig in enumerate(original):
            orig= original[n]
            denoised=preprocessed[n]

            corr_clusts,_=correlate(orig,denoised,channels,num_clusts)
            plot_corr(orig,corr_clusts,"Original - ICA",output_dir,"img%s_original_corr"%n,visualise)
            plot_corr(denoised,corr_clusts,"Denoised - ICA",output_dir,"img%s_denoised_corr"%n,visualise)

    elif (input_dict["Run Intensity Correlation Analysis"] =='N') and (input_dict["Run KMeans"] =='Y'):
        for n,orig in enumerate(original):
            orig= original[n]
            denoised=preprocessed[n]

            kmeans_clusts=get_colocs(denoised,channels,num_clusts,min_dist)
            plot_kmeans(orig, kmeans_clusts, "Original- KMeans", output_dir,"/img%s_original_kmeans"%n,visualise)
            plot_kmeans(denoised, kmeans_clusts, "Denoised- KMeans", output_dir,"/img%s_denoised_kmeans"%n,visualise)
    else:
        raise KeyError("Please select a method for colocalisation analysis") 

if __name__=="__main__":
    inputdict = {
    'in_path': './data/input/colocsample1bRGB_BG.tif',
    'out_path': './data/output',
    'threshold': 0.5,
    'channels': [0,1],
    'num_clusts': 5,
    'min_dist': 10,
    'visualise': True,
    'Run Intensity Correlation Analysis': 'Y',
    'Run KMeans': 'N'}

    run_visualiser(inputdict)



    