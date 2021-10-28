import preprocessingclass

input_dict = {
    # 'in_path': './data/input/colocsample1bRGB_BG.tif',
    'in_path': './data/input/Composite_12156.tif',       # Other .tif files not working, need to check array shape/preprocessed is consistent
    'out_path': './data/output',
    'threshold': 0.5,
    'channels': [0,1],
    'num_clusts': 5,
    'min_dist': 20,
    'Run Intensity Correlation Analysis': 'Y',
    'Run KMeans': 'Y'}



orig1, proc1 = preprocessingclass.do_preprocess(input_dict['in_path'], input_dict['out_path'],threshold=input_dict['threshold'])
orig2, proc2 = preprocessingclass.do_preprocess('./data/input/colocsample1bRGB_BG.tif', input_dict['out_path'], threshold=input_dict['threshold'])


print('I am here to haunt you')
