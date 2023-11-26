# Analysis of log2 fold change RNAseq files from Mariya's experiment

To use the code in this repository, you need the RNAseq log2 fold change data files from Mariya's 250 day time series experiment. Shishir got these files from Mariya via Dropbox. Not sure where they are on the official data servers, might be in cold storage.

The analysis code is in the following files:

```
01_clean_data.py
02_time_progression_linecharts.ipynb
03_run_all_gsea.sh
04_gsea_results.ipynb
05_recreate_bar_charts.ipynb
```

They should be run in numerical order, and will produce various output directories and files that will be used by subsequent analysis code.

The file `01_clean_data.py` needs the path to the data folder from Mariya. See the comment on line 6 of the file for the format of how to pass the path when you run the file.

The file `03_run_all_gsea.sh` needs to be passed the path to the `gsea-cli.sh` executable that is bundled with the GSEA software package. More info on lines 3 and 5 of the file.

## Output files locations

The final outputs of the analysis are the lists of genes in the `output_gene_lists` directory, and the HTML charts in the `output_charts` directory.

## Getting final output charts as SVGs

The HTML charts can be exported to SVG by opening them in a web browser, clicking the circle with the 3 dots in the top right corner, and then clicking the "Save as SVG" button.
