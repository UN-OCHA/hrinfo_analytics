### HRInfo Analytics

## Build the docker image

`docker build --no-cache -t <image_name:image_tag> .`

## Use the docker image

`docker run --rm -v <client_secret.json_path>:/src/client_secret.json -w /src <image_name>:image_tag python3 <script_name>`



