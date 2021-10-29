import pytest
import numpy as np
import matplotlib.pyplot as plt
try:
    from ..backend.Visualiser import correlate, fit_clusters, run_visualiser, annotate, scaled_dist, compare_dists
except ModuleNotFoundError:
    from backend.Visualiser import correlate, fit_clusters, run_visualiser, annotate, scaled_dist, compare_dists


# Tests for visualiser.py


class Vistest():
    def __init__(self):
        self.rand1= np.random.randint(0, 255, size=(150, 150, 2))
        np.random.seed(0)
        self.rand2= np.random.randint(0, 255, size=(150, 150))
        self.im = np.asarray(np.dstack([self.rand2, self.rand2]))
        self.channels=[0, 1]
        self.testdict = {'in_path': './data/input/colocsample1bRGB_BG.tif',
                        'out_path': './data/output',
                        'threshold': 0.5,
                        'channels': [0, 1],
                        'num_clusts': 10,
                        'min_dist': 20,
                        'Run Intensity Correlation Analysis': 'Y',
                        'Run KMeans': 'Y'}

    def test_correlate(self):

        # If 1 cluster is passed, the output array should have length 1

        assert len(correlate(self.rand1, self.channels, 1)) == 1
        
        # If the arrays are the same, an error should be raised

        with pytest.raises(ValueError):
            correlate(self.im, self.channels, 1)

    def test_fit_clusters(self):

        # If 1 cluster is passed, the output array should have length <=1

        assert len(fit_clusters(self.rand2, 1)) == 1

        # If no pixels are zeroed out, an error should be thrown
        # (thresholding is not working )
        with pytest.raises(ValueError):
            fit_clusters(np.ones(np.shape(self.rand2)),1)
    
    def test_compare_dists(self):
        clust1 = [(1,1),(10,10),(20,20),(40,40)]
        clust2 = [(1,1),(10,10),(20,20)]

        with pytest.raises(ValueError):
            compare_dists(clust1, clust2, 5)

        
    
    def test_run_visualiser(self):

    # If source file does not exist, raise error
        tdict=self.testdict.copy()
        tdict['in_path'] = "testfileXXX"
        with pytest.raises(KeyError):
            run_visualiser(tdict)

    # If outpath does not exist, raise error
        tdict2=self.testdict.copy()
        tdict2['out_path'] = "testdirectoryXXX"
        with pytest.raises(KeyError):
            run_visualiser(tdict2)

        tdict3=self.testdict.copy()
        tdict3['threshold']=1
        with pytest.raises(ValueError):
            run_visualiser(tdict3)
        
        tdict4=self.testdict.copy()
        tdict4['channels']=[0,1,2]
        with pytest.raises(ValueError):
            run_visualiser(tdict4)
        
        tdict5=self.testdict.copy()
        tdict5['Run Intensity Correlation Analysis']= 'N'
        tdict5['Run KMeans']= 'N'
        with pytest.raises(KeyError):
            run_visualiser(tdict5)


def test_annotate_title():
    _, ax = plt.subplots(1, 1)
    title = 'Hello'
    annotate(ax, title)
    assert ax.get_title(loc='center') == title

@pytest.mark.parametrize('test',
    [((20, 20),),
     ((30, 50),),
     ((3, 3),),   # Should this still pass for radius 5?
     ]
)
def test_annotate_circle(test):
    _, ax = plt.subplots(1, 1)
    annotate(ax, 'Hello', coords=test)
    assert ax.get_lines

@pytest.mark.parametrize('test, expected',
    [(51,50),
     (0.5, 1),
     (15.1, 15)
     ]
)
def test_scale_dist(test, expected):
    pix_dist = 1
    assert scaled_dist(test) == expected


vis = Vistest()
vis.test_correlate()
vis.test_fit_clusters()
vis.test_compare_dists()
vis.test_run_visualiser()


