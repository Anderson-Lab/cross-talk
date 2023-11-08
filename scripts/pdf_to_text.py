import os
import json
import sys

#from tika import parser

sys.path.insert(0,'/app/')
from pyknowledgegraph import pdf

infile = sys.argv[1]
outfile = sys.argv[2]
title = sys.argv[3]

#content = parsed['content']
sections = pdf.get_sections(infile)
sections['title'] = title
open(outfile,"w").write(json.dumps(sections))
