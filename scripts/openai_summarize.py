import os
import openai
import json
import sys
infile = sys.argv[1]
sections = json.loads(open(infile).read())

openai.api_key = os.getenv("OPENAI_API_KEY")

content = sections["abstract"]
gpt_prompt = f"{content}\n\nTl;dr"

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=gpt_prompt,
  temperature=0.5,
  max_tokens=256,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

print('Abstract summary')
print(response['choices'][0]['text'])

for key in ["discussion","conclusion"]:
    content = sections["results"][key]
    gpt_prompt = f"{content}\n\nTl;dr"

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=gpt_prompt,
      temperature=0.5,
      max_tokens=256,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )

    print(f'{key} summary')
    print(response['choices'][0]['text'])