### manual
```
$ wget -O https://dist.neo4j.org/deb/neo4j_5.7.0_all.deb
$ wget -O https://github.com/neo4j/cypher-shell/releases/download/1.1.15/cypher-shell_1.1.15_all.deb
```
### apt
```
$ wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
$ echo 'deb https://debian.neo4j.com stable 5' | sudo tee /etc/apt/sources.list.d/neo4j.list
$ sudo apt-get update
$ sudo apt install -y neo4j=1:5.7.0
```
### to find the plugin directory
```
$ grep plugins /etc/neo4j/neo4j.conf
server.directories.plugins=/var/lib/neo4j/plugins
```
### to install neosemantics, graph data science, and apoc
```
ownload from: https://github.com/neo4j-labs/neosemantics/release
$ sudo cp neosemantics-5.7.0.0.jar /var/lib/neo4j/plugins/
$ curl -O https://graphdatascience.ninja/neo4j-graph-data-science-2.4.5.zip
$ unzip neo4j-graph-data-science-2.4.5.zip 
$ sudo cp neo4j-graph-data-science-2.4.5.jar /var/lib/neo4j/plugins/
$ cd /var/lib/neo4j/plugins
$ ln -s ../labs/apoc-5.7.0-core.jar .
$ sudo vi /etc/neo4j/neo4j.conf
dbms.security.auth_enabled=false
dbms.security.allow_csv_import_from_file_urls=true
apoc.import.file.enabled=true
server.directories.import=<your base directory>
```
### to run neo4j as a user, not root
```
$ sudo usermod -a -G neo4j <your username> # log out and log back in to take effect
$ sudo chgrp -R neo4j /var/lib/neo4j /var/log/neo4j
$ sudo chmod 2775 $(find /var/lib/neo4j -type d)
$ sudo chmod 2664 $(find /var/lib/neo4j -type f)
$ neo4j start # if you get a permission denied, delete the .pid or .log files and retry
```
### to access neo4j
```
$ cypher-shell
@neo4j>
@neo4j> CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;
@neo4j> CALL n10s.graphconfig.init({handleVocabUris: "MAP"});
@neo4j> WITH "https://data.bioontology.org/ontologies/MESH/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
        AS uri
        CALL n10s.rdf.import.fetch(uri, 'RDF/XML',{ classLabel : 'MESH_Class'})
        YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams, extraInfo
        RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams, extraInfo;
@neo4j> WITH "https://data.bioontology.org/ontologies/NCIT/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=rdf"
        AS uri
        CALL n10s.rdf.import.fetch(uri, 'RDF/XML',{ classLabel : 'NCIT_Class'})
        YIELD terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams, extraInfo
        RETURN terminationStatus, triplesLoaded, triplesParsed, namespaces, callParams, extraInfo;
$ export APPDIR=<path to this repo>
$ export DATADIR=<your base directory # all other paths will be relative>
$ export OPENAI_API_KEY=<text string key to authenticate for OAI API>
```
