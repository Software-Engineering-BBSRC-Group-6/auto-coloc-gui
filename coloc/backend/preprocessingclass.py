# File to test the new pipeline.
# from ..backend.classes import pipeline_object
try:
    from backend.classes import pipeline_object
except ModuleNotFoundError:
    from ..backend.classes import pipeline_object


def do_preprocess(sourcefile, outpath, threshold=False, visualise=False):
    pipeline_full = pipeline_object(sourcefile, outpath, threshold)
    pipeline_original = pipeline_object(sourcefile,
                                        outpath, threshold=False)

    #pipeline_full.split()
    #pipeline_original.split()

    pipeline_full.reshape()
    pipeline_original.reshape()
    pipeline_full.normalise_all()
    pipeline_original.normalise_all()
    if visualise:
        pipeline_full.visualise()

    return pipeline_original, pipeline_full
