FROM unocha/alpine-base-python3:3.8

WORKDIR /src

COPY . .

RUN pip install -r requirements.txt
