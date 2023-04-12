#!/bin/bash

IFS=$'\n'

[ -d "tmp/" ] || mkdir "tmp/"

DIR=$1
OUTDIR=$2
for file in `ls "$DIR" | grep '\.txt$'`; do
    echo "[$file]"
    [ -d "$DIR/../$OUTDIR/" ] || mkdir "$DIR/../$OUTDIR/"
    cp "$DIR/$file" tmp/source.txt && \
    if docker run --network host --env OPENAI_API_KEY=$OPENAI_API_KEY -v $PWD/pyknowledgegraph:/app/pyknowledgegraph -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/text_to_json.py tmp/source.txt tmp/source.json $file; then
      cp tmp/source.json "$DIR/../$OUTDIR/$file.json" && echo "Completed: $file"
    else
      echo "Failed: $file"
    fi;
done;
