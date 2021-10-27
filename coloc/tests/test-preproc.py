import pytest
from ..backend.classes import pipeline_object
import os
from PIL import Image
import random
import numpy as np
import matplotlib.pyplot as plt

filepath = './coloc/tests/test-data/'
correctname = 'colocsample1bRGB_BG.tif'
correctpath = filepath + correctname

@pytest.mark.parametrize('test, raises',
    [(correctpath, None),
     (filepath + 'idontexist.tif', ValueError),
     (filepath + 'colocsample1bRGB_BG.tiff', ValueError)
    ]
)
def test_pipeline_filepath(test, raises):
    """Tests that a pipeline object is created with correct path."""
    if raises:
        pytest.raises(raises, pipeline_object, test, './coloc/tests/test-data/')
    else:
        assert pipeline_object(test,
                               './coloc/tests/test-data/').filepath == test


@pytest.mark.parametrize('test, raises',
                         [(False, None),
                          ('iamnotafloat', TypeError),
                          (0.3, None)
                          ]
)
def test_pipeline_threshold(test, raises):
    """Tests that no invalid types can enter as a threshold."""
    if raises:
        pytest.raises(raises, pipeline_object,
                      correctpath,
                      filepath,
                      test)
    else:
        assert pipeline_object(correctpath,
                               filepath,
                               test).threshold == test

@pytest.mark.parametrize('test',
    [
        ([correctpath, 0.1]),
        ([correctpath, 0.5]),
    ]
)
def test_pipeline_creation(test):
    """Tests that a pipeline object can be created successfully."""
    test_obj = pipeline_object(test[0], os.path.dirname(os.path.abspath(test[0])), test[1])
    assert test_obj.filepath == test[0]
    assert test_obj.outpath == os.path.abspath(os.path.dirname(test[0]))
    assert test_obj.threshold == test[1]


@pytest.mark.parametrize('test',
    [[correctpath, filepath], 
     ]
)
def test_pipeline_split(test):
    """Tests that the pipeline split method works properly."""
    test_obj = pipeline_object(test[0], test[1])
    test_obj.split()
    assert test_obj.frames.shape[-1] == test_obj.num_frames

@pytest.mark.parametrize('test',
    [[correctpath, filepath, 0.01], 
     [correctpath, filepath, False],
    ]
)
def test_pipeline_normalise(test):
    """Tests that the pipeline noramlisation method works properly."""
    test_obj = pipeline_object(test[0], test[1], test[2])
    test_obj.split()
    n_channels = test_obj.frames.shape[2]
    n_frames = test_obj.frames.shape[3]
    random.seed(1)
    rnd_channel = random.randrange(n_channels)
    imgcheck = test_obj.frames[:, :, rnd_channel, :]
    if not imgcheck.all() == 0:
        imgcheck = (imgcheck-imgcheck.min())/(imgcheck.max()-imgcheck.min())
        if test[2]:
            trim = imgcheck < test[2]
            imgcheck[trim] = 0

    test_obj.normalise(rnd_channel)
    np.testing.assert_array_equal(imgcheck,
                                 test_obj.frames[:, :, rnd_channel, :])


# def test_pipeline_visualise(mocker):
#    """Tests that the correct number of plots are produced."""
#    calls = [0, 0, 0, 0]
#   
#    mocker.patch('matplotlib.pyplot.show', return_value=True)
#    mocker.patch('matplotlib.pyplot.imshow', return_value=True)
#    mocker.patch('matplotlib.pyplot.colorbar', return_value=True)
#    mocker.patch('matplotlib.pyplot.title', return_value=True)
#    test_obj = pipeline_object(correctpath, filepath)
#    test_obj.split()
#    test_obj.visualise()
    
