
import os
import openai
#import wandb

openai.api_key = os.getenv("OPENAI_API_KEY")
#wandb.login(key="32dc932461e1fa4fe38408e0a0556c607e351485")
#run = wandb.init(project='GPT-3 in Python')

#prediction_table = wandb.Table(columns=["prompt", "completion"])
# examples below
gpt_prompt = "Correct this to standard English:\n\nShe no went to the market."

gpt_prompt = "A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr"

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=gpt_prompt,
  temperature=0.5,
  max_tokens=256,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

print('Open AI response')
print(response['choices'][0]['text'])


#prediction_table.add_data(gpt_prompt,response['choices'][0]['text'])
