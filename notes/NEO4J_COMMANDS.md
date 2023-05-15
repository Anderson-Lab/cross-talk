# Neo4J Command Collection

## Modifying Nodes

```
MATCH (n: Resource)
SET n.base_uri = split(n.uri,"#")[0]
RETURN n
LIMIT 100
```

## Cleanup
```
MATCH (a:Hypothesis)
DETACH DELETE a;

MATCH (a:Abstract)
DETACH DELETE a;
```

## Returning a hierarchy
```
match (e:Resource {cui:"C0026860"})<-[r:subClassOf*..20]-(e2:Resource) return * limit 100;
```

MATCH (r {prefixIRI:'Thesaurus:C16346'}) return * 

## Return based on subset of ontology
```
MATCH (p:Paper)-[r:HAS_ENTITY]->(e2:Resource) 
WHERE exists((:Resource {cui:"C0026860"})<-[:subClassOf*..20]-(e2:Resource))
return *
```

## Finding annotations

Below is an example that annotates the contents field within each of the texts.
```
$APPDIR/scripts/annotate_dir.sh $DATADIR/texts contents | grep 'Completed\|Failed'
```

## Loading items to annotate

```
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/texts.annotated/contents.MESH.csv' AS row
   RETURN row",
  "MERGE (a:Paper {uri: row.uri})
  WITH a

  CALL apoc.load.json(a.uri)
  YIELD value

  UNWIND value.contents AS text_example

  WITH a,
       value.title AS title,
       value.contents AS text

  SET a.body = text , a.title = title
  RETURN a;",
  {batchSize: 1, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
```

```
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/d4_descriptions.annotated/contents.MESH.csv' AS row
   RETURN row",
  "MERGE (a:Description {uri: row.uri})
  WITH a

  CALL apoc.load.json(a.uri)
  YIELD value

  UNWIND value.contents AS text_example

  WITH a,
       value.title AS title,
       value.contents AS text

  SET a.body = text , a.title = title
  RETURN a;",
  {batchSize: 1, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
```

## Fixing nodes

```
MATCH (n:Description)
SET n.domain = split(split(n.uri,"/")[1],"_")[0]
RETURN n
```

## Annotating text to entities

```
cp $DATADIR/texts.annotated/contents.MESH.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Paper && echo "Completed"
```

```
cp $DATADIR/d1_descriptions.annotated/contents.MESH.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Description && echo "Completed"
```

```
cp $DATADIR/d2_descriptions.annotated/contents.MESH.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Description && echo "Completed"
```

```
cp $DATADIR/d3_descriptions.annotated/contents.MESH.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Description && echo "Completed"
```

```
cp $DATADIR/d4_descriptions.annotated/contents.MESH.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Description && echo "Completed"
```

```
cp $DATADIR/d5_descriptions.annotated/contents.MESH.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Description && echo "Completed"
```

```
cp $DATADIR/d6_descriptions.annotated/contents.MESH.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Description && echo "Completed"
```

## Subset of the ontology

```
MATCH (p)-[r:HAS_ENTITY]->(e2:Resource) 
WHERE (p:Paper or p:Description) and exists((:Resource {cui:"C0026860"})<-[:subClassOf*..20]-(e2:Resource))
return *
```