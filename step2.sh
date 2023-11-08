#!/bin/bash

# Text extracted from PDFs
array=( texts.pdfs.biomechanics texts.pdfs.neither.psychology.nor.biomechanics texts.pdfs.psychology texts.pdfs.psychology.and.biomechanics)
for dir in "${array[@]}"
do
    echo $APPDIR/scripts/annotate_dir.sh $DATADIR/$dir contents | grep 'Completed\|Failed'
    $APPDIR/scripts/annotate_dir.sh $DATADIR/$dir contents | grep 'Completed\|Failed'
done

# text from descriptions
array=( d1_descriptions d2_descriptions d3_descriptions d4_descriptions d5_descriptions d6_descriptions)
for dir in "${array[@]}"
do
    echo $APPDIR/scripts/annotate_dir.sh $DATADIR/$dir contents | grep 'Completed\|Failed'
    $APPDIR/scripts/annotate_dir.sh $DATADIR/$dir contents | grep 'Completed\|Failed'
done
