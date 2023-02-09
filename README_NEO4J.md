# neo4j

Setup and commands are assuming Neo4j desktop and cypher-shell

From Neo4j browser, create new project. I'm calling mine cross-talk.

Then add local DBMS. I'm numbering mine for trial and error purposes, so I'm going to start with v1. Create it with a password and then start it. Making it active in the desktop. I'll be using the neo4j default database.

Then you should be able to ./cypher-shell -u neo4j -p [your password here]

I always forget the goofy way you install plugins which we need. You have to click on Projects and then click on the DB you created. The plugins tab will then be on the right side of screen.

I'm installing:
* APOC
* Neo4j streaming
* neosemantics

I also set dbms.security.allow_csv_import_from_file_urls=true

## Setup
```
CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;

CALL n10s.graphconfig.init({handleVocabUris: "MAP"});

CALL n10s.nsprefixes.add('neo','neo4j://voc#');
CALL n10s.mapping.add("neo4j://voc#subCatOf","SUB_CAT_OF");
CALL n10s.mapping.add("neo4j://voc#about","ABOUT");
```

## Cleanup
```
MATCH (a:Hypothesis)
DETACH DELETE a;

MATCH (a:Abstract)
DETACH DELETE a;
```

## Local files
You must allow local files to be pulled into neo4j by updating the config file.

You must also change your import directory to point to the correct location.

## Loading hypotheses

```
LOAD CSV WITH HEADERS FROM 'file:/hypotheses.annotated/contents.csv' AS row
RETURN row
LIMIT 10;
```

```
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/hypotheses.annotated/contents.csv' AS row
   RETURN row",
  "MERGE (a:Hypothesis {uri: row.uri})
  WITH a

  CALL apoc.load.json(a.uri)
  YIELD value

  UNWIND value.text AS example_var

  WITH a,
       value.title AS title,
       value.text AS text

  SET a.title = title , a.text = text
  RETURN a;",
  {batchSize: 1, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
```

```
MATCH (h:Hypothesis) return h;
```

This will load the hypotheses, but we do not have our ontology from NCIT.

## Loading abstracts

```
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/abstracts.annotated/contents.csv' AS row
   RETURN row",
  "MERGE (a:Abstract {uri: row.uri})
  WITH a

  CALL apoc.load.json(a.uri)
  YIELD value

  UNWIND value.abstract AS text_example

  WITH a,
       value.title AS title,
       value.abstract AS text

  SET a.body = text , a.title = title
  RETURN a;",
  {batchSize: 1, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
```

## Loading NCIT bioontology

```
WITH "https://data.bioontology.org/ontologies/NCIT/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
AS ncitUri
CALL n10s.rdf.import.fetch(ncitUri, 'RDF/XML')
YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams
RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams;
```

To check out the stats so far:

```
CALL apoc.meta.stats()
YIELD labels, relTypes, relTypesCount
RETURN labels, relTypes, relTypesCount;
```

A sample command:
```
MATCH path = (:Class {label: "Stenosis"})<-[:subClassOf]-(child)
RETURN path;
```

## Connecting entities to the ontologies
This command will print out neo4j commands you can run. We could send this to cypher automatically.
```
cp $DATADIR/hypotheses.annotated/contents.csv $APPDIR/tmp/ && \
docker run -v $PWD/pyknowledgegraph:/app/pyknowledgegraph -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Hypothesis && echo "Completed"
```

```
cp $DATADIR/abstracts.annotated/contents.csv $APPDIR/tmp/ && \
docker run -v $PWD/pyknowledgegraph:/app/pyknowledgegraph -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Abstract && echo "Completed"
```

```
MATCH p = (a)-[r]->(b)
WHERE (a:Hypothesis) OR (a:Abstract)
RETURN *
```
