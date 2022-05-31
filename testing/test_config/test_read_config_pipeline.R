setwd("/home/ryan/work/nwrc/programming/remotes/FPC-Trend-Analysis/testing/test_config")

file.yaml <- "./config.yml"
code.directory    <- "/home/ryan/work/nwrc/programming/remotes/FPC-Trend-Analysis/source"

print( format(Sys.time(),"%Y-%m-%d %T %Z") );

start.proc.time <- proc.time();

##################################################
require(arrow);
require(doParallel);
require(foreach);
require(ggplot2);
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
  'parquet2tiff.R',
  'plot-RGB-fpc-scores.R',
  'preprocess-training-data.R',
  'sanitize.R',
  'setup.R',
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
config.list <- setup.workspace(
  config = file.yaml
)

data.directory    <- config.list$dataDir

dir.geoson   <- file.path(data.directory, config.list$trainingDataDir);
dir.tiffs    <- file.path(data.directory, config.list$imagesDir);
dir.parquets <- "parquets-data";
dir.scores   <- "parquets-scores";

target.variable      <- config.list$targetVariable;
n.harmonics          <- 7;
RData.trained.engine <- 'trained-fpc-FeatureEngine.RData';


print( code.directory );
print( data.directory );
print(dir.geoson);
print(dir.tiffs)
print(target.variable)


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###