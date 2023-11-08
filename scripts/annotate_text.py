import os
import json
import sys

import pandas as pd

sys.path.insert(0,'/app')
import pyknowledgegraph

infile = sys.argv[1]
field = sys.argv[2]
outfile = sys.argv[3]
ontology = sys.argv[4] # NCIT, SCIO

# storing the JSON response
# from url in data
data_json = json.loads(open(infile).read())
wrapper = pyknowledgegraph.ncbowrapper.NCBOWrapper()
annotation = wrapper.annotate(data_json[field],ontologies=ontology)
ids = []
prefLabels = []
to_froms = []
matchTypes = []
texts = []
for a in annotation:
    match_type = "|".join([str(v['matchType']) for v in a['annotations']])
    if "PREF" in match_type:
        to_froms.append("|".join(["%s-%s"%(v['from'],v['to']) for v in a['annotations']]))
        matchTypes.append(match_type)
        texts.append("|".join([str(v['text']) for v in a['annotations']]))
        ids.append(a['annotatedClass']['@id'])
        prefLabels.append(a['annotatedClass']['prefLabel'])
annotation_df = pd.DataFrame({"prefLabel": prefLabels, "id":ids,"from_to":to_froms,"matchType":matchTypes,"text":texts})
annotation_df.to_csv(f'{outfile}',index=False)
