#!/bin/bash
cat /dev/null > add_annotations.cypher.txt
array=( MESH NCIT )
dirs=( texts.pdfs.psychology.and.biomechanics.annotated texts.pdfs.psychology.annotated texts.pdfs.biomechanics.annotated texts.pdfs.neither.psychology.nor.biomechanics.annotated )
for dir in "${dirs[@]}"
do
for ontology in "${array[@]}"
do
    cp $DATADIR/$dir/contents.$ontology.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Paper >> add_annotations.cypher.txt
done
done
