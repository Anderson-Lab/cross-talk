## Example

You can change the Dockerfile to be something that works for your project, but the run command at the end needs to remain.

### Build docker image

docker build . -t remote_neo4j

### Starting

Head to remotedesktop.google.com and click set up via SSH. Copy the code 4/... for later.

```
export CODE=<here>
export HOSTNAME=<here>
docker run --rm -e CODE=$CODE --privileged --network host -it --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -e HOSTNAME=$HOSTNAME -e PIN=123456 remote_neo4j
```
