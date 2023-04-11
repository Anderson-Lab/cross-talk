import os
import json
import sys
import time
import openai

sys.path.insert(0,'/app/')

from pyknowledgegraph import pdf

infile = sys.argv[1]
outfile = sys.argv[2]
title = sys.argv[3]

r = os.system(f'mutool convert -F text -o /app/tmp/file.txt {infile}')

if r != 0:
    print(f'mutool failed on file {infile}')
    exit(r)
    
openai.api_key = os.getenv("OPENAI_API_KEY")

content = open('/app/tmp/file.txt').read()
new_sentences = []
paragraphs = content.split("\n\n")
for p in paragraphs:
    new_sentences.extend(p.replace("\n"," ").replace("- ","").split("."))
    
import string
printable = set(string.printable)

valid_sentences = []
for i, sent in enumerate(new_sentences):
    sent = ''.join(filter(lambda x: x in printable, sent))
    gpt_prompt = f"""
Decide whether a Text is a grammatically correct sentence or not.
    
Text: {sent}.
Answer: """

    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=gpt_prompt,
      temperature=0,
      max_tokens=256,
      top_p=1.0,
      frequency_penalty=0.5,
      presence_penalty=0.0
    )

    text = response['choices'][0]['text'].strip()
    #print(gpt_prompt+text)
    if text.startswith("Yes"):
        valid_sentences.append((sent+".").strip())
    
    time.sleep(1)
    #if i % 50 == 0:
    #    print('Sleeping')
    #    time.sleep(60)

contents = "\n".join(valid_sentences)

sections = {}
sections['title'] = title
sections['contents'] = contents
open(outfile,"w").write(json.dumps(sections))