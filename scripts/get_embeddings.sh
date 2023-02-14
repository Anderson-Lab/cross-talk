#!/bin/bash

IFS=$'\n'

[ -d "tmp/" ] || mkdir "tmp/"

DIR=$1
FIELD=$2
base_dir="$(basename $DIR)"
data_dir=$(basename `dirname "$DIR"`)
annotated_dir="$DIR/../$base_dir.embeddings/"
[ -d "$annotated_dir" ] || mkdir "$annotated_dir"
echo "uri," > $annotated_dir/embeddings.csv
for file in `ls "$DIR" | grep '\.json$'`; do
    echo "[$file]"
    cp "$DIR/$file" tmp/source.json && \
    if docker run --env OPENAI_API_KEY=$OPENAI_API_KEY -v $PWD/pyknowledgegraph:/app/pyknowledgegraph -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 /app/scripts/openai_embeddings.py tmp/source.json $FIELD tmp/embeddings.csv; then
      echo "file:/$base_dir/$file,$(< tmp/embeddings.csv)" >> $annotated_dir/embeddings.csv
      echo "Completed: $file"
    else
      echo "Failed: $file"
    fi
done;
