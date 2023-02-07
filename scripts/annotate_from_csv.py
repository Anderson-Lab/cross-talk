import os
import json
import sys

# import urllib library
from urllib.request import urlopen

import pandas as pd

sys.path.insert(0,'..')

infile_uri = sys.argv[1]

url='https://drive.google.com/uc?id=' + infile_uri.split('/')[-2]
print("Fixed url:",url)
contents = pd.read_csv(url)

for uri in contents['uri']:
    url='https://drive.google.com/uc?id=' + uri.split('/')[-2]
    print(url)
    
    # store the response of URL
    response = urlopen(url)

    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())

    print(data_json)
    wrapper = pyknowledgegraph.ncbowrapper.NCBOWrapper()
    annotation = wrapper.annotate(data_json['text'],ontologies="NCIT")
    ids = []
    prefLabels = []
    for a in annotation:
        ids.append(a['annotatedClass']['@id'])
        prefLabels.append(a['annotatedClass']['prefLabel'])
    annotation_df = pd.DataFrame({"prefLabel": prefLabels, "id":ids})
    annotation_df.to_csv(f'{OUT_DIR_NAME}/{filename}.abstract.ncit.annotation.csv',index=False)