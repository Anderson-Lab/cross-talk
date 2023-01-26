# cross-talk

## Installation notes

## Workflow
docker build -t cross-talk .

docker run --env OPENAI_API_KEY=foobar cross-talk env

docker run --env OPENAI_API_KEY=foobar cross-talk python3 ./pkg/openai_verificiation.py