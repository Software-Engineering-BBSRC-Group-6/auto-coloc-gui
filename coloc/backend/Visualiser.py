import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from math import dist
import preprocessingclass

def correlate(preprocessed, channels, num_clusts):
    """Returns the centres of clusters based on their PMCC.

    :param preprocessed: Preprocessed image data
    :type preprocessed: numpy array
    :param channels: List of indices referring to the populated channels in the data
    :type channels: list of integers of length 2.
    :param num_clusts: Number of clusters to output
    :type num_clusts: integer

    :return out: Intensity Correlation Analysis (ICA) array for every pixel in the image.
    :type out: numpy array
    :return clusts: List of (x, y) coordinates of cluster centres.
    :type clusts: List of tuples.
    """
    chan1, chan2 = [preprocessed[:, :, c] for c in channels]
    shape = np.shape(chan1)
    if np.shape(chan2) != shape:
        raise ValueError("Input arrays must have the same shape")

    mu1 = np.mean(chan1)
    mu2 = np.mean(chan2)
    
    out = np.zeros(shape)
    for x in range(shape[0]):
        for y in range(shape[1]):
            out[x, y] = (chan1[x, y] - mu1)*(chan2[x, y] - mu2)

    idx = np.unravel_index(np.argsort(out.ravel())[-num_clusts:], shape)  # Pull out the locations of the max values
    clusts = [(idx[0][i], idx[1][i]) for i in range(num_clusts)]    # Convert to tuple of coordinates
    return clusts


def fit_clusters(im, num_clusters):
    """Fits a series of k-means clusters using Scikit-Learn.

    :param im: image data
    :type im: numpy array of dims (heightxwidthxn-channels)
    :param num_clusters: Number of clusters to fit the data to.
    :type num_clusters: int

    :return clusts: Coordinates of the centres of clusters
    :type clusts: list of tuples? # NB check this
    """

    mask = im > 0
    im[mask] = 1        # Set nonzero values to 1
    xrange, yrange = np.shape(im)
    out = []
    for x in range(xrange):
        for y in range(yrange):
            if im[x, y] == 1:
                out.append([x, y]) 

    kmeans = KMeans(n_clusters=num_clusters, n_init=10, init='k-means++').fit(out)
    return kmeans.cluster_centers_.astype(int)


def compare_dists(ch1_clusters, ch2_clusters, max_dist):
    """Compares the distances between centroids of channel 1 and 2 clusters.

    :param ch1_clusters: List of the coordinates of all cluster centres for channel 1
    :type ch1_clusters: list of tuples (x, y)
    :param ch2_clusters: List of the coordinates of all cluster centres for channel 2
    :type ch2_clusters: list of tuples (x, y)

    :return euc_dists: Euclidean distances between the cluster centres
    """
    n = 0
    euc_dists = {}
    if len(ch1_clusters) != len (ch2_clusters):
        raise ValueError("Unequal cluster vectors")
    print("Ch1 cluster: ",ch1_clusters)
    print("Ch2 cluster: ",ch2_clusters)
    for n, c1_clust in enumerate(ch1_clusters):      
        for n2,c2_clust in enumerate(ch2_clusters):
            centroid_dist = dist(c1_clust, c2_clust)  # Compute euclidean distance
            if centroid_dist < max_dist:          # Check vs. threshold distance criterion
                euc_dists["Pair %s" % (n)] = {}
                # Record distance between cluster centroids. 
                euc_dists["Pair %s"%(n)]["Chan1"]=c1_clust.astype(int)
                euc_dists["Pair %s"%(n)]["Chan2"]=c2_clust.astype(int)
                print("Ch 1 n",str(n))
                print("Ch2 n", str(n2))
                print("Ch1 :",c1_clust)
                print("Ch2 :",c2_clust)
                print("Means: ",np.mean([c1_clust,c2_clust],axis=0))
                euc_dists["Pair %s"%(n)]["Avg"]=reversed(np.mean([c1_clust,c2_clust],axis=0).astype(int))
    return euc_dists


def get_colocs(im, channels, num_clusts, max_dist):
    """Compare two chanels of an image and return the set of KMeans cluster centroids.
    Centroids fall within a minimum distance of one another.

    :param im: Image data to compare
    :type im: Numpy array of shape (height x width x channels)
    :param num_clusts: Number of clusters to fit to the image
    :type num_clusts: int
    :param max_dist: Maximum allowed distance between cluster centres.
    :type max_dist: float

    :return euc_dists: Average positions of cluster centres for cluster positions closest to each other.
    :type euc_dists: list of tuples
    """
    if len(channels) != 2:
        raise ValueError("This function can only compare two channels at a time.")

    chan1, chan2 = [im[:, :, c] for c in channels]
    if chan1.shape != chan2.shape:
        raise ValueError("Input arrays must have the same shape")
    
    c1_clusters = fit_clusters(chan1, num_clusts)
    c2_clusters = fit_clusters(chan2, num_clusts)

    return compare_dists(c1_clusters, c2_clusters, max_dist)

