#' Sanitizes Dataframe columns; standardize them for FPC analysis
#' 
sanitize.col.names <- function(
    DF.training = NULL
    ) {
    thisFunctionName <- "sanitize.col.names";

    cat("\n### ~~~~~~~~~~~~~~~~~~~~ ###");
    cat(paste0("\n# ",thisFunctionName,"() starts.\n"));

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
    colnames(DF.training) <- tolower(colnames(DF.training));
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^class$",   replacement = "land_cover");
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^cdesc$",   replacement = "land_cover");
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^point_x$", replacement =  "longitude");    
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^point_y$", replacement =   "latitude");
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^lon$",     replacement =  "longitude");
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^lat$",     replacement =   "latitude");
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^x$",       replacement =  "longitude")
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^y$",       replacement =   "latitude");
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^vv$",      replacement =         "VV");
    colnames(DF.training) <- gsub(x = colnames(DF.training), pattern = "^vh$",      replacement =         "VH");

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
    cat(paste0("\n# ",thisFunctionName,"() exits."));
    cat("\n### ~~~~~~~~~~~~~~~~~~~~ ###\n");
    return(DF.training)
}