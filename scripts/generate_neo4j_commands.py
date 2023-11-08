import sys

import pandas as pd

infile = sys.argv[1]
type = sys.argv[2]
contents = pd.read_csv(infile)

command1 = """
CALL apoc.periodic.iterate(
"WITH '%s' AS uri_annotations
WITH uri_annotations, '%s' as uri_json
LOAD CSV WITH HEADERS FROM uri_annotations AS row
UNWIND row.id AS entity_uri
RETURN entity_uri,uri_json,uri_annotations",
"MATCH (c:Class {uri: entity_uri})
 WITH c, entity_uri, uri_json
 MATCH (a:%s {uri: uri_json})
 WITH a,c
 MERGE (a)-[:HAS_ENTITY]->(c)
 ",
{batchSize: 5, parallel: true}
)
YIELD batches, total, timeTaken, committedOperations
RETURN batches, total, timeTaken, committedOperations;
""".strip()

def generate_annotate_command(uri_json,uri_annotations,type):
    return command1%(uri_annotations,uri_json,type)

#print("############# START")
for ix in contents.index:
    uri_json = contents.loc[ix,"uri"]
    uri_annotations = contents.loc[ix,"uri_annotations"]
    #print("Index:",ix)
    #print(f"<START id='{ix}'>")
    print(generate_annotate_command(uri_json,uri_annotations,type))
    #print("</END>")
#print("############# END")
