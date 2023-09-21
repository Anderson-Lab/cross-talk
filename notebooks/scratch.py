def get_triplets_old(contents,field):
    all_sentences_with_results = []
    all_sentences_without_results = []
    
    output = []
    paragraphs = contents[field].split("\n\n")
    for paragraph in paragraphs:
        output.append({"paragraph": {"text":paragraph}})
        num_words = len(paragraph.split(" "))
        if num_words < min_num_words_in_paragraph:
            continue
        #print(paragraph)
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "You will be provided a paragraph, and your task is to extract all the sentences that describe scientific results. If there are no matching sentences, respond None. Your answer should be a numbered list."},
              {"role": "user", "content": paragraph }
          ],
          temperature=0,
          max_tokens=1024,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        sentences = response['choices'][0]['message']['content'].split("\n")
        if sentences[0].strip() == "None":
            continue
        sentences_with_results = [" ".join(s.split(" ")[1:]) for s in sentences] # Remove the number
        sentences_without_results = []
        for sent in paragraph.strip().split(". "):
            if sent[-1] != ".":
                sent = f"{sent}."
            if f"{sent}." not in sentences:
                sentences_without_results.append(f"No results: {sent}")
        #all_sentences_with_results.extend(sentences_with_results)
        #all_sentences_without_results.extend(sentences_without_results)
        output[-1]["paragraph"]["sentences_with_results"] = [{"text":s, "clauses": []} for s in sentences_with_results]
        output[-1]["paragraph"]["sentences_without_results"] = [{"text":s, "clauses": []} for s in sentences_without_results]
        
        for j,sentence in enumerate(sentences_with_results):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You will be provided a sentence, and your task is break that sentence into independent clauses. Your answer should be a numbered list."},
                    {"role": "user", "content": sentence }
                ],
                temperature=0,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            #print("Sentence:",sentence)
            clauses = [" ".join(clause.split(" ")[1:]) for clause in response['choices'][0]['message']['content'].split("\n")]
            output[-1]["paragraph"]["sentences_with_results"][j]["clauses"] = [{"text": c} for c in clauses]
            for i, clause in enumerate(clauses):            
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You will be provided a sentence, and your task is split it into a subject, verb, and object. Return your answer as JSON with keys subject, verb, and object."},
                        {"role": "user", "content": sentence }
                    ],
                    temperature=0,
                    max_tokens=1024,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )   
                content = response['choices'][0]['message']['content']
                output[-1]["paragraph"]["sentences_with_results"][j]["clauses"][i]["triplet"] = json.loads(content)
    return output

import time

def get_triplets(contents,field):
    all_sentences_with_results = []
    all_sentences_without_results = []
    
    output = []
    paragraphs = contents[field].split("\n\n")
    for paragraph in paragraphs:
        output.append({"paragraph": {"text":paragraph}})
        num_words = len(paragraph.split(" "))
        if num_words < min_num_words_in_paragraph:
            continue
        #print(paragraph)
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "Rewrite these sentences such that each sentence has one subject and one object. Keep the meaning the same. Your answer should be a numbered list."},
              {"role": "user", "content": paragraph }
          ],
          temperature=0,
          max_tokens=1024,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        sentences = response['choices'][0]['message']['content'].split("\n")
        if sentences[0].strip() == "None":
            continue
        sentences_with_results = [" ".join(s.split(" ")[1:]) for s in sentences] # Remove the number
        sentences_without_results = []
        for sent in paragraph.strip().split(". "):
            if sent[-1] != ".":
                sent = f"{sent}."
            #if f"{sent}." not in sentences:
            #    sentences_without_results.append(f"No results: {sent}")
        #all_sentences_with_results.extend(sentences_with_results)
        #all_sentences_without_results.extend(sentences_without_results)
        output[-1]["paragraph"]["sentences_with_results"] = [{"text":s, "clauses": []} for s in sentences_with_results]
        output[-1]["paragraph"]["sentences_without_results"] = [{"text":s, "clauses": []} for s in sentences_without_results]

        print("Sentences with results:")
        print("\n".join(sentences_with_results))
        for j,sentence in enumerate(sentences_with_results):
            print("Sentence",j+1,"out of",len(sentences_with_results))
            #response = openai.ChatCompletion.create(
            #    model="gpt-3.5-turbo",
            #    messages=[
            #        {"role": "system", "content": "You will be provided a sentence, and your task is break that sentence into independent clauses. Your answer should be a numbered list."},
            #        {"role": "user", "content": sentence }
            #    ],
            #    temperature=0,
            #    max_tokens=1024,
            #    top_p=1,
            #    frequency_penalty=0,
            #    presence_penalty=0
            #)
            #time.sleep(2)
            #print("Sentence:",sentence)
            clauses = [" ".join(clause.split(" ")[1:]) for clause in sentence.split("\n")]
            output[-1]["paragraph"]["sentences_with_results"][j]["clauses"] = [{"text": c} for c in clauses]
            for i, clause in enumerate(clauses):  
                print("Clause",i+1,"out of",len(clauses))
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You will be provided a sentence, and your task is split it into a subject, verb, and object. Return your answer as JSON with keys subject, verb, and object."},
                        {"role": "user", "content": sentence }
                    ],
                    temperature=0,
                    max_tokens=1024,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                time.sleep(2)
                content = response['choices'][0]['message']['content']
                output[-1]["paragraph"]["sentences_with_results"][j]["clauses"][i]["triplet"] = json.loads(content)
    return output