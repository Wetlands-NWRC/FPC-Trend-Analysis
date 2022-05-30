data.directory    <- "/home/ryan/work/nwrc/programming/remotes/FPC-Trend-Analysis/testing/data"
code.directory    <- "/home/ryan/work/nwrc/programming/remotes/FPC-Trend-Analysis/source"
output.directory  <- "./VV";

print( data.directory );
print( code.directory );
print( output.directory );

print( format(Sys.time(),"%Y-%m-%d %T %Z") );

start.proc.time <- proc.time();

options(warn = 0)

# set working directory to output directory
# setwd( output.directory );

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
dir.geoson   <- file.path(data.directory,"col_sanitize");
dir.tiffs    <- file.path(data.directory,"img");
dir.parquets <- "parquets-data";
dir.scores   <- "parquets-scores";

target.variable      <- 'VV';
n.harmonics          <- 7;
RData.trained.engine <- 'trained-fpc-FeatureEngine.RData';

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
DF.training <- getData.geojson(
  input.directory = dir.geoson,
  parquet.output  = "DF-training-raw.parquet"
);

DF.training <- sanitize.col.names(
  DF.input = DF.training
);

DF.colour.scheme <- getData.colour.scheme(
  DF.training = DF.training
);