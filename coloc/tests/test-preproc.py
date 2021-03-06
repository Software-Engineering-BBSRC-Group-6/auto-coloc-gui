import pytest
from ..backend.classes import pipeline_object
import os
import random
import numpy as np

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


#test_array = np.zeros((2, 2, 3, 1))

@pytest.mark.parametrize('test, raises',
   [(np.empty((2, 2, 3, 2, 2)), ValueError),
    (np.zeros((2, 2, 3, 2)), None)
   ]
)
def test_pipeline_normalise_errors(test, raises):
    """Tests that the normalisation handles various cases properly."""
    test_obj = pipeline_object(correctpath, filepath)
    test_obj.frames = test
    
    if raises:
        with pytest.raises(raises):
            test_obj.normalise_all()
    else:
        test_obj.normalise_all()
        np.testing.assert_array_equal(test_obj.frames, test)

def test_pipeline_visualise(mocker):
    """Tests that the correct number of plots are produced"""

    mocker.patch('matplotlib.pyplot.show', return_value=True)
    mocker.patch('matplotlib.pyplot.imshow', return_value=True)
    mocker.patch('matplotlib.pyplot.colorbar', return_value=True)
    mocker.patch('matplotlib.pyplot.title', return_value=True)
    test_obj = pipeline_object(correctpath, filepath)
    test_obj.visualise()
    # for patched in mocker.patch:
    #     patched.assert_called()

 
