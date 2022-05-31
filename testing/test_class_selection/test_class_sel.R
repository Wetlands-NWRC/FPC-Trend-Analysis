file.yaml <- "/home/ryan/work/nwrc/programming/remotes/FPC-Trend-Analysis/testing/test_class_selection/config.yml"
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
  'query.R',
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
select.land.cover    <- config.list$landCover
n.harmonics          <- 7;
RData.trained.engine <- 'trained-fpc-FeatureEngine.RData';


print( data.directory );
print( code.directory );


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
DF.training <- getData.geojson(
  input.directory = dir.geoson,
  parquet.output  = "DF-training-raw.parquet"
);

DF.training <- sanitize.col.names(
  DF.input = DF.training
);

DF.training <- select.landcover(
  DF.input   = DF.training,
  land.cover = select.land.cover
)

DF.colour.scheme <- getData.colour.scheme(
  DF.training = DF.training
);

DF.training <- preprocess.training.data(
  DF.input         = DF.training,
  DF.colour.scheme = DF.colour.scheme
);


cat("\nstr(DF.colour.scheme)\n");
print( str(DF.colour.scheme)   );


arrow::write_parquet(
  sink = "DF-training.parquet",
  x    = DF.training
);

cat("\nstr(DF.training)\n");
print( str(DF.training)   );
