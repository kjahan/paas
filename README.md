# paas
Prophet as a service

## Step I - create a docker image:

`docker build -t paas:latest -f deployment/Dockerfile .`

## Step II - find your IMAGE_ID for pass docker image:

`docker image ls`

## Step III - run a container (port forwarding on 5001):

`docker run -p 5001:5001 -i -t IMAGE-ID`

## Step IV - activate conda env inside the container

`conda activate apollo`

## Step V - run prophet server:

`python -m paas.server -d paas/uploads -o paas/figs`

## Step VI - run prophet client:

`python test_paas.py`

## Step VII - download prediction image:

`docker cp CONTAINER_NAME:/opt/paas/figs/image_file_name.png .`