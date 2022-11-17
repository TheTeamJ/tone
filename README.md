# Tone

![](https://gyazo.com/64abf83ee241d258cf305a32913d8710/raw)

![](https://gyazo.com/6cd408b0031ae0e14b225450cf135515/raw)

## CLI demo
```
$ pip3 install -r requirements.txt
$ BASE_DIR_NAME="./" python3 main.py
```

## Flask app
```
$ BASE_DIR_NAME="/tmp/tone/" DEBUG=yes python3 app.py
```

## Flask app (local)
```
$ BASE_DIR_NAME="./tmp" DEBUG=yes python3 app.py
```

## Docker
```
$ docker build -t daiiz/tone:1.0 .
$ docker run -p 8080:8080 -it daiiz/tone:1.0
```

## Docker (development)
```
$ docker compose up app
```
