# Notebook commands
## Processing Corpus

```
docker run --rm -p 8891:8888 -v /mnt/clbp/:/mnt/clbp/ -v $PWD:$PWD cross-talk
```

And then run Process_PDFs.ipynb to read in Corpus.tsv and create pdfs with IDS.

Next step is to create clean text versions of PDFs.

```
export DATADIR=/mnt/clbp/
export APPDIR=/home/paul/cross-talk
export OPENAI_API_KEY=here
array=( pdfs.with.ids )
for dir in "${array[@]}"
do
    echo $APPDIR/scripts/pdfs_to_texts_v2.sh $DATADIR/$dir texts.$dir
    $APPDIR/scripts/pdfs_to_texts_v2.sh $DATADIR/$dir texts.$dir
done
```