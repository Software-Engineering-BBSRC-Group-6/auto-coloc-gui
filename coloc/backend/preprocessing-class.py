# File to test the new pipeline.
from classes import pipeline_object

testimg = pipeline_object('./data/input/colocsample1bRGB_BG.tif', 
                          'test.tif', threshold=0.05)
testimg.split()
testimg.reshape()
testimg.normalise_all()
testimg.visualise()

