reshapeData_attachScaledVariable <- function(
    DF.input        = NULL,
    target.variable = NULL,
    by.variable     = NULL
    ) {


    require(dplyr);

    my.formula <- as.formula(paste0(target.variable," ~ ",by.variable));

    DF.means <- aggregate(formula = my.formula, data = DF.input, FUN = mean);
    colnames(DF.means) <- gsub(
        x           = colnames(DF.means),
        pattern     = target.variable,
        replacement = "mean_target"
        );

    DF.sds <- aggregate(formula = my.formula, data = DF.input, FUN = sd  );
    colnames(DF.sds) <- gsub(
        x           = colnames(DF.sds),
        pattern     = target.variable,
        replacement = "sd_target"
        );

    DF.output <- dplyr::left_join(
        x  = DF.input,
        y  = DF.means,
        by = by.variable
        );

    DF.output <- dplyr::left_join(
        x  = DF.output,
        y  = DF.sds,
        by = by.variable
        );

    DF.output <- as.data.frame(DF.output);

    DF.output[,"scaled_variable"] <- DF.output[, target.variable ] - DF.output[,"mean_target"];
    DF.output[,"scaled_variable"] <- DF.output[,"scaled_variable"] / DF.output[,  "sd_target"];

    colnames(DF.output) <- gsub(
        x           = colnames(DF.output),
        pattern     = "scaled_variable",
        replacement = paste0(target.variable,"_scaled")
        );

    DF.output <- DF.output[,setdiff(colnames(DF.output),c("mean_target","sd_target"))];

    return( DF.output );

}