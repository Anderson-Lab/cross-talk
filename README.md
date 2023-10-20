# cross-talk
## Prereqs
* Neo4j
* Docker

## Docker
### To shell into and debug the container:
`$ docker run -i -v $PWD:/app --workdir /app -t cross-talk /bin/bash`
### to build the container
`docker build -f Dockerfile -t cross-talk .`

## Neo4J
See [neo4j-install instructions](./neo4j-install.md)
1. Create new project
2. Under that project create or connect to a new DBMS
3. Start DBMS (version 5.7 because at the time of writing this the plugins weren't available in later versionss)
4. Install plugins: n10s, Graph Data Science, and APOC.

## Post install Neo4J

```
CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;
CALL n10s.graphconfig.init({handleVocabUris: "MAP"});
```

## Importing ontologies

### MESH
```
WITH "https://data.bioontology.org/ontologies/MESH/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
AS uri
CALL n10s.rdf.import.fetch(uri, 'RDF/XML',{ classLabel : 'MESH_Class'})
YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams, extraInfo
RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams, extraInfo;
```

### NCIT
```
WITH "https://data.bioontology.org/ontologies/NCIT/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
AS uri
CALL n10s.rdf.import.fetch(uri, 'RDF/XML',{ classLabel : 'NCIT_Class'})
YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams, extraInfo
RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams, extraInfo;
```

## Local file access

In order to access local files, we need to change some configuration of Neo4J. In the settings, you must add the following with modifications depending on your system (also covered in the `neo4j-install.md` instructions):

```
dbms.security.allow_csv_import_from_file_urls=true
server.directories.import=/home/paul/
apoc.import.file.enabled=true
```

You should replace the import directory to match your system, but all imports will be relative to this directory.

## Executing things at the command line

In order to execute things at the command line, you must set some
environment variables.

```
export APPDIR=path to this repo
export DATADIR=path to data directory # e.g. parent of pdfs.biomechanics
export OPENAI_API_KEY=foobar
```

## Next steps

The next steps are described in:

[Step 1 - Convert PDFs](./Step-1_Convert-PDFs.md)

[Step 2 - Annotate texts](./Step-2_Annotate-texts.md)

[Step 3 - Populate KG](./Step-3_Populate-KG.md)

Example queries are shown in [NEO4J_COMMANDS](./NEO4J_COMMANDS.md).
