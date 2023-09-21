#!/usr/bin/python3

# https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/17299597/ascii
import sys
import requests

DIR=sys.argv[1]
import pandas as pd
corpus = pd.read_csv('../Corpus.tsv',sep="\t")
print(corpus.head())

#ids = [ID for ID in open(f"{DIR}/PMIDS").read().split("\n") if ID.strip() != ""]

c = 0
for ID in corpus['PMID']:
    url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/{ID}/ascii"
    print(ID,int(100*(c+1)/len(corpus)))
    response = requests.get(url)
    f = open(f"{DIR}/{ID}.xml","w")
    f.write(str(response.content))
    f.close()
    c+=1 
