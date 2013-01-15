Eve-Demo
========

A fully featured RESTful Web API built, deployed and powered by Eve_. 

With Eve, setting up an API is very simple. You just need a launch script
(run.py_) and a configuration module (settings.py_).
                                                       
Try it live 
----------- 
An instance of this code is running live at http://eve-demo.herokuapp.com. You
can consume the API by using cURL (see the examples below) or, if you are on
Chrome, you might want to give a shot at the Advanced REST Client extension.

There is also a sample client application available. It uses the Requests
library to consume the demo API. In fact, it has been quickly hacked togheter
to reset the API every once in a while. Check it out at
https://github.com/nicolaiarocci/eve-demo-client.
 
API Entry Point 
--------------- 
A ``GET`` request sent to the API entry point will provide a list of available
resources.

::

    $ curl -i http://eve-demo.herokuapp.com/

    HTTP/1.1 200 OK
    Cache-Control: max-age=20
    Content-Type: application/json
    Date: Thu, 22 Nov 2012 10:33:52 GMT
    Expires: Thu, 22 Nov 2012 10:34:12 GMT
    Server: Werkzeug/0.8.3 Python/2.7.2
    Content-Length: 272
    Connection: keep-alive    
    
    
    { 
        "links": [ 
            "<link rel='child' title='works' href='eve-demo.herokuapp.com/works/' />",
            "<link rel='child' title='people' href='eve-demo.herokuapp.com/people/' />" 
        ] 
    }
    
    
Each link provides two tags: ``rel``, explaining the relation between the
linked resource and current endpoint, and ``title``, containing the linked
resource name. Togheter these two informations allow the client to eventually
update its UI and/or transverse the API without any prior knoweledge of its
structure. HATEOAS is at work here: a ``links`` section is included with
every response provided by any Eve-powered API.

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

    <response>
        <links>
            <link><link rel='child' title='works' href='eve-demo.herokuapp.com/works/' /></link>
            <link><link rel='child' title='people' href='eve-demo.herokuapp.com/people/' /></link>
        </links>
    </response>

We requested XML this time. API responses will be rendered in JSON or XML
depending on the requested mime-type. 

Resource Endpoints
------------------
We can of course send requests to resource endpoints. With the previous request
we learned that there is a ``people`` resource available:

::

    $ curl -i http://eve-demo.herokuapp.com/people/

    HTTP/1.0 200 OK
    Last-Modified: Thu, 22 Nov 2012 10:11:12 UTC
    (...)

    {
        "links": [
            "<link rel='parent' title='home' href='eve-demo.herokuapp.com' />",
            "<link rel='collection' title='people' href='eve-demo.herokuapp.com/people/' />"
        ],
        "items": [
            {
                "updated": "Thu, 22 Nov 2012 10:11:12 UTC",
                "firstname": "Mark",
                "created": "Thu, 22 Nov 2012 10:11:12 UTC",
                "lastname": "Green",
                "born": "Sat, 23 Feb 1985 12:00:00 UTC",
                "etag": "77b0a15eaa65027685fe21482937ac2e185c695f",
                "role": [
                    "copy",
                    "author"
                ],
                "location": {
                    "city": "New York",
                    "address": "4925 Lacross Road"
                },
                "link": "<link rel='self' title='person' href='eve-demo.herokuapp.com/people/50adfa4038345b1049c88a37/' />",
                "_id": "50adfa4038345b1049c88a37"
            },
            {
                "updated": "Thu, 22 Nov 2012 10:11:12 UTC",
                "firstname": "Anne",
                "created": "Thu, 22 Nov 2012 10:11:12 UTC",
                "lastname": "White",
                "born": "Fri, 25 Sep 1970 10:00:00 UTC",
                "etag": "990ea0b937347269d43f748179be67062f1417d5",
                "role": [
                    "contributor",
                    "copy"
                ],
                "location": {
                    "city": "Ashfield",
                    "address": "32 Joseph Street"
                },
                "link": "<link rel='self' title='person' href='eve-demo.herokuapp.com/people/50adfa4038345b1049c88a38/' />",
                "_id": "50adfa4038345b1049c88a38"
            },
            ( ... )
            ]
    }

Each resource item is provided with some important additional fields, all
automatically handled by the API: 

=========== =================================================================
Field       Description
=========== =================================================================
``created`` document creation date
``updated`` document last update
``etag``    ETag to be used for concurrency control and conditional requests. 
``_id``     unique document key, needed to access the indivdual item endpoint
=========== =================================================================

Conditional requests
::::::::::::::::::::
In the above response, a ``Last-Modified`` header is included. It can be used
later to retrieve only the items that have changed since:

::

    $ curl -H "If-Modified-Since: Thu, 22 Nov 2012 10:11:12 UTC" -i http://eve-demo.herokuapp.com:5000/people/

    HTTP/1.0 200 OK
    ( ... )

    {
        "items": [],
        "links": [
            "<link rel='child' title='works' href='eve-demo.herokuapp.com/works/' />",
            "<link rel='child' title='people' href='eve-demo.herokuapp.com/people/' />"
        ]
    }

This time we didn't get any item back, as none has changed since the previous
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
            "link": "<link rel='self' title='person' href='eve-demo.herokuapp.com/people/50ae43339fa12500024def5b/' />"
        },
        "item1": {
            "status": "OK",
            "updated": "Thu, 22 Nov 2012 15:22:27 UTC",
            "_id": "50ae43339fa12500024def5c",
            "link": "<link rel='self' title='person' href='eve-demo.herokuapp.com/people/50ae43339fa12500024def5c/' />"
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
            "link": "<link rel='self' title='person' href='eve-demo.herokuapp.com/people/50ae44c49fa12500024def5d/' />"
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
    ( ... )

    {
        "links": [
            "<link rel='parent' title='home' href='eve-demo.herokuapp.com' />",
            "<link rel='collection' title='people' href='eve-demo.herokuapp.com/people/' />"
        ],
        "item": {
            "updated": "Wed, 21 Nov 2012 16:04:56 UTC",
            "firstname": "John",
            "created": "Wed, 21 Nov 2012 16:04:56 UTC",
            "lastname": "Doe",
            "born": "Thu, 27 Aug 1970 14:37:13 UTC",
            "role": [
                "author"
            ],
            "location": {
                "city": "Auburn",
                "address": "422 South Gay Street"
            },
            "link": "<link rel='self' title='person' href='eve-demo.herokuapp.com/people/50acfba938345b0978fccad7/' />",
            "_id": "50acfba938345b0978fccad7"
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
    (...)

    {
        "data": {
            "status": "OK",
            "updated": "Fri, 23 Nov 2012 08:11:19 UTC",
            "_id": "50adfa4038345b1049c88a37",
            "link": "<link rel='self' title='person' href='eve-demo.herokuapp.com/people/50adfa4038345b1049c88a37/' />",
            "etag": "372fbbebf54dfe61742556f17a8461ca9a6f5a11"
        }
    }

Right on! This time we got our patch in, and the server returned the new ETag.
We also get the new ``updated`` value, which eventually will allow us to
perform ``If-Modified-Since`` requests.

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
