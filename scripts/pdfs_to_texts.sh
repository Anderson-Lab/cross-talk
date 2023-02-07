#!/bin/bash

IFS=$'\n'

[ -d "tmp/" ] || mkdir "tmp/"

DIR=$1
for file in `ls "$DIR" | grep '\.pdf$'`; do
    echo "[$file]"
    [ -d "$DIR/../texts/" ] || mkdir "$DIR/../texts/"
    cp "$DIR/$file" tmp/source.pdf && \
    docker run -v $PWD/pyknowledgegraph:/app/pyknowledgegraph -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/pdf_to_text.py tmp/source.pdf tmp/source.json && \
    cp tmp/source.json "$DIR/../texts/$file.json" && echo "Completed: $file"
done;
