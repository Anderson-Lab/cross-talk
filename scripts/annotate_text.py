import os
import json
import sys

import pandas as pd

sys.path.insert(0,'/app')
import pyknowledgegraph

infile = sys.argv[1]
field = sys.argv[2]
outfile = sys.argv[3]

# storing the JSON response
# from url in data
data_json = json.loads(open(infile).read())

print(data_json)
wrapper = pyknowledgegraph.ncbowrapper.NCBOWrapper()
annotation = wrapper.annotate(data_json[field],ontologies="NCIT")
ids = []
prefLabels = []
for a in annotation:
    ids.append(a['annotatedClass']['@id'])
    prefLabels.append(a['annotatedClass']['prefLabel'])
annotation_df = pd.DataFrame({"prefLabel": prefLabels, "id":ids})
annotation_df.to_csv(f'{outfile}',index=False)
