
# command.arguments <- commandArgs(trailingOnly = TRUE);
# data.directory    <- normalizePath(command.arguments[1]);
# code.directory    <- normalizePath(command.arguments[2]);
# output.directory  <- normalizePath(command.arguments[3]);

setwd(getwd())

### DEBUG ###
data.directory <- "./000-data/training_data"
code.directory <- "./output/code"
output.directory <- "./output/"
### ~~~ ###
  
  
print( data.directory );
print( code.directory );
print( output.directory );

print( format(Sys.time(),"%Y-%m-%d %T %Z") );

start.proc.time <- proc.time();


##################################################
require(arrow);
require(doParallel);
require(foreach);
require(ggplot2);
require(ncdf4);
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


# set working directory to output directory
# setwd( output.directory );

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
my.seed <- 7654321;
set.seed(my.seed);

is.macOS  <- grepl(x = sessionInfo()[['platform']], pattern = 'apple', ignore.case = TRUE);
n.cores   <- ifelse(test = is.macOS, yes = 2, no = parallel::detectCores() - 1);
cat(paste0("\n# n.cores = ",n.cores,"\n"));

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

target.variables      <- c('VV', 'VH');
n.harmonics          <- 7;
RData.trained.engine <- 'trained-fpc-FeatureEngine.RData';


file.parquet <- "./000-data/training_data/data-labelled-2020.parquet"
DF.training <- arrow::read_parquet(file = file.parquet)
DF.training <- base::data.frame(DF.training)
DF.training$date <- as.Date(DF.training$date)

cat("\nstr(DF.training)\n");
print( str(DF.training)   );

DF.colour.scheme <- getData.colour.scheme(
    DF.training = DF.training
    );

cat("\nstr(DF.colour.scheme)\n");
print( str(DF.colour.scheme)   );
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
visualize.training.data(
    DF.training      = DF.training,
    colname.pattern  = "(VV|VH)",
    DF.colour.scheme = DF.colour.scheme,
    output.directory = "plot-training-data"
    );
gc();

for (target.variable in target.variables) {
    RData.trained.engine.var <- paste0(target.variable, "-", RData.trained.engine)
    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
    trained.fpc.FeatureEngine <- train.fpc.FeatureEngine(
        DF.training      = DF.training,
        x                = 'x',
        y                = 'y',
        land.cover       = 'land_cover',
        date             = 'date',
        variable         = target.variable,
        min.date         = NULL,
        max.date         = NULL,
        n.harmonics      = n.harmonics,
        DF.colour.scheme = DF.colour.scheme,
        RData.output     = RData.trained.engine.var
        );
    gc();
    print( str(trained.fpc.FeatureEngine) );

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
    visualize.fpc.approximations(
        featureEngine    = trained.fpc.FeatureEngine,
        DF.variable      = DF.training,
        location         = 'y_x',
        date             = 'date',
        land.cover       = 'land_cover',
        variable         = target.variable,
        n.locations      = 10,
        DF.colour.scheme = DF.colour.scheme,
        my.seed          = my.seed,
        output.directory = "plot-fpc-approximations"
        );
}


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

##################################################
print( warnings() );

print( getOption('repos') );

print( .libPaths() );

print( sessionInfo() );

print( format(Sys.time(),"%Y-%m-%d %T %Z") );

stop.proc.time <- proc.time();
print( stop.proc.time - start.proc.time );
