# A sample RESTful API implemented with Flask

## Background

An implementation of a RESTful API in Flask which accepts and retrieves two arbitrary entities - named <b>Article</b> and <b>Channel</b> - which have a many-to-many relationship.

An Article can belong to any number of <b>Channel</b>s and a <b>Channel</b> can hold any number of articles.
The <b>Article</b> entity will store a URL, the HTML title of the corresponding page and the word count of the page.

The <b>Channel</b> entity will store a name and a list of relevant articles.

A given user can add and delete any <b>Article</b>s/<b>Channel</b>. A new <b>Article</b> will be specified by a public URL and a <b>Channel</b> by any name.


#

##  Setup (Using Docker)

Installation of Docker required

#

## Running

A Dockerfile is provided.

Before building the image, create a file <i>.env</i> in the directory <i>instance</i>. In this, specify the following:

SECRET_KEY= `<insert any secret string>`

SQLALCHEMY_DEV_DATABASE_URI="sqlite:///../database/dev_database.db" 

SQLALCHEMY_PROD_DATABASE_URI=`<insert a database string corresponding to a running server with a ready database>`


PASSWORD=`<insert a root password>`

PASSWORD_HASH_ALGORITHM="hs256" 

SALT_LENGTH=8

TOKEN_VALID_PERIOD=60


When running the image, provide the environment variable <i>FLASK_ENV</i> as "test", "development" or "production".

When using a production environment, ensure there is the relevant database available specified in teh SQLALCHEMY_PROD_DATABASE_URI environment variable.


When first run, there is a root user called <i>root</i> created with a password which is specified in the <i>.env</i> file.  

#

## Usage


There are four endpoints: <b>/login/</b>, <b>/user/</b>, <b>/v1/articles/"</b> and <b>"/v1/channels/"</b>

The server will run at <u>http://localhost:5000</u> by default in development environment. The following endpoints are accessed by sending HTTP requests to this address, appended by the given names. e.g. http://localhost:5000/login/

<u>/login/</u>: 

This endpoint must be first hit to "login" the user and retrieve a token for further requests.

- Accepts a POST request with username and password provided in an Authorization header field to perform basic access authentication.
This returns a JWT (JSON web token) which must be included as value of header field <i>x-access-token</i> in subsequent requests to authenticate user.

<u>/user/</u>:

- The root user can create a new user with a POST request to the server, including the JWT as value of header field <i>x-access-token</i> + <i>username</i> and <i>password</i> specified in the JSON body. To use this new user, they must then login and retrieve a JWT as above.


<u>/v1/articles/</u>:

Implemented REST verbs/HTTP method and their corresponding functionality

Note that a unique article_id is assigned to each new article when it is entered and can be retrieved with a GET request to <b>/v1/articles/</b> endpoint


- POST: Add article provided at URL

        Required parameters
        JSON body - <string: article_url>,  e.g. {"article_url": "www.example.com"}

- GET: Get single article provided in URL or omit to request list of all

        Optional parameter
        Path parameter - <int: article_id>,  e.g. endpoint http://localhost:5000/v1/articles/1


- PUT: Add existing article into existing channel 


        Required parameters
        Path parameter - <int: article_id>,  e.g. endpoint http://localhost:5000/v1/articles/1
        JSON body - `<string: channel_name>` e.g. {"channel_name": "www.example.com"}


- PATCH: Remove an article from a channel

        Required parameters
        Path parameter - <int: article_id>,  e.g. endpoint http://localhost:5000/v1/articles/1
        JSON body - `<string: channel_name>` e.g. {"channel_name": "www.example.com"}



- DELETE: Delete provided article

        Required parameters
        Path parameter - <int: article_id>,  e.g. endpoint http://localhost:5000/v1/articles/1


<u>/v1/channels/</u>:

- POST: Add a new channel


        Required parameters
        JSON body - <string: channel_name>,  e.g. {"channel_name": "channel1"}


- GET: Pass channel_name to get info for channel otherwise return list of all channels

        Optional parameter
        Path parameter - <string: channel_name>,  e.g. endpoint http://localhost:5000/v1/channels/channel1


- PUT: Update an existing channels name 

        Required parameters
        Path parameter - <string: old_channel_name>,  e.g. endpoint http://localhost:5000/v1/channels/channel1
        JSON body - `<string: new_channel_name>` e.g. {"channel_name": "channel2"}

- DELETE: Delete channel

        Required parameters
        Path parameter - <int: channel_name>,  e.g. endpoint http://localhost:5000/v1/channels/channel1


## Notes

<u>Versioning</u>

This implementation facilitates simple versioning by minimizing code update when changing functionality at the endpoints. This uses MethodViews and blueprints to achieve this. Only v1 (version 1) is currently implemented, so the method definitions which are imported into the <i>Articles</i> and <i>Channels</i> classes all come from their respective <i>common</i> directory. To create a v2, simply replicate the pattern of <i>endpoints/{channels,articles}/v1</i> into <i>endpoints/{channels,articles}/v2</i>, importing modules from <i>endpoints/common/</i>  when needed and creating new modules for methods that should be updated under the <i>endpoints/{channels,articles}/v2</i>.
This can then be added in the app factory (Flask_REST.create_app()) and multiple versions can be running simultaneously.

<u>Testing</u>

Pytest is used as the testing framework. A basic CI pipeline is implemented with AWS Codebuild with several tests although the tests present are by no means exhaustive.
There are however 2 levels of granulity implemented - unit testing and integration testing

<u>Logging</u>

There are two loggers active - article.log and channel.log corresponding to the <i>articles</i> and <i>channels</i> endpoints respectively. The logging levels are set by environment variable. 

<u>Caching</u>

There is a simple server-side cache implemented for the POST and GET verbs on the <i>articles</i> and <i>channels</i> endpoints.
