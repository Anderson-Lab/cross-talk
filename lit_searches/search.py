#!/usr/bin/python3
from pymed import PubMed
import json
import numpy as np
years = np.arange(1980,2023)
pubmed = PubMed(tool="Chronic Pain Research", email="pauleanderson@gmail.com")
print("Year","PMID",sep=",")
for year in years:
    results = pubmed.query(f'("spinal cord injuries"[MeSH Terms]) AND (animal[Filter]) AND {year}[dp]', max_results=9998)
    for result in results:
        article = json.loads(result.toJSON())
        pmid=article['pubmed_id'].split("\n")[0]
        print(year,pmid,sep=",")
        f = open(f"/mnt/clbp/lit_searches/s1/{pmid}.json","w")
        f.write(result.toJSON())
        f.close()
