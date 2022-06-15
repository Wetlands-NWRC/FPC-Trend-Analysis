# FPC-Trend-Analysis
# Installation
Requirements for the fpcFeatures R Package, note this package is not available via CRAN
``` R
> install.packages(pkgs = c("cowplot","dplyr","fda","ggplot2","logger","R6") )
> install.packages(repos = NULL, type = "source", pkgs = "fpcFeatures_0.0.0.0002.tar.gz" )
```
# Configuration Setup
FPC pipeline takes a config.yml file. this file contains all relevant protocls for the pipeline to take.  
Sample file below, note that <strong>landCover</strong> key is optional
``` YAML
dataDir: ./path/to/the/parent/data/dir
trainingDir: ./child/dir/to/training/data
imagesDir: ./child/of/datadir/points/to/images
targetVariable: channel you want to target for analysis
landCover:
    - landCover1
    - landCover2
```

# Project Setup
```
FPC-SITE
|   
|   
|___000-data
|       img
|       training_data
|
|___VV
|       config.yml
|       run.py
|
|___VH
|       config.py
|       run.py
```