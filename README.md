# cross-talk

## Installation notes
### Misc
I'm assuming a directory tmp is created but it is not tracked in git, so you'll have to mkdir tmp inside this repo.

### Google Drive
For ease of use for the entire team, we are storing results in Google Drive. To make this easier, I am assuming folks can mount google drive locally. Here are the links that worked for me.

https://medium.com/@enthu.cutlet/how-to-mount-google-drive-on-linux-windows-systems-5ef4bff24288

https://github.com/astrada/google-drive-ocamlfuse/wiki/Headless-Usage-&-Authorization

google-drive-ocamlfuse -headless -label me -id 991295574367-b5jslg94q7ingil90887qqpjomkq41mu.apps.googleusercontent.com -secret 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

google-drive-ocamlfuse -label me $HOME/googledrive


## Workflow Examples
docker build -t cross-talk .

export OPENAI_API_KEY=foobar

docker run --env OPENAI_API_KEY=$OPENAI_API_KEY cross-talk env

docker run --env OPENAI_API_KEY=$OPENAI_API_KEY -v $PWD/scripts:/app/scripts cross-talk python3 ./scripts/openai_verificiation.py

cp "$HOME/googledrive/cLBP–chronic_lower_back_pain/cross-talk/papers/Papers cited by Schmid et al./PDFs_Schmid_Refs/1.38037-PB1-9531-R2.pdf" tmp/source.pdf && \
docker run -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/pdf_to_text.py tmp/source.pdf tmp/source.json

docker run --env OPENAI_API_KEY=$OPENAI_API_KEY -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/clean_text.py /app/tmp/1.38037-PB1-9531-R2.pdf.tika.txt

docker run --env OPENAI_API_KEY=$OPENAI_API_KEY -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk python3 ./scripts/openai_summarize.py /app/tmp/1.38037-PB1-9531-R2.pdf.tika.txt

docker run -it --env OPENAI_API_KEY=$OPENAI_API_KEY --gpus all -v $PWD/scripts:/app/scripts -v $PWD/tmp:/app/tmp cross-talk /bin/bash

### Create text/json from pdfs
./scripts/pdfs_to_texts.sh "$HOME/googledrive/cLBP–chronic_lower_back_pain/cross-talk/papers/Papers cited by Schmid et al./PDFs_Schmid_Refs"

## Neo4j

Setup and commands are assuming Neo4j desktop and cypher-shell

From Neo4j browser, create new project. I'm calling mine cross-talk. 

Then add local DBMS. I'm numbering mine for trial and error purposes, so I'm going to start with v1. Create it with a password and then start it. Making it active in the desktop. I'll be using the neo4j default database.

Then you should be able to ./cypher-shell -u neo4j -p [your password here]

I always forget the goofy way you install plugins which we need. You have to click on Projects and then click on the DB you created. The plugins tab will then be on the right side of screen.

I'm installing:
* APOC
* Neo4j streaming
* neosemantics

I also set dbms.security.allow_csv_import_from_file_urls=true

See NEO4J_DB.md