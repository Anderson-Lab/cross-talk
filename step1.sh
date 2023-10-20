#!/bin/bash
array=( pdfs.biomechanics pdfs.neither.psychology.nor.biomechanics pdfs.psychology pdfs.psychology.and.biomechanics)
for dir in "${array[@]}"
do
  echo $APPDIR/scripts/pdfs_to_texts_v2.sh $DATADIR/$dir texts.$dir
  $APPDIR/scripts/pdfs_to_texts_v2.sh $DATADIR/$dir texts.$dir
done
