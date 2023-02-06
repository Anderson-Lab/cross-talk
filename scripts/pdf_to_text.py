import os
import json
import sys

from tika import parser

sys.path.insert(0,'.')
import pdf

infile = sys.argv[1]
outfile = sys.argv[2]

use_tika = False

if use_tika:
    parsed = parser.from_file(infile)
    content = parsed['content']
    f = open(outfile,"w")
    f.write(content)
    f.close()
else:
    sections = pdf.get_sections(infile)
    open(outfile,"w").write(json.dumps(sections))