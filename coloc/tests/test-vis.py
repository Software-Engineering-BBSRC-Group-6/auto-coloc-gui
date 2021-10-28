import pytest

# Tests for visualiser.py

def test_correlate():
    # If 1 cluster is passed, the output array should have length 1
    # If one array is all zeros, the output should have no clusters
    # If the arrays are the same, an error should be raised


def test_fit_clusters():
    # If 1 cluster is passed, the output array should have length <=1
    # If no pixels are zeroed out, an error should be thrown
    # (thresholding is not working )

def test_compare_dists():
    # If cluster lists are of unequal lengths, should raise an error
    # Centroid distance between clusters at (1,1) and (2,2) should be root(2)
    # Centroid distance between clusters at (1,1) and (1,1) should be zero
    # the output centroid between two clusters at (1,1) and (2,2) should be (2,2) as int

def test_get_colocs():
    # If 0 or 3 channels fed to the function, it should raise a value error
    # If arrays of different types are passed to the function, it should raise a value error
    # Passing an input with num_clusts =1 should return a dictionary with <= 1 pair

def test_run_visualiser():
    testdict = {
    'in_path': './data/input/colocsample1bRGB_BG.tif',
    # 'in_path': './data/input/Composite_12156.tif',
    'out_path': './data/output',
    'threshold': 0.5,
    'channels': [0, 1],
    'num_clusts': 10,
    'min_dist': 20,
    'Run Intensity Correlation Analysis': 'Y',
    'Run KMeans': 'Y'}