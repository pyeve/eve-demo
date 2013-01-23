Eve-Demo
========

A fully featured RESTful Web API powered by Eve_. With Eve setting up an API is
very simple. You just need a launch script (run.py_) and a configuration module
(settings.py_).

*Note*. The demo is currently running v0.0.3 of the Eve framework. Eve-Demo is
only updated when major Eve updates are released. Please refer to the official
Eve repository for an up-to-date features list. 

Try it live 
----------- 
An instance of this code is running live at http://eve-demo.herokuapp.com. You
can consume the API by using cURL or, if you are on Chrome, you might want to
give a shot at the Advanced REST Client extension.

There is also a sample client application available. It uses the Requests
library to consume the demo. In fact it has been quickly hacked togheter to
reset the API every once in a while. Check it out at
https://github.com/nicolaiarocci/eve-demo-client.
 
API Entry Point 
--------------- 
A ``GET`` request sent to the API entry point (the `home page`) will obtain
a list of available resources:

::

    $ curl -i http://eve-demo.herokuapp.com/

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 131
    Cache-Control: max-age=20
    Expires: Tue, 22 Jan 2013 09:34:34 GMT
    Server: Eve/0.0.3 Werkzeug/0.8.3 Python/2.7.3
    Date: Tue, 22 Jan 2013 09:34:14 GMT

    {
        "_links": {
            "child": [
                {"href": "eve-demo.herokuapp.com/works/", "title": "works"}, 
                {"href": "eve-demo.herokuapp.com/people/", "title": "people"}
            ]
        }
    }   
    
Every API endpoint exposes a ``_links`` dictionary containing one or more links
to related resources. Dictionary keys express the relation (``rel``) between
the resource and the endpoint. Values can be lists of links (such as in this
case) or a single link. Links are dictionaries themselves where ``title``
is the `human readable` resource name and ``href`` the actual link to the
resource. Links allow the client to eventually update its UI and/or transverse
the API without any prior knoweledge of its structure: HATEOAS_ is at work here.

Cache Control
:::::::::::::
Notice how the response header contains cache-control directives
(``Cache-Control``, ``Expires``). Any Eve-powered API can easily control the
values of these, both at global and individual endpoint level.

JSON and XML rendering
::::::::::::::::::::::
Since we did not provide an ``Accept`` header with our request, the
API responded with the default ``Content-Type``: JSON. 

::

    $ curl -H "Accept: application/xml" -i http://eve-demo.herokuapp.com/

    HTTP/1.0 200 OK
    Content-Type: application/xml; charset=utf-8
    ...

    <resource>
        <link rel="child" href="localhost:5000/works/" title="works" />
        <link rel="child" href="localhost:5000/people/" title="people" />
    </resource>

We requested XML this time. API responses will be rendered in JSON or XML
depending on the requested mime-type. 

Resource Endpoints
------------------
Clients can of course send requests to resource endpoints. With the previous
request we learned that a ``people`` resource is available. Let's get it:

::

    $ curl -i http://eve-demo.herokuapp.com/people/

    Content-Type: application/json
    Content-Length: 2392
    Cache-Control: max-age=20
    Expires: Tue, 22 Jan 2013 10:04:43 GMT
    Last-Modified: Wed, 05 Dec 2012 09:53:07 UTC
    Server: Eve/0.0.3 Werkzeug/0.8.3 Python/2.7.3
    Date: Tue, 22 Jan 2013 10:04:23 GMT

    
    {
        "_items": [
            {
                "firstname": "Mark", 
                "lastname": "Green", 
                "born": "Sat, 23 Feb 1985 12:00:00 UTC", 
                "role": ["copy", "author"], 
                "location": {"city": "New York", "address": "4925 Lacross Road"}, 
                "_id": "50bf198338345b1c604faf31",
                "updated": "Wed, 05 Dec 2012 09:53:07 UTC", 
                "created": "Wed, 05 Dec 2012 09:53:07 UTC", 
                "etag": "ec5e8200b8fa0596afe9ca71a87f23e71ca30e2d", 
                "_links": {
                    "self": {"href": "localhost:5000/people/50bf198338345b1c604faf31/", "title": "person"},
                },
            },
            {
                "firstname": "Anne", 
                "updated": "Wed, 05 Dec 2012 09:53:07 UTC",
                ...
            } ,
            ...
        ],
        "_links": {
            "self": {"href": "localhost:5000/people/", "title": "people"}, 
            "parent": {"href": "localhost:5000", "title": "home"}
        }
    }


The ``_items`` list contains the requested data. Along with its own fields,
each item provides some important, additional fields:

=========== =================================================================
Field       Description
=========== =================================================================
``created`` item creation date.
``updated`` item last updated on.
``etag``    ETag, to be used for concurrency control and conditional requests. 
``_id``     unique item key, also needed to access the indivdual item endpoint.
=========== =================================================================

