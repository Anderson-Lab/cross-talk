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
``
CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;

CALL n10s.graphconfig.init({handleVocabUris: "MAP"});

CALL n10s.nsprefixes.add('neo','neo4j://voc#');
CALL n10s.mapping.add("neo4j://voc#subCatOf","SUB_CAT_OF");
CALL n10s.mapping.add("neo4j://voc#about","ABOUT");
``

## Local files
You must allow local files to be pulled into neo4j by updating the config file.

By default things are imported relatively to an import directory. On my mac it is located at: You can find these things at:

Call dbms.listConfig() YIELD name, value
WHERE name='dbms.directories.neo4j_home'
RETURN value;

I'm going to change mine so that it stores things automatically in Dropbox for easy sharing. Dropbox.

ln -s /Users/pander14/Dropbox/cross-talk-v1/ "/Users/pander14/Library/Application Support/Neo4j Desktop/Application/relate-data/dbmss/dbms-5e9ab340-7f99-4512-8e34-4e130590c637/import/cross-talk-v1"

## Loading hypotheses

```
LOAD CSV WITH HEADERS FROM 'file:/cross-talk-v1/hypotheses.annotated/contents.csv' AS row
RETURN row
LIMIT 10;
```

```
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:/cross-talk-v1/hypotheses.annotated/contents.csv' AS row
   RETURN row",
  "MERGE (a:Hypothesis {uri: row.uri})
  WITH a

  CALL apoc.load.json(a.uri)
  YIELD value

  UNWIND value.text AS item

  WITH a,
       value.title AS title,
       value.text AS text

  SET a.body = body , a.title = title, a.datetime = datetime(date)
  RETURN a;",
  {batchSize: 5, parallel: true}
)
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
```
