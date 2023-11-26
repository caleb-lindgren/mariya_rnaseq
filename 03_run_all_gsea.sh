#!/bin/bash

# Usage: ./03_run_all_gsea.sh PATH/TO/GSEA/CLI/EXECUTABLE/CALLED/gsea-cli.sh

# GSEA is installable from <https://www.gsea-msigdb.org/gsea/downloads.jsp>, and the gsea-cli.sh executable will be in the installation directory

# FYI: If you previously have run this script, this script will move the results from the previous run to a different directory in the same location with the name "old_gsea_res_moved_" plus a timestamp.

# Make directory for results within the intermediate files directory
idir=intermediate_files
resdir=$idir/gsea_res

# Handle old output files
if [ -d $resdir ]; then
    mv $resdir $idir/old_gsea_res_moved_$(date -d "today" +"%Y%m%d%H%M")
fi

mkdir $resdir

# Run GSEA Prerank with each of the different GMT files
# GMT files are lists of gene sets to run GSEA with. These ones were downloaded from the GSEA website.
for gmt in $idir/gmts/*; do
    gmtname=$(basename -- $gmt)
    gmtresdir=$resdir/$gmtname
    mkdir $gmtresdir

    # For each GMT file, run GSEA on the individual ranking file for each day
    for rnk in $idir/rnks/*; do
        rnkname=$(basename -- $rnk)
        $1 GSEAPreranked -gmx $gmt -collapse No_Collapse -mode Abs_max_of_probes -norm meandiv -nperm 1000 -rnd_seed timestamp -rnk $rnk -scoring_scheme weighted -rpt_label $rnkname -create_svgs false -include_only_symbols true -make_sets true -plot_top_x 20 -set_max 500 -set_min 15 -zip_report false -out $gmtresdir
    done
done
