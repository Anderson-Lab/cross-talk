# cross-talk

## Installation notes

Following this: https://www.geeksforgeeks.org/get-list-of-files-and-folders-in-google-drive-storage-using-python/

sudo pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

## Workflow
docker build -t cross-talk .

docker run --env OPENAI_API_KEY=foobar cross-talk env

docker run --env OPENAI_API_KEY=foobar cross-talk python3 ./pkg/openai_verificiation.py