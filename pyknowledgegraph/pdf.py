import glob
import re

import fitz
import pandas as pd

#import spacy
#nlp = spacy.load("en_core_web_sm")

from collections import OrderedDict

abstract_headers = ["Abstract","ABSTRACT","Abstract-","Abstract."]
introduction_headers = ["Introduction","INTRODUCTION","Introduction-"]
section_headers = OrderedDict()
section_headers["introduction"] = introduction_headers
section_headers["methods"] = ["Methods","METHODS","Methods-", "Materials and Methods", "Materials and Methods-"]
section_headers["results"] = ["Results","RESULTS","Results-"]
section_headers["discussion"] = ["Discussion","DISCUSSION","Discussion-"]
section_headers["conclusion"] = ["Conclusion","CONCLUSION","Conclusion-"]

patterns_to_remove = [
    "Manuscript received",
    "Authorized licensed use limited to",
    "<image:",
    "All rights reserved."
]

def get_abstract(file_path):
    blocks = {}
    with fitz.open(file_path) as doc:
        for i,page in enumerate(doc):
            blocks[i] = page.get_text_blocks()
            
    return extract_abstract(blocks[0]) # assume that it is on the first page    

def get_pages(file_path):
    pages = {}
    with fitz.open(file_path) as doc:
        for i,page in enumerate(doc):
            pages[i] = page.get_text_blocks()
    return pages

def clean_section(contents):
    if type(contents) == list:
        content = " ".join(contents)
    else:
        content = contents
    content = re.sub("\s+"," ",content.replace("- ","-"))
    return content

def get_sections(file_path):
    sections = {}
    blocks = {}
    with fitz.open(file_path) as doc:
        for i,page in enumerate(doc):
            blocks[i] = page.get_text_blocks()
            
    sections["abstract"] = clean_section(extract_abstract(blocks[0])) # assume that it is on the first page
    sections["results"] = break_blocks_into_sections(blocks)
    
    for key in sections["results"].keys():
        sections["results"][key] = clean_section(sections["results"][key])
    return sections

def strip_blocks(pages):
    """Go through each page and remove blocks that don't look like main text blocks"""
    new_pages = {}
    found_end = False
    for p in pages.keys():
        page = pages[p]
        new_pages[p] = []
        num_vol = 0
        for block in page:
            skip = found_end
            if not skip:
                if "References" in block[4] or "REFERENCES" in block[4]:
                    skip = True
                    found_end = True
                if "Acknowledgment" in block[4] or "ACKNOWLEDGMENT" in block[4]:
                    skip = True
                    found_end = True
                for to_remove_pattern in patterns_to_remove:
                    if to_remove_pattern in block[4]:
                        skip = True
                        break
            
            if not skip:
                doc=nlp(block[4])
                num_subjects = 0
                num_sents = 0
                for sentence in doc.sents:
                    for word in sentence:
                        if "nsubj" in word.dep_:
                            num_subjects += 1
                            num_sents += 1
                if num_subjects == 0:
                    skip = True
            
            if not skip:
                new_pages[p].append(block)
    return new_pages

def find_bounds(pages,min_len=200):
    """Go through all of the blocks within all of the pages and find the first and last biggest valid blocks. 
       Return those positions"""
    ret_bottom_right = None
    ret_top_left = None
    for p in pages.keys():
        page = pages[p]
        if len(page) == 0:
            continue
        for block in page:
            last_block = block#page[-1]
            first_block = block#page[0]
            if len(last_block[4]) >= min_len:
                bottom_right = last_block[2],last_block[3]
                if ret_bottom_right is None:
                    ret_bottom_right = list(bottom_right)
                else:
                    if ret_bottom_right[0] < bottom_right[0]:
                        ret_bottom_right[0] = bottom_right[0]
                    if ret_bottom_right[1] < bottom_right[1]:
                        ret_bottom_right[1] = bottom_right[1]

            if len(first_block[4]) >= min_len:
                top_left = first_block[0],first_block[1]
                if ret_top_left is None:
                    ret_top_left = list(top_left)
                else:
                    if ret_top_left[0] > top_left[0]:
                        ret_top_left[0] = top_left[0]
                    if ret_top_left[1] > top_left[1]:
                        ret_top_left[1] = top_left[1]
    return ret_top_left,ret_bottom_right

