import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from math import dist
import os
from ..backend.preprocessingclass import do_preprocess


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
            ax.axis("off")
    else:
        ax.set_title(title)
        ax.axis("off")


def correlate(original, preprocessed, channels, num_clusts):
    """Returns the centres of clusters based on their PMCC.

    :param preprocessed: Preprocessed image data
    :type preprocessed: numpy array
    :param channels: List of indices referring to the populated channels in the data
    :type channels: list of integers of length 2.
    :param num_clusts: Number of clusters to output
    :type num_clusts: integer

    :return out: PMCC array for every pixel in the image.
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
    clusts = [(idx[0][i], idx[1][i]) for i in range(num_clusts)]
    return clusts, out


def fit_clusters(im, num_clusters):
    """Fits a series of k-means clusters using SKLearn.

    :param im: image data
    :type im: numpy array of dims (heightxwidthxn-channels)
    :param num_clusters: Number of clusters to fit the data to.
    :type num_clusters: int

    :return clusts: Coordinates of the centres of clusters
    :type clusts: list of tuples? # NB check this
    """

    mask = im > 0
    im[mask] = 1
    xrange, yrange = np.shape(im)
    out = []
    # Reconfigure kmeans to out xox1 cluster vectors + y prediction
    for x in range(xrange):
        for y in range(yrange):
            if im[x, y] == 1:
                out.append([x, y])       # Check coordinates vs output in case it should be max - coord

    kmeans = KMeans(n_clusters=num_clusters, n_init=10, init='k-means++').fit(out)        # Add function to capture global distances for param optimisation
    return kmeans.cluster_centers_.astype(int)


def compare_dists(ch1_clusters, ch2_clusters, max_dist):
    """Compares the distances between centres of channel 1 and 2 clusters.

    :param ch1_clusters: List of the coordinates of all cluster centres for channel 1
    :type ch1_clusters: list of tuples (x, y)
    :param ch2_clusters: List of the coordinates of all cluster centres for channel 2
    :type ch2_clusters: list of tuples (x, y)

    :return euc_dists: Euclidean distances between the cluster centres
    """
    n = 0
    euc_dists = {}
    for c1_clust in ch1_clusters:      
        for c2_clust in ch2_clusters:
            centroid_dist = dist(c1_clust, c2_clust)  # Compute euclidean distance
            if centroid_dist < max_dist:          # Check vs. threshold distance criterion
                euc_dists["Pair %s" % (n)] = {}
                # Record distance between cluster centroids. NB Reversing is necessary here to get the correct [x,y] output coords
                euc_dists["Pair %s" % (n)]["Avg"] = reversed(np.mean([c1_clust, c2_clust], axis=0).astype(int))
                n += 1      
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
    
    print("Getting KMeans clusters..")
    c1_clusters = fit_clusters(chan1, num_clusts)
    c2_clusters = fit_clusters(chan2, num_clusts)
    print("Complete")
    return compare_dists(c1_clusters, c2_clusters, max_dist)


def plot_corr(image, clusters, title, output_dir, filename, visualise=False):
    """Plots an image, draws cluster markings on, and saves the figure.

    :param image: Image data
    :type im: Numpy array of shape (height x width x channels)
    :param title: Image title
    :type title: string
    :param output_dir: Path to output the result to
    :type output_dir: string
    :param filename: Name to output file as
    :type filename: string
    :param visualise: Whether to show the plots at the end
    :type visualise: boolean, default False.
    """
    _, ax = plt.subplots(1, 1)
    ax.imshow(image)
    annotate(ax, title, clusters)

    plt.savefig(os.path.join(output_dir, filename))
    if visualise:
        plt.show()


def plot_kmeans(image, clusters, title, output_dir, filename,
                max_dist=5, visualise=False):
    """Plots circles corresponding to kmeans in the data
    
    :param image: Image data
    :type im: Numpy array of shape (height x width x channels)
    :param title: Image title
    :type title: string
    :param output_dir: Path to output the result to
    :type output_dir: string
    :param filename: Name to output file as
    :type filename: string
    :param visualise: Whether to show the plots at the end, default False
    :type visualise: boolean
    :param min_dist: Maximum distance (in px) between cluster centres in different channels
    :type min_dist: float
    """
    _, ax = plt.subplots(1, 1)
    ax.imshow(image)

    for pair in clusters.keys():
        coords = tuple(clusters[pair]["Avg"])
        circle = plt.Circle(coords, max_dist, color='g', fill=False)
        ax.add_artist(circle)
    ax.axis("off")
    ax.set_title(title)
    plt.savefig(os.path.join(output_dir, filename))
    if visualise:
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

    visualise = False  # This is for development only

    print("Preprocessing")

    original, preprocessed = do_preprocess(sourcefile, input_dict['threshold'], visualise=visualise)
    original = original.frames.astype(int)
    preprocessed = preprocessed.frames

    if (input_dict["Run Intensity Correlation Analysis"] == 'Y') and (input_dict["Run KMeans"] == 'Y'):
        for n in range(original.shape[-1]):
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n]

            corr_clusts, _ = correlate(orig, denoised,
                                       input_dict['channels'],
                                       input_dict['num_clusts'])
            kmeans_clusts = get_colocs(denoised,
                                       input_dict['channels'],
                                       input_dict['num_clusts'],
                                       input_dict['min_dist'])

            plot_corr(orig, corr_clusts, "Original - ICA",
                      output_dir, "img%s_original_corr" % n, visualise)
            
            plot_corr(denoised, corr_clusts, "Denoised - ICA",
                      output_dir, "img%s_denoised_corr" % n, visualise)
            
            plot_kmeans(orig, kmeans_clusts, "Original - KMeans",
                        output_dir, "/img%s_original_kmeans" % n, visualise)
            
            plot_kmeans(denoised, kmeans_clusts, "Denoised - KMeans",
                        output_dir, "/img%s_denoised_kmeans" % n, visualise)
        
    elif (input_dict["Run Intensity Correlation Analysis"] == 'Y') and (input_dict["Run KMeans"] == 'N'):
        for n in range(original.shape[-1]):
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n]

            corr_clusts, _ = correlate(orig, denoised, input_dict['channels'], input_dict['num_clusts'])
            plot_corr(orig, corr_clusts, "Original - ICA", output_dir, "img%s_original_corr" % n, visualise)
            plot_corr(denoised, corr_clusts, "Denoised - ICA", output_dir, "img%s_denoised_corr" % n, visualise)

    elif (input_dict["Run Intensity Correlation Analysis"] == 'N') and (input_dict["Run KMeans"] == 'Y'):
        for n in range(original.shape[-1]):
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n]

            kmeans_clusts = get_colocs(denoised, input_dict['channels'], input_dict['num_clusts'], input_dict['min_dist'])
            plot_kmeans(orig, kmeans_clusts, "Original- KMeans", output_dir, "/img%s_original_kmeans" % n, visualise)
            plot_kmeans(denoised, kmeans_clusts, "Denoised- KMeans", output_dir, "/img%s_denoised_kmeans" % n, visualise)
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



    