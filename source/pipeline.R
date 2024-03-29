command.arguments <- commandArgs(trailingOnly = TRUE);
code.directory    <- normalizePath(command.arguments[1])
output.directory  <- normalizePath(command.arguments[2])
config.file       <- normalizePath(command.arguments[3])


setwd(output.directory)
print(getwd())
print( code.directory );
print( output.directory );
print(config.file )

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
  'scale-data.R',
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
  config = config.file
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
data.normalize       <- config.list$normalize


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
DF.training <- getData.geojson(
  input.directory = dir.geoson,
  parquet.output  = "DF-training-raw.parquet"
);

DF.training <- sanitize.col.names(
  DF.input = DF.training
);

DF.training <- query.landcover(
  DF.input   = DF.training,
  land.cover = select.land.cover
)

DF.colour.scheme <- getData.colour.scheme.json(
  DF.training = DF.training,
  colours.json = file.path(data.directory, 'colours.json')
);

DF.training <- preprocess.training.data(
  DF.input         = DF.training,
  DF.colour.scheme = DF.colour.scheme
);

DF.training <- reshapeData_attachScaledVariable(
    DF.input = DF.training,
    target.variable = target.variable,
    by.variable = "X_Y_year"
)

if(data.normalize){
    target.variable <- paste0(target.variable, '_scaled')
}

cat("\nstr(DF.colour.scheme)\n");
print( str(DF.colour.scheme)   );


arrow::write_parquet(
  sink = "DF-training.parquet",
  x    = DF.training
);

cat("\nstr(DF.training)\n");
print( str(DF.training)   );

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
visualize.training.data(
  DF.training      = DF.training,
  colname.pattern  = target.variable,
  DF.colour.scheme = DF.colour.scheme,
  output.directory = "plot-training-data"
);
gc();

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
trained.fpc.FeatureEngine <- train.fpc.FeatureEngine(
  DF.training      = DF.training,
  x                = 'longitude',
  y                = 'latitude',
  land.cover       = 'land_cover',
  date             = 'date',
  variable         = target.variable,
  min.date         = NULL,
  max.date         = NULL,
  n.harmonics      = n.harmonics,
  DF.colour.scheme = DF.colour.scheme,
  RData.output     = RData.trained.engine
);
gc();
print( str(trained.fpc.FeatureEngine) );

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
DF.training[,"latitude_longitude"] <- apply(
  X      = DF.training[,c("latitude","longitude")],
  MARGIN = 1,
  FUN    = function(x) { return(paste(x = x, collapse = "_")) }
);

visualize.fpc.approximations(
  featureEngine    = trained.fpc.FeatureEngine,
  DF.variable      = DF.training,
  location         = 'latitude_longitude',
  date             = 'date',
  land.cover       = 'land_cover',
  variable         = target.variable,
  n.locations      = 10,
  DF.colour.scheme = DF.colour.scheme,
  my.seed          = my.seed,
  output.directory = "plot-fpc-approximations"
);

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
tiff2parquet(
  dir.tiffs    = dir.tiffs,
  n.cores      = n.cores,
  dir.parquets = dir.parquets,
);

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
compute.fpc.scores(
  x                    = 'x',
  y                    = 'y',
  date                 = 'date',
  variable             = target.variable,
  RData.trained.engine = RData.trained.engine,
  dir.parquets         = dir.parquets,
  n.cores              = n.cores,
  dir.scores           = dir.scores
);
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
parquet2tiff()

##################################################
print( warnings() );

print( getOption('repos') );

print( .libPaths() );

print( sessionInfo() );

print( format(Sys.time(),"%Y-%m-%d %T %Z") );

stop.proc.time <- proc.time();
print( stop.proc.time - start.proc.time );
