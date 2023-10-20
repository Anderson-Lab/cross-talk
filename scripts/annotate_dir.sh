#!/bin/bash

IFS=$'\n'

[ -d "tmp/" ] || mkdir "tmp/"; chmod 2775 "tmp/"

ontologies=("SCIO" "NCIT" "MESH" "OCHV")

DIR=$1
FIELD=$2
base_dir="$(basename $DIR)"
data_dir=$(basename `dirname "$DIR"`)
#data_dir=$(dirname "$DIR")
annotated_dir="$DIR/../$base_dir.annotated/"
for ontology in ${ontologies[@]}; do
    echo $ontology
    echo "uri,uri_annotations" > $annotated_dir/contents.$ontology.csv
    [ -d "$annotated_dir" ] || mkdir "$annotated_dir"
    for file in `ls "$DIR" | grep '\.json$'`; do
      echo "[$file]"
      cmd="docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/annotate_text.py tmp/source.json $FIELD tmp/annotations.csv $ontology"
      echo $cmd
      cp "$DIR/$file" $APPDIR/tmp/source.json && \
      if eval $cmd; then
        cp $APPDIR/tmp/annotations.csv "$annotated_dir/$file.annotations.$ontology.csv" && echo "Completed: $file" && \
        echo "file:/$data_dir/$base_dir/$file,file:/$data_dir/$base_dir.annotated/$file.annotations.$ontology.csv" >> $annotated_dir/contents.$ontology.csv
      else
        echo "Failed: $file"
      fi
    done;
done;
