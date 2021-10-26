# File to test the new pipeline.
from classes import pipeline_object

testimg = pipeline_object('./data/input/colocsample1bRGB_BG.tif', 
                          'test.tif', threshold=0.3)
testimg.split()
testimg.rescale_all()
testimg.visualise()

