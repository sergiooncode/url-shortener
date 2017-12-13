# URL Shortener

URL Shortener à la bit.ly but way humbler. The Shortener is exposed through an API with endpoints to create a redirect between short url to target url, configure target url for different types of devices, get statistics about redirects, and hit short url and get redirected to target url.

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

```
make test
```

## Running the URL Shortener API application

```
./manage runserver
```


## API Usage
----

### Redirect to target url

- **URL**

  /:hashed_id

-  **Method:**
  
   `GET`

- **URL Params:**
  **Required:**
  `hashed_id=[string]`

- **Success Response:**

  - **Code:** 302 FOUND <br />
    **Content:** `{ }`
 
- **Error Response:**

  - **Code:** 404 NOT FOUND <br />
    - When / route is hit:
      - **Content:** `{ "error" : "not found" }`
    - When /:hashed_id route is hit but hashed_id doesn't exist
      - **Content:** `{ "error" : "no redirects found for short url <shortUrl>" }`

### Create redirect short url to target url

- **URL**

  /redirects

-  **Method:**
  
   `POST`

- **Data Params:**
  **Required:**
  `longUrl=[string]`

- **Success Response:**

  - **Code:** 200 OK <br />
      - **Content:** `{ "shortUrl": <shortUrl> }`

### Get data about all existing redirects

- **URL**

  /redirects

-  **Method:**
  
   `GET`

- **Success Response:**

  - **Code:** 200 OK <br />
      - **Content:** 
        ```json
         {
             "<hashed_id>": [
                 {
                     "longUrl": <mobile_target_url>,
                     "redirectCount": <count>,
                     "sinceCreation": <since_creation>,
                     "type": "mobile"
                 },
                 {
                     "longUrl": <tablet_target_url>,
                     "redirectCount": <count>,
                     "sinceCreation": <since_creation>,
                     "type": "tablet"
                 },
                 {
                     "longUrl": <desktop_target_url>,
                     "redirectCount": <count>,
                     "sinceCreation": <since_creation>,
                     "type": "desktop"
                 }
             ],
             ...
         }
        ```

### Configure target url associated to a short url for specific devices

- **URL**

  /redirects/:hashed_id

-  **Method:**
  
   `PATCH`

- **URL Params:**
  **Required:**
  `hashed_id=[string]`

- **Data Params:**
  **Required:**
  ```json
   {
          "mobile": <mobile_target_url>,
          "tablet": <tablet_target_url>,
          "desktop": <desktop_target_url>
   }
  ```

- **Success Response:**

  - **Code:** 200 OK <br />
      - **Content:** `{ "shortUrl": <shortUrl> }`
 
## Design Decisions

### API

The API was designed taking a REST-like approach. The endpoints uri represent the resource on which the request acts based on the HTTP verb (GET to read, POST to create and PATCH to update). Compliance with best practices around HTTP protocol were considered and that's why PATCH was chosen instead of PUT since the configuration of a shortened url described in the business rules implies a partial update (which fits the intended use of PATCH) and not an overwrite of the resource (which fits the intended use of PUT).

Another intentional design approach taken was to make the error responses returned by the API be as informative and actionable as possible for its clients.

### DB Schema

The pattern single-table inheritance (STI) was chosen to generate the ORM models. That translates to having only one table to store the different objects: mobile, tablet and desktop redirects. Other patterns were considered but diregarded since 1) nothing in the current business rules hints that more device types will introduced soon, and 2) STI pattern is a well known pattern in the ORM used (SQLAlchemy).

A possible axis of change in the future could be that more device types are added (smart devices, bots browsing on user behalf, etc) which would force us to refactor towards a pattern that give a more normalized schema. That pattern would probably be Class Table Inheritance. 

### Hashing

When a target url (also long url) is submitted to create a redirect a one-to-one correspondence between a hash and the target url has to be established. The hash will be used late to generate the short url.

The mechanism currently used here to generate the mentioned hash is based on a bijective function provided a certain alphabet to convert from digits to characters.

Hashing is an area where several changes and improvements could come up and that was taken into account in the hashing package by adding an abstract base class that enforces to implement the encoding method since it's the one used in the project.

Things that should be take into account for improvements:

- The current mechanism uses the auto generated id generated by the database in primary key field, by using a hashing function on it manages to obfuscate the id, said that we can foresee the id could be guessed back which probably we want to avoid happening.

- The hashed ids generated has variable length currently but can be convenient to generate hashed ids with fixed length.

## TO-DO list

- Set up proper logging
- Check target url is valid when redirect is submitted
