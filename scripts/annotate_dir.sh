#!/bin/bash

IFS=$'\n'

[ -d "tmp/" ] || mkdir "tmp/"

DIR=$1
FIELD=$2
base_dir="$(basename $DIR)"
data_dir=$(basename `dirname "$DIR"`)
annotated_dir="$DIR/../$base_dir.annotated/"
echo "uri,uri_abstract_ncit_annotations" > $annotated_dir/contents.csv
[ -d "$annotated_dir" ] || mkdir "$annotated_dir"
for file in `ls "$DIR" | grep '\.json$'`; do
    echo "[$file]"
    cp "$DIR/$file" tmp/source.json && \
    if docker run -v $PWD/pyknowledgegraph:/app/pyknowledgegraph -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/annotate_text.py tmp/source.json $FIELD tmp/annotations.csv; then
      cp tmp/annotations.csv "$annotated_dir/$file.annotations.csv" && echo "Completed: $file" && \
      echo "file:/$base_dir/$file,file:/$base_dir.annotated/$file.annotations.csv" >> $annotated_dir/contents.csv
    else
      echo "Failed: $file"
    fi
done;
