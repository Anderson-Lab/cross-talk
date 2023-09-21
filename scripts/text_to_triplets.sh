#!/bin/bash

IFS=$'\n'

[ -d "tmp/" ] || mkdir "tmp/"

DIR=$1
OUTDIR=$2
KEY=$3
for file in `ls "$DIR" | grep '\.json$'`; do
    echo "[$file]"
    [ -d "$DIR/../$OUTDIR/" ] || mkdir "$DIR/../$OUTDIR/"
    echo cp "$DIR/$file" tmp/source.json
    cp "$DIR/$file" tmp/source.json && \
    if docker run --workdir /app --env OPENAI_API_KEY=$OPENAI_API_KEY -v $PWD/pyknowledgegraph:/app/pyknowledgegraph -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 /app/scripts/text_to_triplets.py tmp/source.json tmp/triplets.json $KEY; then
      cp tmp/triplets.json "$DIR/../$OUTDIR/$file.json" && echo "Completed: $file"
    else
      echo "Failed: $file"
    fi;
done;
