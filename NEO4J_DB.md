# neo4j

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

I'm going to change mine so that it stores things automatically in Dropbox for easy sharing. Dropbox


## Loading hypotheses

**Note:** In order to get access to a Google sheet in csv format, the URL needs the following format: https://drive.google.com/uc?id=1MNMFsGFbR9L8rGOmn7fN4-A5gxBG23E2
```
LOAD CSV WITH HEADERS FROM 'https://drive.google.com/uc?id=1MNMFsGFbR9L8rGOmn7fN4-A5gxBG23E2' AS row
RETURN row
LIMIT 10;
```

