import os
import openai
import json
import sys
infile = sys.argv[1]
field = sys.argv[2]
outfile = sys.argv[3]
sections = json.loads(open(infile).read())

openai.api_key = os.getenv("OPENAI_API_KEY")

content = sections[field]

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

f = open(outfile,"w")
f.write(str(get_embedding(content, model='text-embedding-ada-002'))[1:-1])
f.close()
