data.directory    <- "P:/programming/remotes/FPC-Trend-Analysis/testing"
code.directory    <- "P:/programming/remotes/FPC-Trend-Analysis/source"
output.directory  <- "P:/programming/remotes/FPC-Trend-Analysis/testing";

print( data.directory );
print( code.directory );
print( output.directory );

print( format(Sys.time(),"%Y-%m-%d %T %Z") );

start.proc.time <- proc.time();

# set working directory to output directory
setwd( output.directory );

##################################################
require(arrow);
require(doParallel);
require(foreach);
require(ggplot2);
#require(ncdf4);
require(openssl);
require(parallel);
require(raster);
require(terra);
require(terrainr);
require(sf);
require(stringr);
require(tidyr);

require(fpcFeatures);

# source supporting R code
code.files <- c(
  'compute-fpc-scores.R',
  'getData-colour-scheme.R',
  'getData-geojson.R',
  'initializePlot.R',
  'plot-RGB-fpc-scores.R',
  'preprocess-training-data.R',
  'tiff2parquet.R',
  'train-fpc-FeatureEngine.R',
  'utils-rgb.R',
  'visualize-fpc-approximations.R',
  'visualize-training-data.R'
);

for ( code.file in code.files ) {
  source(file.path(code.directory,code.file));
}

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
my.seed <- 7654321;
set.seed(my.seed);

is.macOS  <- grepl(x = sessionInfo()[['platform']], pattern = 'apple', ignore.case = TRUE);
n.cores   <- ifelse(test = is.macOS, yes = 2, no = parallel::detectCores() - 1);
cat(paste0("\n# n.cores = ",n.cores,"\n"));

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
#dir.geoson   <- file.path(data.directory,"TrainingData_Geojson");
dir.tiffs    <- file.path(data.directory,"testing_image");
dir.parquets <- "parquets-data";
dir.scores   <- "parquets-scores";

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
tiff2parquet(
  dir.tiffs    = dir.tiffs,
  n.cores      = n.cores,
  dir.parquets = dir.parquets
);
