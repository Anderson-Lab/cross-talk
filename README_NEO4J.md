# neo4j

## Set up your ontologies

Install the n10s plugin.

```
CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;

CALL n10s.graphconfig.init({handleVocabUris: "MAP"});
```

```
WITH "https://data.bioontology.org/ontologies/SCIO/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
AS ncitUri
CALL n10s.rdf.import.fetch(ncitUri, 'RDF/XML')
YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams
RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams;
```

## Older

Setup and commands are assuming Neo4j desktop and cypher-shell

From Neo4j browser, create new project. I'm calling mine cross-talk.

Then add local DBMS. I'm numbering mine for trial and error purposes, so I'm going to start with v1. Create it with a password and then start it. Making it active in the desktop. I'll be using the neo4j default database.

Then you should be able to ./cypher-shell -u neo4j -p [your password here]

I always forget the goofy way you install plugins which we need. You have to click on Projects and then click on the DB you created. The plugins tab will then be on the right side of screen.

I'm installing:
* APOC
* Graph Data Science

I also set dbms.security.allow_csv_import_from_file_urls=true

## Setup
Pass over this setup for now and do not install n10s.

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
LOAD CSV WITH HEADERS FROM 'file:/hypotheses.annotated/contents.NCIT.csv' AS row
RETURN row
LIMIT 10;
```

```
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/hypotheses.annotated/contents.NCIT.csv' AS row
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
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/hypotheses.annotated/contents.SCIO.csv' AS row
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
  "LOAD CSV WITH HEADERS FROM 'file:/abstracts.annotated/contents.SCIO.csv' AS row
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

```
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/abstracts.annotated/contents.NCIT.csv' AS row
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

## Loading bioontologies

```
WITH "https://data.bioontology.org/ontologies/NCIT/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
AS uri
CALL n10s.rdf.import.fetch(uri, 'RDF/XML')
YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams
RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams;
```

```
WITH "https://data.bioontology.org/ontologies/SCIO/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
AS ncitUri
CALL n10s.rdf.import.fetch(ncitUri, 'RDF/XML')
YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams
RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams;
```

```
WITH "https://data.bioontology.org/ontologies/OCHV/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
AS uri
CALL n10s.rdf.import.fetch(uri, 'RDF/XML')
YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams
RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams;
```

```
WITH "https://data.bioontology.org/ontologies/MESH/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
AS uri
CALL n10s.rdf.import.fetch(uri, 'RDF/XML')
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
cp $DATADIR/hypotheses.annotated/contents.NCIT.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Hypothesis && echo "Completed"
```

```
cp $DATADIR/hypotheses.annotated/contents.SCIO.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Hypothesis && echo "Completed"
```

```
cp $DATADIR/abstracts.annotated/contents.NCIT.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Abstract && echo "Completed"
```

```
cp $DATADIR/abstracts.annotated/contents.SCIO.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Abstract && echo "Completed"
```

```
cp $DATADIR/abstracts.annotated/contents.MESH.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Abstract && echo "Completed"
```

```
cp $DATADIR/abstracts.annotated/contents.OCHV.csv $APPDIR/tmp/contents.csv && \
docker run -v $APPDIR/pyknowledgegraph:/app/pyknowledgegraph -v $APPDIR/scripts:/app/scripts -v $APPDIR/tmp:/app/tmp cross-talk python3 ./scripts/generate_neo4j_commands.py tmp/contents.csv Abstract && echo "Completed"
```

You then have to run the commands generated one at a time. A future TODO is to integrate this.

## Use cases
### Counting the number of entities in common

```
MATCH path = (s:Abstract)-[r1]->(re:Resource)<-[r2]-(e:Abstract)
WITH [s.title] as title1, [e.title] as title2, re, s, e
WITH re,apoc.coll.union(title1,title2) AS names, s, e
RETURN names, count(DISTINCT re) as value
ORDER BY value
```

I believe there are more efficient cyphers than this one.

```
MATCH p = (a)-[r]->(b)
WHERE (a:Hypothesis) OR (a:Abstract)
RETURN *

CALL gds.graph.project.cypher(
    'abstracts5',
    'MATCH (a)-[r]->(b) WHERE (a:Hypothesis) OR (a:Abstract) RETURN id(a) as id UNION MATCH (a)-[r]->(b) WHERE (a:Hypothesis) OR (a:Abstract) RETURN id(b) as id',
    'MATCH (n)-[e]-(m) WHERE (n:Abstract) RETURN id(n) AS source, e AS edge, id(m) AS target'
)
```

Add the connections and the count between nodes.

```
CALL {
    MATCH path = (s:Abstract)-[r1]->(re:Resource)<-[r2]-(e:Abstract)
    WITH [s.title] as title1, [e.title] as title2, re, s, e
    WITH re,apoc.coll.union(title1,title2) AS names, s, e
    RETURN names, count(DISTINCT re) as value
}
WITH names, value
MATCH (a:Abstract {title:names[0]}),(b:Abstract {title:names[1]})
MERGE (a)-[r:CONNECT {value:value}]-(b)
RETURN r
```

Now visualize what we did:

```
MATCH (a:Abstract)(a)-[r:CONNECT]-(b)
RETURN *
```

```
CALL gds.graph.project.cypher(
    'abstracts9',
    'MATCH (a:Abstract) RETURN id(a) as id',
    'MATCH (a:Abstract)-[e:CONNECT]-(b:Abstract) RETURN id(a) AS source, e.value AS weight, id(b) AS target'
)

CALL gds.louvain.write('abstracts9',
    {relationshipWeightProperty: 'weight',
     writeProperty: 'full_community_id'
})
```

Node similarity

```
CALL gds.graph.drop('myGraph');


CALL gds.graph.project(
    'myGraph',
    ['Abstract', 'Resource'],
    {
        HAS_ENTITY: {
            properties: {
            }
        }
    }
);

CALL gds.nodeSimilarity.stream('myGraph')
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1).title AS Abstract1, gds.util.asNode(node2).title AS Abstract2, similarity
ORDER BY similarity DESCENDING, Abstract1, Abstract2
```
