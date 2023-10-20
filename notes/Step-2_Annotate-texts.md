
These scripts call the bioportal API and annotate entities. The output is stored next to the JSON files. For convenience, the `step2.sh` script is provided containing the following:

## Text extracted from PDFs

```
array=( texts.pdfs.biomechanics texts.pdfs.neither.psychology.nor.biomechanics texts.pdfs.psychology texts.pdfs.psychology.and.biomechanics)
for dir in "${array[@]}"
do
    echo $APPDIR/scripts/annotate_dir.sh $DATADIR/$dir contents | grep 'Completed\|Failed'
    $APPDIR/scripts/annotate_dir.sh $DATADIR/$dir contents | grep 'Completed\|Failed'
done
```

## Text from descriptions

```
array=( d1_descriptions d2_descriptions d3_descriptions d4_descriptions d5_descriptions d6_descriptions)
for dir in "${array[@]}"
do
    echo $APPDIR/scripts/annotate_dir.sh $DATADIR/$dir contents | grep 'Completed\|Failed'
    $APPDIR/scripts/annotate_dir.sh $DATADIR/$dir contents | grep 'Completed\|Failed'
done
```