[![Python Version Compatability and Flake-8](https://github.com/Software-Engineering-BBSRC-Group-6/auto-coloc-gui/actions/workflows/python-version.yml/badge.svg)](https://github.com/Software-Engineering-BBSRC-Group-6/auto-coloc-gui/actions/workflows/python-version.yml)
[![Check Systems Compatability](https://github.com/Software-Engineering-BBSRC-Group-6/auto-coloc-gui/actions/workflows/system-compatability.yml/badge.svg)](https://github.com/Software-Engineering-BBSRC-Group-6/auto-coloc-gui/actions/workflows/system-compatability.yml)
[![codecov](https://codecov.io/gh/Software-Engineering-BBSRC-Group-6/auto-coloc-gui/branch/main/graph/badge.svg?token=0jS0kYRsze)](https://codecov.io/gh/Software-Engineering-BBSRC-Group-6/auto-coloc-gui)
[![Documentation Status](https://readthedocs.org/projects/auto-coloc-gui/badge/?version=main)](https://auto-coloc-gui.readthedocs.io/en/main/?badge=main)

# ACG Tools - auto-coloc-gui

<p align="center">
  <img src="coloc/gui/acg_logo.png" alt="ACG Tools Logo"/>
</p>

> Filtering the noise in immunohistochemistry analysis

An open source desktop image processing tool written in Python to automate the analysis of multichannel flourescence images to quantify colocalisation available on Windows, Mac OS and Debian Linux.

[ReadTheDocs detailed documentation](https://auto-coloc-gui.readthedocs.io/en/main/)


## Authors

Amit Halkhoree - amit.halkhoree@dtc.ox.ac.uk \
Cameron Anderson - cameron.anderson@dtc.ox.ac.uk \
Dan Hudson - alexander.hudson@dtc.ox.ac.uk \
Ishaan Kapoor - ishaan.kapoor@dtc.ox.ac.uk \
Joseph Pollacco - joseph.pollacco@dtc.ox.ac.uk \
Samuel Johnson - samuel.johnson@dtc.ox.ac.uk
# User Guide
The tool accepts .TIFF formatted images with two or more colour channels and uses a statistical model to indicate regions of interest (ROIs) where flourophores colocalise. The tool comes with a user friendly interface which allows users to customise thresholds and distances across which colocolisation could be calculated. This tool serves to be a python based alternative to [ImageJ](https://imagej.nih.gov/ij/) and the [EzColocalization plugin](https://www.nature.com/articles/s41598-018-33592-8).

## Installation
Please find the appropriate installation executable for your operating system within the dist folder. As of release, the software has been validated to work on (as per systems compatibility testing):
* Windows 10
* MacOS Monterey 
* Debian Linux Ubuntu LTS 20.04.3
## Usage
1) Select a .TIFF image stack to be processed
- A .TIFF stack is a collection of images stored within one file, and often contains images across a Z axis
- The output will be generated in an output folder in the same location as the .TIFF file so please ensure that there is enough diskspace to do so.
2) Define the desired `threshold` between 0.1 and 0.9 
- Threshold refers to the degree pixel noise filtering
3) Select the number of `channels` in the image (1, 2, or 3).
- Channels indicates how many colour spaces from the RGB spectrum are available. For example, cells stained with GFP and Texas Red would require 2 channels. 
4) Select the `scale` of the images between 1μM and 500μM.
5) Define the desired number of `clusters` between 10 and 50.
- Determines the number of colocalisations detected.
6) Specify the `type of analysis` - Intensity correlation analysis (based on fluoresence correlation) OR [Kmeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) analysis (groups datapoints which are similar).
7) Press `run` - model run time can vary based on local resources.
8) Click on the `view` tab to view the original and denoised image side by side.
9) Use the `Next` and `Previous` buttons to move between the generated images.

# Background

In molecular and cellular biology, colocalisation refers to the spatial arrangement of individual molecules such that two or more molecules are clustered in the same biological subdomains. The most common way of testing this is through flourescence microscopy, where different moleules are tagged using flourophores with differing emission spectra. Images are then processed and flourescence across channels is assessed for co-occurance or correlation. While correlation is a statistical measured, usually using Pearson and Spearman coefficients, co-occurance reports the overlap of the flourophores within a region of interest. 

[Reference](https://en.wikipedia.org/wiki/Colocalization)

[Aaron et al., 2018](doi:10.1242/jcs.211847), present a good review on the topics of correlation vs co-occurance, explaining which method should be preferred in certain biological settings. 


![4 panel image displaying colocalisation of different proteins using different flourophores](https://iiif.elifesciences.org/lax/22904%2Felife-22904-fig4-v2.tif/full/1500,/0/default.jpg) 
(Adapted from Genc et al., 2017)

# Software overview

## Rationale
This software aims to reduce user error when evaluating flourophore colocalisation by determining colocalisation algorithmically, rather than by eye. This should reduce user bias and increase experimental reproducibility. 

## Principal components
The program consists of a frontend graphical user interface (gui.py) which handles user input as well as results output and a backend pipeline of preprocessing (preprocessing.py) and visualisation (visualiser.py).

## Folder structure
This repository contains the following key files and folders:
* .github/workflows: directory of github actions ensuring continuous integration (CI) of repository updates
* coloc: directory for main executables
    * backend
        * preprocessing.py: data processing prior to model computation
        * preprocessingclass.py: helper tests for preprocessing.py
        * visualiser.py: model construction and visualisation
    * gui
        * gui.py: graphical user interface constructed using the PyQT5 framework
    * tests: contains unit tests for CI
* data: directory for data input and output
* dist: executable installers wil be found here
* docs: files required for automated document production
* venv: virtual environment configuration including the dependencies for this software
* .gitignore: file controlling which files are/are not updated by git during development
* requirements.txt: Dependencies required for proper package functioning
* setup: allows for setup via requirements.txt


## Issues and futher development

If you find a bug in the software or an unexpected behaviour when using ACG Tools, please open an issue describing the bug and include a minimum reproducible example. 
