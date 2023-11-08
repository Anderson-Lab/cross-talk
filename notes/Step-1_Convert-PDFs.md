
These scripts convert a PDF to text, which is naturally messy. It then makes API calls to OpenAI to cull sentences that are not deeemed full/complete sentences. For convenience, the `step1.sh` script is provided containing the following:

```
array=( pdfs.biomechanics pdfs.neither.psychology.nor.biomechanics pdfs.psychology pdfs.psychology.and.biomechanics)
for dir in "${array[@]}"
do
    echo $APPDIR/scripts/pdfs_to_texts_v2.sh $DATADIR/$dir texts.$dir
    $APPDIR/scripts/pdfs_to_texts_v2.sh $DATADIR/$dir texts.$dir
done
```