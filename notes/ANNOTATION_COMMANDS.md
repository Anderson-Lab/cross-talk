# Annotation Command Collection

## Annotating directories
Below is an example that annotates the abstract field within each of the texts.
```
$APPDIR/scripts/annotate_dir.sh $DATADIR/abstracts contents | grep 'Completed\|Failed'
```

Below is an example that annotates the text field within each of the hypotheses.
```
$APPDIR/scripts/annotate_dir.sh $DATADIR/hypotheses text | grep 'Completed\|Failed'
```