def annotate(ax, title, coords=False):
    """Adds a circle and/title to a given position in a plot.
    
    :param ax: Axis to add the circle to.
    :type ax: matplotlib.pyplot axis object
    :param title: Title to add to the axes.
    :type title: string
    :param coords: Coordinates to plot the circle(s) at
    :type list: tuple of tuples (y, x)

    """
    if coords:
        for y, x in coords:
            circle = plt.Circle((x, y), 5, color='white', fill=False)
            ax.add_artist(circle)
            ax.set_title(title)
            # ax.set_aspect(aspect=1.0)
            ax.axis("off")
    else:
        ax.set_title(title)
        ax.axis("off")

def plot(original,denoised, clusters, output_dir, filename):
    """Plots an image, draws cluster markings on, and saves the figure.

    :param original: Input image data
    :type original: Numpy array of shape (height x width x channels)
    :param denoised: Denoised image data
    :type denoised: Numpy array of shape (height x width x channels)
    :param output_dir: Path to output the result to
    :type output_dir: string
    :param filename: Name to output file as
    :type filename: string
    """
    _, ax = plt.subplots(1, 2)
    ax[0].imshow(original)
    ax[1].imshow(denoised)
    titles= ['Original','Denoised']
    for a, axis in enumerate(ax):
        annotate(axis, titles[a], clusters)
    plt.savefig(output_dir+filename)
    # plt.show()        # Retained for debugging

def plot_kmeans(original, denoised, clusters, output_dir, filename):
    """Plots circles corresponding to overlapping kmeans centroids in the data
    
    """
    _, ax = plt.subplots(1, 2)
    ax[0].imshow(denoised)
    ax[1].imshow(original)
    titles=['Original','Denoised']
    for a,axis in enumerate(ax):
        for pair in clusters.keys():
            print(clusters[pair])
            coords = tuple(clusters[pair]["Avg"])
            print(coords)
            circle = plt.Circle(coords, 5, color='white', fill=False)
            axis.add_artist(circle)
        axis.set_title(titles[a])
        axis.axis("off")

    plt.savefig(output_dir+ filename)
    plt.show()

def run_visualiser(input_dict):
    # Get parameters from user input

    sourcefile, output_dir = [input_dict[key] for key in ["in_path", "out_path"]]
    default_params = {
        'threshold': 0.5,
        'channels': [0, 1],
        'num_clusts': 10,
        'min_dist': 15
    }

    for key in default_params.keys():
        if key not in input_dict.keys():
            input_dict[key] = default_params[key]

    print("Preprocessing")

    original, preprocessed = preprocessingclass.do_preprocess(sourcefile, input_dict['threshold'])
    original = original.frames.astype(int)
    preprocessed = preprocessed.frames

    if (input_dict["Run Intensity Correlation Analysis"] == 'Y') and (input_dict["Run KMeans"] == 'Y'):
        for n in range(original.shape[-1]):
        # for n in [8,9]:   # For debugging only
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n]

            corr_clusts = correlate(denoised, input_dict['channels'], input_dict['num_clusts'])
            plot(orig, denoised, corr_clusts, output_dir, "/img%s_original_corr" % n)
                   
            kmeans_clusts = get_colocs(denoised, input_dict['channels'], input_dict['num_clusts'], input_dict['min_dist'])
            # There is an error here - passing kmeans_clusts is affecting plotting of the denoised image (im)
            plot_kmeans(orig, denoised, kmeans_clusts, output_dir,"/img%s_original_kmeans" % n)
        
    elif (input_dict["Run Intensity Correlation Analysis"] == 'Y') and (input_dict["Run KMeans"] == 'N'):
        for n in range(original.shape[-1]):
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n]

            corr_clusts = correlate(denoised, input_dict['channels'], input_dict['num_clusts'])
            plot(orig,denoised,corr_clusts,output_dir,"/img%s_original_corr" % n)

    elif (input_dict["Run Intensity Correlation Analysis"] == 'N') and (input_dict["Run KMeans"] == 'Y'):
        # for n in range(original.shape[-1]):
        for n in [8,9]:
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n]

            kmeans_clusts = get_colocs(denoised, input_dict['channels'], input_dict['num_clusts'], input_dict['min_dist'])
            plot(orig, denoised, kmeans_clusts, output_dir, "/img%s_original_kmeans" % n)
    else:
        raise KeyError("Please select a method for colocalisation analysis") 

if __name__=="__main__":
    inputdict = {
    'in_path': './data/input/colocsample1bRGB_BG.tif',
    'out_path': './data/output',
    'threshold': 0.5,
    'channels': [0,1],
    'num_clusts': 10,
    'min_dist': 1000,
    'Run Intensity Correlation Analysis': 'Y',
    'Run KMeans': 'N'}
    
    run_visualiser(inputdict)
    


    