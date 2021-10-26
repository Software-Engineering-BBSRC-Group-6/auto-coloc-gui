# auto-coloc-gui

An image processing tool to automoate the analysis of multichannel flourescence images to quantify colocalisation. The tool accepts .TIFF formatted images with two or more colour channels and uses a statistical model to indicate regions of interest (ROIs) where flourophores colocalise. The tool comes with a user friendly interface which allows users to customise thresholds and distances across which colocolisation could be calculated.

https://software-engineering-bbsrc-group-6.github.io/auto-coloc-gui/

# Authors

Amit Halkhoree - amit.halkhoree@dtc.ox.ac.uk \
Cameron Anderson - cameron.anderson@dtc.ox.ac.uk \
Dan Hudson - alexander.hudson@dtc.ox.ac.uk \
Ishaan Kapoor - ishaan.kapoor@dtc.ox.ac.uk \
Joseph Pollacco - joseph.pollacco@dtc.ox.ac.uk \
Samuel Johnson - samuel.johnson@dtc.ox.ac.uk

# Background
Ref: https://en.wikipedia.org/wiki/Colocalization

In molecular and cellular biology, colocalisation refers to the spatial arrangement of individual molecules such that two or more molecules are clustered in the same biological subdomains. The most common way of testing this is through flourescence microscopy, where different moleules are tagged using flourophores with differing emission spectra. Images are then processed and flourescence across channels is assessed for co-occurance or correlation. While correlation is a statistical measured, usually using Pearson and Spearman coefficients, co-occurance reports the overlap of the flourophores within a region of interest. 

Aaron et al., 2018 (doi:10.1242/jcs.211847), present a good review on the topics of correlation vs co-occurance, explaining which method should be preferred in certain biological settings. 


![alt text](https://iiif.elifesciences.org/lax/22904%2Felife-22904-fig4-v2.tif/full/1500,/0/default.jpg) 
(Adapted from Genc et al., 2017)