These additional fields are automatically handled by the API (clients don't
need to provide them when adding/editing resources).

Conditional requests
::::::::::::::::::::
In the above response, a ``Last-Modified`` header is included. It can be used
later to retrieve only the items that have changed since:

::

    $ curl -H "If-Modified-Since: Wed, 05 Dec 2012 09:53:07 UTC" -i http://eve-demo.herokuapp.com:5000/people/

    HTTP/1.0 200 OK
    ...

    {
        "_items": [],
        "_links": [..]
    }

This time we didn't get any item back as none has changed since the previous
request. 

Filtering and sorting
:::::::::::::::::::::
Eve-powered APIs support several kinds of conditional requests. Besides the
``If-Modified-Since`` header, you can also submit queries. There are two
supported query syntaxes, the MongoDB query syntax:

::

    $ curl -i http://eve-demo.herokuapp.com/people/?where={"lastname": "Doe"}

and the native Python syntax:

::

    $ curl -i http://eve-demo.herokuapp.com/people/?where=lastname=="Doe"

Sorting is supported as well:

::

    $ curl -i http://eve-demo.herokuapp.com/people/?sort={"lastname": -1}


Currently sort directives use a pure MongoDB syntax; support for a more general
syntax (``sort=lastname``) is planned.

Pagination
::::::::::
In order to save bandwith and resources, pagination is enabled by default. You
have control on the default page size and the maximum number of items per page.

::

    $ curl -i http://eve-demo.herokuapp.com/people/?max_results=20&page=2

Of course you can mix all the available query parameters:

::

    $ curl -i http://eve-demo.herokuapp.com/people/?where={"lastaname": "Doe"}&sort={"firstname"}&page=5

Multiple inserts
::::::::::::::::
Insertion is done at the resource endpoint via POST. Multiple items can be
inserted with a single request. 

::

    curl -d 'item1={"firstname": "barack", "lastname": "obama"}' -d 'item2={"firstname": "mitt", "lastname": "romney"}' http://eve-demo.herokuapp.com/people/

    {
        "item2": {
            "status": "OK",
            "updated": "Thu, 22 Nov 2012 15:22:27 UTC",
            "_id": "50ae43339fa12500024def5b",
            "_links": {"self": {"href": "eve-demo.herokuapp.com/people/50ae43339fa12500024def5b/", "title": "person"}}
        },
        "item1": {
            "status": "OK",
            "updated": "Thu, 22 Nov 2012 15:22:27 UTC",
            "_id": "50ae43339fa12500024def5c",
            "_links": {"self": {"href": "eve-demo.herokuapp.com/people/50ae43339fa12500024def5c/", "title": "person"}}
        }
    }

The response will contain a status update for each item inserted. If the
insertion succeeded, item status will include the update/creation date, the new
unique id and a link to the item endpoint.

The API mantainer controls wether insertion is allowed. By default, APIs
are read-only.

Data validation
***************
An item won't be inserted if it doesn't validate against the validation rules
set by the API maintainer. The whole the request is always processed, which
means that eventual validation errors won't prevent insertion of valid
items.

::

    curl -d 'item1={"firstname": "bill", "lastname": "clinton"}' -d 'item2={"firstname": "mitt", "lastname": "romney"}' http://eve-demo.herokuapp.com/people/
    {
        "item2": {
            "status": "ERR",
            "issues": [
                "value 'romney' for field 'lastname' not unique"
            ]
        },
        "item1": {
            "status": "OK",
            "updated": "Thu, 22 Nov 2012 15:29:08 UTC",
            "_id": "50ae44c49fa12500024def5d",
            "_links": {"self": {"href": "eve-demo.herokuapp.com/people/50ae44c49fa12500024def5d/", "title": "person"}}
        }
    }

In the example above, ``item2`` did not validate and was rejected, while
``item1`` was successfully created. API maintainer has complete control on
data validation. Since Eve validation is based on Cerberus_, it is also
possible to extend the system to suit specific use cases. Check out the
settings.py_ module used in this demo to get an idea of how data structures are
configured.

Resource Deletion
*****************
If enabled by the maintainer, an Eve-powered API will also allow deletion of
the whole content of a resource.

::

    $ curl -X DELETE http://eve-demo.herokuapp.com/people/

Again, Eve-powered APIs are read-only by default. Enabling/disabling features
is just a matter of setting the appropriate value in the configuration module.

Item Endpoints
--------------
Item endpoints are accessed by combining parent resource URI and item unique
key.

::

    $ curl -i http://eve-demo.herokuapp.com/people/50acfba938345b0978fccad7/

