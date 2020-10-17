# paas
Prophet as a service

Prophet runs as a web service listenning on port `5001`.  To run the time series prediction, you should first upload the time series file and then hit predict api end point.  See or run `test_paas.py` script for the steps.

After running the prediction, the server stores the outcome in a png file in `/opt/paas/figs` folder.  So, you can download the visualization file from container to your local machine.

## Step I - create a docker image:

`docker build -t paas:latest -f deployment/Dockerfile .`

## Step II - find your `pass`'s IMAGE_ID:

`docker image ls`

## Step III - run container (port forwarding on 5001):

`docker run -p 5001:5001 -i -t IMAGE-ID`

## Step IV - activate conda env inside the container

`conda activate apollo`

## Step V - run prophet server:

`python -m paas.server -d paas/uploads -o paas/figs`

## Step VI - run prophet client:

`python test_paas.py`

## Step VII - download prediction image:

`docker cp CONTAINER_NAME:/opt/paas/figs/image_file_name.png .`