# geohack-api

## Run app
### With Docker
run db
```
make run-db
```

run app
```
make run-app
```

To check if the server runs well
```
curl localhost:8000
```

### With your host OS's runtime
**Make sure you've installed poerty globally

To install dependencies
```
make install
```

To run server
```
make run-app-host
```

## Other info

To run shell on venv
```
poetry shell
```