If enabled by the API mantainer, it is also possibile to access the same item
with a secondary field value (in our case, ``lastname``):

::

    $ curl -i http://eve-demo.herokuapp.com/people/Doe/

    HTTP/1.0 200 OK
    Etag: 28995829ee85d69c4c18d597a0f68ae606a266cc
    Last-Modified: Wed, 21 Nov 2012 16:04:56 UTC 
    ... 

    {
        "firstname": "John",
        "lastname": "Doe",
        "born": "Thu, 27 Aug 1970 14:37:13 UTC",
        "role": ["author"],
        "location": {"city": "Auburn", "address": "422 South Gay Street"},
        "_id": "50acfba938345b0978fccad7"
        "updated": "Wed, 21 Nov 2012 16:04:56 UTC",
        "created": "Wed, 21 Nov 2012 16:04:56 UTC",
        "_links": {
            "self": {"href": "eve-demo.herokuapp.com/people/50acfba938345b0978fccad7/", "title": "person"},
            "parent": {"href": "eve-demo.herokuapp.com/", "title": "home"},
            "collection": {"href": "http://eve-demo.herokuapp.com/people/", "title": "people"}
        }
    }


Editing and deleting items
::::::::::::::::::::::::::

Concurrency Control
*******************
The header provided with the above response contains an ``ETag`` which is very
important because etags are mandatory for performing edit and delete
operations on items. Editing happens at the item endpoint and is allowed only
if the request includes an ``ETag`` that matches the current representation
stored on the server. This prevents overwriting the items with obsolete
versions.

::

    $ curl -X PATCH -i http://eve-demo.herokuapp.com/people/50adfa4038345b1049c88a37/ -d 'data={"firstname": "ronald"}'

    HTTP/1.0 403 FORBIDDEN

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>403 Forbidden</title>
    <h1>Forbidden</h1>
    <p>You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.</p>

We did not provide an ETag for the item so we got a not-so-nice ``403
FORBIDDEN``. Let's try again:

::

    $ curl -H "If-Match: 1234567890123456789012345678901234567890" -X PATCH -i http://eve-demo.herokuapp.com/people/50adfa4038345b1049c88a37/ -d 'data={"firstname": "ronald"}'

    HTTP/1.0 412 PRECONDITION FAILED

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>412 Precondition Failed</title>
    <h1>Precondition Failed</h1>

What went wrong this time? We did provide the mandatory ``If-Match`` header,
but it did not match the ETag computed on the representation of the current
item, so we got a ``402 PRECONDITION FAILED``. Again!

::

    $ curl -H "If-Match: 80b81f314712932a4d4ea75ab0b76a4eea613012" -X PATCH -i http://eve-demo.herokuapp.com/people/50adfa4038345b1049c88a37/ -d 'data={"firstname": "ronald"}'

    HTTP/1.0 200 OK
    ETag: 372fbbebf54dfe61742556f17a8461ca9a6f5a11
    Last-Modified: Fri, 23 Nov 2012 08:11:19 UTC
    ...

    {
        "data": {
            "status": "OK",
            "updated": "Fri, 23 Nov 2012 08:11:19 UTC",
            "_id": "50adfa4038345b1049c88a37",
            "etag": "372fbbebf54dfe61742556f17a8461ca9a6f5a11"
            "_links": {"self": "..."}
        }
    }

This time we got our patch in, and the server returned the new ETag.  We also
get the new ``updated`` value, which eventually will allow us to perform
subsequent ``If-Modified-Since`` requests.

Local install
-------------
If you want to play with this app locally create a virtualenv environment and
once activated install Eve:

::

    $ pip install eve
Then, just clone this repository:

::

    git clone https://github.com/nicolaiarocci/eve-demo.git
    
Of course you need a local instance of MongoDB running, and don't forget to
ajust the settings.py_ module accordingly.  Launching the API is
straightforward:

::

    python run.py

Have fun!

Wrapping it up
--------------
Check out the settings.py_ module used in this demo to get an idea of how
configuration is handled. Also don't forget to visit Eve_
repository and, if you need a gentle introduction to the wondeful world of
RESTful WEB APIs, check out my EuroPython 2012 talk: `Developing RESTful Web
APIs with Python, Flask and MongoDB
<https://speakerdeck.com/nicola/developing-restful-web-apis-with-python-flask-and-mongodb>`_
- *thank you*.

.. _Eve: https://github.com/nicolaiarocci/eve
.. _Cerberus: https://github.com/nicolaiarocci/cerberus
.. _run.py: https://github.com/nicolaiarocci/eve-demo/blob/master/run.py
.. _settings.py: https://github.com/nicolaiarocci/eve-demo/blob/master/settings.py
.. _HATEOAS: http://en.wikipedia.org/wiki/HATEOAS
