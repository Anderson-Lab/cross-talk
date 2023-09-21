#!/usr/bin/python3

# https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/17299597/ascii
import sys
import requests

import pandas as pd
corpus = pd.read_csv('s1/ids.csv')
print(corpus.head())

#ids = [ID for ID in open(f"{DIR}/PMIDS").read().split("\n") if ID.strip() != ""]

c = 0
for ID in corpus['PMID']:
    try:
        print(int(ID),end=" ")
        response = requests.get(f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids={ID}")
        print(response.content)
    except:
        pass
    exit(0)
print("")
