#!/bin/bash
cat /dev/null > add_descriptions.cypher.txt
array=( d1_descriptions.annotated d2_descriptions.annotated d3_descriptions.annotated d4_descriptions.annotated d5_descriptions.annotated d6_descriptions.annotated )
for dir in "${array[@]}"
do
tee -a add_descriptions.cypher.txt << END
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:$DATADIR/$dir/contents.MESH.csv' AS row
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
  "LOAD CSV WITH HEADERS FROM 'file:$DATADIR/$dir/contents.MESH.csv' AS row
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
