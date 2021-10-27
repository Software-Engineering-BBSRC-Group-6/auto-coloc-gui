import pytest
from ..backend import Visualiser
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from ..backend.preprocessingclass import do_preprocess

def test_annotate_title():
    _, ax = plt.subplots(1, 1)
    title = 'Hello'
    Visualiser.annotate(ax, title)
    assert ax.get_title(loc='center') == title

@pytest.mark.parametrize('test',
    [((20, 20),),
     ((30, 50),),
     ((3, 3),),   # Should this still pass for radius 5?
     ]
)
def test_annotate_circle(test):
    _, ax = plt.subplots(1, 1)
    Visualiser.annotate(ax, 'Hello', coords=test)
    assert ax.get_lines

# An unfinished test to deal with correlate.
"""
def test_correlate():
    sourcefile = './data/input/colocsample1bRGB_BG.tif'
    orig, pre = do_preprocess(sourcefile, 0.2, visualise=False)
    random.seed(1)
    rnd_frame = random.randrange(pre.frames.shape[-1])
    orig = orig.frames.astype(int)[:, :, :, rnd_frame]
    pre = pre.frames[:, :, :, rnd_frame]
    corr_clusts, _ = correlate(orig, denoised,
                               3,
                               10)
                               """