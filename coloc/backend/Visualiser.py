import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import math
from backend.preprocessingclass import do_preprocess
import os

def correlate(denoised, channels, num_clusts):
    """Returns the centres of clusters based on Intensity Correlation Analysis (ICA).

    :param preprocessed: Preprocessed image data
    :type preprocessed: numpy array
    :param channels: List of indices referring to the populated channels in the data
    :type channels: list of integers of length 2
    :param num_clusts: Number of clusters to output
    :type num_clusts: integer
    :return out: Intensity Correlation Analysis (ICA) array for every pixel in the image.
    :type out: numpy array
    :return clusts: List of (x, y) coordinates of cluster centres.
    :type clusts: List of tuples.
    """
    chan1, chan2 = [denoised[:, :, c] for c in channels]
    shape = np.shape(chan1)
    if np.shape(chan2) != shape:
        raise ValueError("Input arrays must have the same shape")

    if np.array_equal(chan1, chan2):
        raise ValueError("Input channels are identical")

    mu1 = np.mean(chan1)
    mu2 = np.mean(chan2)

    out = np.zeros(shape)
    for x in range(shape[0]):
        for y in range(shape[1]):
            # Compute ICA between two channels for each pixel
            out[x, y] = (chan1[x, y] - mu1)*(chan2[x, y] - mu2)
    print("\tTotal fluorescence overlap: {:.2e}".format(np.sum(out)))
    # Pull out the locations of the top n max values
    idx = np.unravel_index(np.argsort(out.ravel())[-num_clusts:], shape)
    # Convert to tuple of coordinates
    clusts = [(idx[0][i], idx[1][i]) for i in range(num_clusts)]
    return clusts


def fit_clusters(im, num_clusters):
    """Fits a series of k-means clusters using Scikit-Learn.
    :param im: image data
    :type im: numpy array of dims (heightxwidthxn-channels)
    :param num_clusters: Number of clusters to fit to the data
    :type num_clusters: int
    :return clusts: Coordinates of the centres of clusters
    :type clusts: list of tuples? # NB check this
    """

    if 0 not in im:
        raise ValueError("No zero values, please apply a threshold")
    xrange, yrange = np.shape(im)
    out = []
    for x in range(xrange):
        for y in range(yrange):
            # Select only pixels not masked out during denoising
            if im[x, y] != 0:
                out.append([x, y])
    # Derive cluster centroids and pass as an array of coordinates
    kmeans = KMeans(n_clusters=num_clusters, n_init=5,
                    init='k-means++').fit(out)

    return np.asarray(kmeans.cluster_centers_).astype('int')


def compare_dists(ch1_clusters, ch2_clusters, max_dist):
    """Compares the distances between centroids of channel 1 and 2 clusters.
    :param ch1_clusters: List of the coordinates of all cluster centres for channel 1
    :type ch1_clusters: list of tuples (x, y)
    :param ch2_clusters: List of the coordinates of all cluster centres for channel 2
    :type ch2_clusters: list of tuples (x, y)
    :param max_dist: defines distance threshold for definition of clusters as colocalised
    :type max_dist: int

    :return euc_dists: Euclidean distances between the cluster centres
    :type euc_dists: dictionary
    """
    n = 0
    euc_dists = {}
    if len(ch1_clusters) != len(ch2_clusters):
        raise ValueError("Unequal cluster vectors")
    for c1_clust in ch1_clusters:
        for c2_clust in ch2_clusters:
            # Compute euclidean distance
            centroid_dist = math.dist(c1_clust, c2_clust)
            # Check vs. distance criterion
            if centroid_dist < max_dist:
                euc_dists["Pair %s" % (n)] = {}
                # Record distance between cluster centroids
                # NB reversal is necessary to map to 2D image coordinates
                euc_dists["Pair %s" % (n)]["Centroid"] = list(
                                                        reversed(
                                                            np.mean([c1_clust,
                                                                     c2_clust],
                                                                    axis=0
                                                                    ).astype(
                                                                        int)))

                n += 1
    return euc_dists


