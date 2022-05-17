moduel <- "source/parquet2tiff.R";
# DIR.DATA <- NULL;
# DIR.OUR  <- NULL;


source(moduel)

dir.parq <- "testing/testing_parq_2_tiff/parquets-scores"
dir.tiff <- "testing/testing_parq_2_tiff/tiff-scores"

parquet2tiff(
  dir.scores.parquet = dir.parq,
  dir.scores.tiff = dir.tiff
)