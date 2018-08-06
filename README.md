# HR.info Analytics

## Build the docker image

`docker build --no-cache -t <image_name:image_tag> .`

Example:

`docker build --no-cache -t analytics:1 .`

## Use the docker image

`docker run --rm -v <client_secret.json_path>:/src/client_secret.json -w /src <image_name>:image_tag python3 <script_name>`

Example:

`docker run --rm -v $PWD/client_secret.json:/src/client_secret.json -w /src analytics:1 python3 list_orgs.py`

## Use docker-compose

The image will be built automatically if it was not yet built.

`docker-compose run --rm analytics python3 <script_name>`

Example:

`docker-compose run --rm analytics python3 list_orgs.py`
