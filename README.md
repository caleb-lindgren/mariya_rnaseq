# Analysis of log2 fold change RNAseq files from Mariya's experiment

The analysis code is in the following files:

```
01_clean_data.py
02_time_progression_linecharts.ipynb
03_run_all_gsea.sh*
04_gsea_results.ipynb
05_recreate_bar_charts.ipynb
```

They should be run in numerical order, and will produce various output directories and files that will be used by subsequent analysis code.

## Getting final output charts as SVG

The final outputs of the analysis are the lists of genes in the `final_output_gene_lists` directory, and the HTML charts in the `final_output_charts` directory. The HTML charts can be exported to SVG by opening them in a web browser, clicking the circle with the 3 dots in the top right corner, and then clicking the "Save as SVG" button.

## Explanation of other directories

Here is an explanation of the other directories in this repository.

- data/
    - This contains the original log2 fold change RNAseq files from Mariya. Shishir got them from her via Dropbox. Not sure where they are on the official data servers, might be in cold storage.
- gmts/
    - GMT (Gene Matrix Transposed) files used for gene set enrichment analysis (GSEA). Downloaded from [https://www.gsea-msigdb.org/gsea/msigdb/human/collections.jsp]
- gsea_res/
    - Results produced by the GSEA software
- rnks/
    - Input files for GSEA, generated from the original log2 fold change RNAseq files by the `01_clean_data.py` script.

