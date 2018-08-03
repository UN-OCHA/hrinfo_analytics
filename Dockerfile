FROM unocha/alpine-base-python3:3.8

WORKDIR /src

COPY . .

RUN apk add -U \
        git \
        openssh-client && \
    touch client_secret.json && \
    pip install -r requirements.txt
