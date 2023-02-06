#!/bin/bash

IFS=$'\n'

DIR=$1
for file in `ls "$DIR" | grep -P '\.pdf$'`; do
    echo "[$file]"
    mkdir "$DIR/text/"
    cp "$DIR/$file" tmp/source.pdf && \
    docker run -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/pdf_to_text.py tmp/source.pdf tmp/source.json && \
    cp tmp/source.json "$DIR/text/$file.json" && echo "Completed: $file"    
done;