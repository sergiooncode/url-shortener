# URL Shortener API

URL Shortener a la bit.ly but humbler exposed through API with endpoints to create short url to target url redirect, configure target url for different types of devices, get statisticsi, and hit short url and get redirected to target url.

## Installing

- Clone this repository

- Change into the repository folder

- Install Python 3 using pyenv or similar (if necessary, the code was tested for Python 3.6.2)

- Create a virtual environment

```
python -m venv venv
```

- Install base and dev dependencies

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running the tests

- Run tests

```
make test
```

## API Usage

** Redirect to long url **

* **URL**

  /:hashed_id

* **Method:**
  
  `GET`

* **URL Params:**
  ** Required **
  ``hashed_id=[string]`

## Design Decisions

### API

### DB Schema

### Hashing
