## Example

You can change the Dockerfile to be something that works for your project, but the run command at the end needs to remain.

### Build docker image

docker build . -t remote_ubuntu

### Starting

Head to remotedesktop.google.com and click set up via SSH. Copy the code 4/... for later.

```
export CODE=<here>
export HOSTNAME=<here>
docker run --rm -e CODE=$CODE --name $HOSTNAME --privileged --network chronic_pain -it --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -e HOSTNAME=$HOSTNAME -e PIN=123456 -h $HOSTNAME -v /mnt/clbp:/mnt/clbp remote_ubuntu
```
