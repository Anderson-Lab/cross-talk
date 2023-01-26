import os
from tika import parser  

import sys
infile = sys.argv[1]
outfile = sys.argv[2]

parsed = parser.from_file(infile)
content = parsed['content']
f = open(outfile,"w")
f.write(content)
f.close()