def get_colocs(im, channels, num_clusts, max_dist):
    """Compare two chanels of an image and return the set of KMeans cluster centroids.
    Centroids fall within a minimum distance of one another.
    :param im: Image data to compare
    :type im: Numpy array of shape (height x width x channels)
    :param channels: index of the channels of interest, defaults to [0,1]
    :type channels: list
    :param num_clusts: Number of clusters to fit to the image
    :type num_clusts: int
    :param max_dist: Maximum allowed distance between cluster centres
    :type max_dist: float
    :return euc_dists: Average positions of cluster centres for cluster positions closest to each other.
    :type euc_dists: list of tuples
    """
    if len(channels) != 2:
        raise ValueError("This function can only ",
                         "compare two channels at a time.")

    chan1, chan2 = [im[:, :, c] for c in channels]
    if chan1.shape != chan2.shape:
        raise ValueError("Input arrays must have the same shape")
    c1_clusters = fit_clusters(chan1, num_clusts)
    c2_clusters = fit_clusters(chan2, num_clusts)

    return compare_dists(c1_clusters, c2_clusters, max_dist)


def annotate(ax, title, coords=False):
    """Adds a circle and/title to a given position in an ICA plot.

    :param ax: Axis to add the circle
    :type ax: matplotlib.pyplot axis object
    :param title: Title to add to the axes
    :type title: string
    :param coords: Coordinates to plot the circle(s)
    :type coords: list of tuples (y, x)
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


def plot(original, denoised, clusters, output_dir, filename):
    """Plots a pair of images, draws ICA cluster markings , and saves the figure.

    :param original: Input image data
    :type original: Numpy array of shape (height x width x channels)
    :param denoised: Denoised image data
    :type denoised: Numpy array of shape (height x width x channels)
    :param clusters: List of cluster coordinates
    :type clusters: List
    :param output_dir: Path to output the result to
    :type output_dir: string
    :param filename: Name to output file as
    :type filename: string
    """

    fig, ax = plt.subplots(1, 2)
    fig.suptitle("Intensity Correlation Analysis")
    ax[0].imshow(original)
    ax[1].imshow(denoised)
    titles = ['Original', 'Denoised']
    for a, axis in enumerate(ax):
        annotate(axis, titles[a], clusters)
    plt.savefig(output_dir+filename)
    plt.close(fig)


def plot_kmeans(original, denoised, clusters, output_dir, filename):
    """Plots a pair of images, draws ICA cluster markings , and saves the figure.

    :param original: Input image data
    :type original: Numpy array of shape (height x width x channels)
    :param denoised: Denoised image data
    :type denoised: Numpy array of shape (height x width x channels)
    :param clusters: List of cluster coordinates
    :type clusters: List
    :param output_dir: Path to output the result to
    :type output_dir: string
    :param filename: Name to output file as
    :type filename: string
    """
    fig, ax = plt.subplots(1, 2)
    fig.suptitle("K-means")
    ax[0].imshow(original)
    ax[1].imshow(denoised)
    titles =['Original','Denoised']
    for a, axis in enumerate(ax):
        if clusters:
            for pair in clusters.keys():
                coords = tuple(clusters[pair]["Centroid"])
                circle = plt.Circle(coords, 5, color='white', fill=False)
                axis.add_artist(circle)
        axis.set_title(titles[a])
        axis.axis("off")

    plt.savefig(output_dir + filename)
    plt.close(fig)


def run_visualiser(input_dict):
    """ Generates ICA and/or K-means plots in response to user-defined inputs

    :param input_dict: User input values
    :type input_dict: dictionary
    """
    # Get parameters from user input

    sourcefile, output_dir = [input_dict[key] for key in ["in_path",
                                                          "out_path"]]
    default_params = {
        'threshold': 0.5,
        'channels': [0, 1],
        'num_clusts': 10,
        'min_dist': 20
    }

    for key in default_params.keys():
        if key not in input_dict.keys():
            input_dict[key] = default_params[key]


    if not os.path.isfile(sourcefile):
        raise KeyError("%s does not exist" % (sourcefile))

    if not os.path.isdir(output_dir):
        raise KeyError("%s does not exist" % (output_dir))
    if (input_dict['threshold']==0) or (input_dict['threshold']==1):
        raise ValueError("Please enter a threshold between (but not including) 0 and 1 ")

    print("=========================================\n",
          "=========================================")
    print("**WELCOME TO THE AUTOMATED COLOCALISATION GUI**\n")
    print("Analysing files from ", sourcefile)
    print("Preprocessing")

    original, preprocessed = do_preprocess(sourcefile,
                                           output_dir,
                                           threshold=input_dict['threshold'])

    # Rescale in range (0, 255)
    original = (original.frames*255).astype(int)
    preprocessed = (preprocessed.frames*255).astype(int)
    print("Complete")
    print("==================================\n")
    print("Running fluorescence colocalisation analysis")
    if (input_dict["Run Intensity Correlation Analysis"] == 'Y') and (input_dict["Run KMeans"] == 'Y'):
        for n in range(original.shape[-1]):
            print("\nProcessing Image %s/%s" % (str(n+1),
                                                str(original.shape[-1])))
        # for n in [3, 8,9]:   # For debugging only
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n]
            print("\tRunning Intensity Correlation Analysis")
            corr_clusts = correlate(denoised, input_dict['channels'],
                                    input_dict['num_clusts'])
            plot(orig, denoised, corr_clusts, output_dir, "/0%s_ICA" % n)
            print("\tSaved")
            print("\tRunning KMeans")

            try:
                kmeans_clusts = get_colocs(denoised,
                                           input_dict['channels'],
                                           input_dict['num_clusts'],
                                           input_dict['min_dist'])
                plot_kmeans(orig, denoised, kmeans_clusts,
                            output_dir, "/0%s_kmeans" % n)
            except ValueError:
                print("\tNo clusters found within",
                      " %s pixels for image %s" % (input_dict['min_dist'],
                                                   str(n)))
                plot_kmeans(orig, denoised, None,
                            output_dir, "/0%s_kmeans" % n)
            print("\tSaved")

    elif (input_dict["Run Intensity Correlation Analysis"] == 'Y') and (input_dict["Run KMeans"] == 'N'):
        for n in range(original.shape[-1]):
            print("\nProcessing Image %s/%s" % (str(n+1),
                                                str(original.shape[-1])))
        # for n in [8,9]:   # For debugging only
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n].astype(int)
            print("\tRunning Intensity Correlation Analysis")
            corr_clusts = correlate(denoised, input_dict['channels'],
                                    input_dict['num_clusts'])
            plot(orig, denoised, corr_clusts, output_dir, "/0%s_ICA" % n)
            print("\tSaved")

    elif (input_dict["Run Intensity Correlation Analysis"] == 'N') and (input_dict["Run KMeans"] == 'Y'):
        for n in range(original.shape[-1]):
            print("\nProcessing Image %s/%s" % (str(n+1),
                                                str(original.shape[-1])))
        # for n in [8,9]:   # For debugging only
            orig = original[:, :, :, n]
            denoised = preprocessed[:, :, :, n]
            print("\tRunning KMeans")
            try:
                kmeans_clusts = get_colocs(denoised,
                                           input_dict['channels'],
                                           input_dict['num_clusts'],
                                           input_dict['min_dist'])
                plot_kmeans(orig, denoised, kmeans_clusts,
                            output_dir, "/0%s_kmeans" % n)
            except ValueError:
                print("\tNo clusters found within",
                      " %s pixels for image %s" % (input_dict['min_dist'],
                                                   str(n)))
                plot_kmeans(orig, denoised, None,
                            output_dir, "/0%s_kmeans" % n)
            print("\tSaved")
    else:
        raise KeyError("Please select a method for colocalisation analysis")
    print("Complete")


if __name__ == "__main__":
    inputdict = {
        'in_path': './data/input/colocsample1bRGB_BG.tif',
        # 'in_path': './data/input/Composite_12156.tif',
        'out_path': './data/output',
        'threshold': 0.5,
        'channels': [0, 1],
        'num_clusts': 10,
        'min_dist': 20,
        'Run Intensity Correlation Analysis': 'Y',
        'Run KMeans': 'Y'}
    # run_visualiser(inputdict)
