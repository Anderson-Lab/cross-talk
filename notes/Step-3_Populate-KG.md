The following are Bash commands for setting up Neo4j Cypher-Shell commands to load annotations into the database. For convenience, 2 scripts are provided: `step3-load.sh` and `step3-txt2ent.sh`. Once those complete, run the final command to execute the Cypher-Shell commands placed in the output files `add_descriptions.cypher.txt`, `add_papers.cypher.txt`, and `add_annotations.cypher.txt`.

## Loading the notes

```
cat /dev/null > add_descriptions.cypher.txt
array=( d1_descriptions.annotated d2_descriptions.annotated d3_descriptions.annotated d4_descriptions.annotated d5_descriptions.annotated d6_descriptions.annotated )
for dir in "${array[@]}"
do
tee -a add_descriptions.cypher.txt << END
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/$dir/contents.MESH.csv' AS row
   RETURN row",
  "MERGE (a:Description {uri: row.uri})
  WITH a

  CALL apoc.load.json(a.uri)
  YIELD value

  UNWIND value.contents AS text

  WITH a,
       value.title AS title,
       value.contents AS text

  SET a.body = text , a.title = title
  RETURN a;",
  {batchSize: 1, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
END
done

cat /dev/null > add_papers.cypher.txt
dirs=( texts.pdfs.psychology.and.biomechanics.annotated texts.pdfs.psychology.annotated texts.pdfs.biomechanics.annotated texts.pdfs.neither.psychology.nor.biomechanics.annotated )
for dir in "${dirs[@]}"
do
tee -a add_papers.cypher.txt << END
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/$dir/contents.MESH.csv' AS row
   RETURN row",
  "MERGE (a:Paper {uri: row.uri})
  WITH a

  CALL apoc.load.json(a.uri)
  YIELD value

  UNWIND value.contents AS text

  WITH a,
       value.title AS title,
       value.contents AS text

  SET a.body = text , a.title = title
  RETURN a;",
  {batchSize: 1, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
END
done
```

Then run the commands in the generated files.

## Annotating text to entities

```
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
```

Then run the commands generated in the 3 output files:
```
$ cypher-shell -f add_descriptions.cypher.txt
$ cypher-shell -f add_papers.cypher.txt
$ cypher-shell -f add_annotations.cypher.txt
```
