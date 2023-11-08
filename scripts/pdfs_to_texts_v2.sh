#!/bin/bash

IFS=$'\n'

[ -d "tmp/" ] || mkdir "tmp/"

DIR=$1
OUTDIR=$2
for file in `ls "$DIR" | grep '\.pdf$'`; do
    echo "[$file]"
    [ -d "$DIR/../$OUTDIR/" ] || mkdir "$DIR/../$OUTDIR/"
    echo cp "$DIR/$file" tmp/source.pdf
    cp "$DIR/$file" tmp/source.pdf && \
    if docker run --workdir /app --network host --env OPENAI_API_KEY=$OPENAI_API_KEY -v $PWD/pyknowledgegraph:/app/pyknowledgegraph -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 /app/scripts/pdf_to_text_v2.py tmp/source.pdf tmp/source.json $file; then
      cp tmp/source.json "$DIR/../$OUTDIR/$file.json" && echo "Completed: $file"
    else
      echo "Failed: $file"
    fi;
done;
