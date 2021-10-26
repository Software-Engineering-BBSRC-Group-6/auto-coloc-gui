import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.stats import pearsonr
from scipy import signal
import numpy as np
from math import dist

""" Stats/ ML section """

def add_clusts(ax,coords):
    for y,x in coords:
        circle= plt.Circle((x,y), 5, color='white', fill=False)
        ax.add_artist(circle)

def correlate(orig,im,c1,c2,maxspots):
    chan1 = im[:,:,c1]
    chan2=im[:,:,c2]
    if chan1.shape!=chan2.shape:
        raise ValueError("Input arrays must have the same shape")
    mu1=np.mean(chan1)
    mu2=np.mean(chan2)
    out=np.zeros(chan1.shape)
    for x in range(chan1.shape[0]):
        for y in range(chan1.shape[1]):
            out[x,y]=(chan1[x,y]-mu1)*(chan2[x,y]-mu2)
    clusts=[]
    idx = np.unravel_index(np.argsort(out.ravel())[-maxspots:], out.shape) # Pull out the locations of the max values
    clusts = [(idx[0][i],idx[1][i]) for i in range(maxspots)]
    fig, ax =plt.subplots(1,3)
    ax[0].imshow(orig)
    ax[0].set_title("Input")
    ax[0].axis('off')
    ax[1].imshow(im)
    ax[1].set_title("Denoised")
    ax[1].axis('off')
    ax[2].imshow(out)
    ax[2].set_title("Correlated")
    ax[2].axis('off')
    for a in ax:
        add_clusts(a,clusts)
    # for y,x in clusts:
    #     circle=plt.Circle((x,y),5,color='white',fill=False)
    #     ax[0].add_artist(circle)
    plt.show()

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
                euc_dists["Pair %s"%(n)]["Avg"]=reversed(np.mean([rclust,gclust],axis=0).astype(int))
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

from preprocessing import preprocess

original, preprocessed = preprocess(sourcefile, threshold, visualise=False)
print(np.shape(original))
num_clusts=40
plot_colocs(original[8:10],preprocessed[8:10],10)
im=preprocessed[9]
correlate(original[9],im,0,1,10)


# r,g=[im[:,:,i] for i in [0,1]]      # Modify to use the full number of channels
# print("Getting clusters")
# r_clusters=fit_intensityclusters(r,num_clusts)
# print(np.shape(r_clusters))
# print(r_clusters[0])
# "Red clusters found"
# g_clusters=fit_clusters(g,num_clusts)
# "Green clusters founds"
# euc_dists={}