def get_blocks_within_bounds(pages,top_left,bottom_right,removed_blocks=[],e=0.2):
    blocks = []
    for p in pages.keys():
        page = pages[p]
        for block in page:
            x_bound = block[0] >= (top_left[0]-e) and block[2] <= (bottom_right[0]+e)
            y_bound = block[1] >= (top_left[1]-e) and block[3] <= (bottom_right[1]+e)
            if x_bound and y_bound:
                blocks.append(block)
            else:
                removed_blocks.append((p,block))
    return blocks
            
        
def break_blocks_into_sections(pages,min_abstract_length = 50):
    results = {}
    for possible_section in section_headers.keys():
        results[possible_section] = []
    current_section = None
    current_spec_section_name = None
    
    clean_text = lambda header,txt: re.sub("\s+"," ",txt.replace(header, "").strip().replace("\n"," "))
    for p in pages.keys():
        page = pages[p]
        for block in page:
            skip = False
            for to_remove_pattern in patterns_to_remove:
                if to_remove_pattern in block[4]:
                    skip = True
                    break
            if not skip:
                for possible_section in section_headers.keys():
                    for spec_section_name in section_headers[possible_section]:
                        if spec_section_name in block[4]:
                            current_section = possible_section
                            current_spec_section_name = spec_section_name
                            break
                if current_section is not None and len(block[4]) >= min_abstract_length:
                    results[current_section].append(clean_text(current_spec_section_name,block[4]))
                
    return results

def knit(blocks):
    contents = []
    for block in blocks:
        contents.append(block[4].replace("-\n","").replace("\n"," ")) #.replace("\n"," "))
    contents = " ".join(contents)
    contents = re.sub("\s+"," ",contents.replace(".",".\n")) 
    return contents

def post_knit_process(contents):
    doc=nlp(contents)
    passed = []
    sentences = []
    ix = 0
    for sentence in doc.sents:
        sentences.append(sentence)
        has_subj = False
        if len(sentence) >= 3:
            for word in sentence:
                if "nsubj" in word.dep_:
                    has_subj = True
                    break
        if has_subj:
            passed.append(True)
        else:
            passed.append(False)
    results = pd.DataFrame({"sentence": sentences, "passed": passed})
    return results

def sort_headers(headers):
    lengths = []
    new_headers = []
    for header in headers:
        lengths.append(len(header))
        new_headers.append(header)
    for header in headers:
        new_headers.append(header.upper())
        lengths.append(len(header))
    headers = pd.DataFrame({"header":new_headers,"length":lengths})
    headers = headers.sort_values(by='length',ascending=False)
    headers = list(headers['header'])
    return headers
    
def extract_abstract(blocks,min_abstract_length = 100):
    clean_abstract = lambda txt: txt.replace(header,"").strip().replace("\n","")
    return_next = False
    for block in blocks:
        if not return_next:
            for header in sort_headers(abstract_headers):
                if header in block[4]:
                    return_next = True
                    break
        if return_next and len(block[4].split(" ")) > min_abstract_length:
            return clean_abstract(block[4])
            
    # Nothing was explicitly found with an abstract header. 
    # Defaulting back to biggest block of text before introduction header

    first_min_block = None
    biggest_block = None
    biggest_block_length = -1
    for block in blocks:
        if len(block[4]) > biggest_block_length:
            biggest_block_length = len(block[4])
            biggest_block = block[4]
            if first_min_block is None and len(block[4].split(" ")) >= min_abstract_length:
                first_min_block = block[4]
            
        for header in sort_headers(introduction_headers):
            if header in block[4]:
                return clean_abstract(biggest_block)
    
    if first_min_block:
        return clean_abstract(first_min_block) 
    else:
        return clean_abstract(biggest_block)
            
def process_dir(d):
    sections = {}
    for file in glob.glob(f"{d}/*.pdf"):
        print("Processing",file)
        sections[file] = get_sections(file)
    return sections

