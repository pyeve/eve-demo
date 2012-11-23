Eve-Demo
========

A fully featured RESTful Web API built, deployed and powered by Eve_ 
                                                       
Try it live
-----------
An instance of this code is running live at http://eve-demo.herokuapp.com. You
can consume the API by using cURL (see the examples below) or, if you are on
Chrome, you might want to give a shot at the phenomenal Advanced RET Client
extension.

API entry point
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
        "response": {
            "links": [
                "<link rel='child' title='works' href='eve-demo.herokuapp.com/works/' />", 
                "<link rel='child' title='people' href='eve-demo.herokuapp.com/people/' />"
                ]
            }
    }
    
    
Each link provides two tag: ``rel``, explaining the relation between the linked
resource and current endpoint, and ``title``, containing the linked resource
name. Togheter, these two informations allow the client to eventually update
its UI and/or transverse the API without prior knoweledge of its structure.
HATEOAS is at work here. A ``links`` section is included with every response
provided by any Eve-powered API.

Cache Control
:::::::::::::
Also notice how the response header contains cache-control directives
(``Cache-Control``, ``Expires``). Any Eve-powered API can easily control the
values of these directives. It is possibile to setup a global value for both,
and it is also possible to override the global settings for individual resource
endpoints.  

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
            <link><link rel='child' title='works' href='localhost:5000/works/' /></link>
            <link><link rel='child' title='people' href='localhost:5000/people/' /></link>
        </links>
    </response>

We requested XML this time. API responses will be rendered in JSON or XML, with
JSON being the default, depending on the requested mime-type. This behavior is
provided automatically by any EVe-powered API.

Resource Endpoints
------------------
Besides the API homepage (the entry point), we can of course send requests to
resource endpoints. We learned from the previous request that there's
a `people` resource available:

::

    $ curl -i http://eve-demo.herokuapp.com/people/

    HTTP/1.0 200 OK
    Last-Modified: Thu, 22 Nov 2012 10:11:12 UTC
    (...)

    {
        "response": {
            "links": [
                "<link rel='parent' title='home' href='localhost:5000' />",
                "<link rel='collection' title='people' href='localhost:5000/people/' />"
            ],
            "people": [
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
                    "link": "<link rel='self' title='person' href='localhost:5000/people/50adfa4038345b1049c88a37/' />",
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
                    "link": "<link rel='self' title='person' href='localhost:5000/people/50adfa4038345b1049c88a38/' />",
                    "_id": "50adfa4038345b1049c88a38"
                },
                ( ... )
            ]
        }
    }

Each resource item is provided with some important, additional fields: 

=========== =================================================================
Field       Description
=========== =================================================================
``created`` document creation date
``updated`` document last update
``etag``    ETag to be used for concurrency control and conditional requests. 
            An hash of the current representation of the document.
``_id``     unique document key, needed to access the indivdual item endpoint
=======     =================================================================

All these fields are automatically handled by the API. 

Conditional requests
::::::::::::::::::::
In the above response, a ``Last-Modified`` header is included. It can be used later to
retrieve only the items that have changed since the last request.::

    $ curl -H "If-Modified-Since: Thu, 22 Nov 2012 10:11:12 UTC" -i http://eve-demo.herokuapp.com:5000/

    HTTP/1.0 200 OK
    ( ... )

    {
        "response": {
            "links": [
                "<link rel='child' title='works' href='localhost:5000/works/' />",
                "<link rel='child' title='people' href='localhost:5000/people/' />"
            ]
        }
    }

This time we didn't get any item back, as none has been changed since
our previous request. 

Filtering and sorting
:::::::::::::::::::::
Eve-powered APIs support several kinds of conditional requests. Besides the
``If-Modified-Since`` header, you can also submit queries. There are two
supported query syntaxes, the MongoDB query syntax

::
    $ curl -i http://eve-demo.herokuapp.com/people/?where={"lastname": "Doe"}

and the native Python syntax

::

    $ curl -i http://eve-demo.herokuapp.com/people/?where=lastname=="Doe"

Sorting is supported as well

::

    $ curl -i http://eve-demo.herokuapp.com/people/?sort={"lastname": -1}


Currently you provide a sort directive by using a pure MongoDB syntax; support
for a more general syntax (``sort=lastname``) is planned as well.

Pagination
::::::::::
In order to save bandwith and resources, pagination is enabled by default. You
have control on the default page size, and the maximum number of items
per page that the consumer is allowed to request.

::

    $ curl -i http://eve-demo.herokuapp.com/people/?max_results=20&page=2

Of course you can mix all the available query parameters

::
    $ curl -i http://eve-demo.herokuapp.com/people/?where={"lastaname":
    "Doe"}&sort={"firstname"}&page=5

Multiple inserts
::::::::::::::::
Insertion is done at the resource endpoint via POST. Multiple items can be
inserted with a single request. 

::
    curl -d 'item1={"firstname": "barack", "lastname": "obama"}' -d 'item2={"firstname": "mitt", "lastname": "romney"}' http://eve-demo.herokuapp.com/people/

    {
        "response": {
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
    }

The response will contain a status update for each item. If the insertion
succeeded, item status will include the update/creation date, the new unique id
and a link to the item endpoint.

The API mantainer controls wether insertion is allowed. By default, APIs
are read-only.

Data validation
***************
If an item doesn't validate against the validation rules it won't be inserted.
All the request is always processed; validation errors on certain items won't
prevent the insertion of others included in the request.

::

    curl -d 'item1={"firstname": "bill", "lastname": "clinton"}' -d 'item2={"firstname": "mitt", "lastname": "romney"}' http://eve-demo.herokuapp.com/people/
    {
        "response": {
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
    }

In the example above, `item2` got a validation error and was not inserted,
while `item1` was successfully inserted. API maintainer has complete control on
data validation. Since Eve validation is based on Cerberus_, it is also
possible to extend the system to suit specific use cases. Check out the
settings.py_ module used in this demo to get an idea of how data structures are
configured in any Eve-powered API.

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
Item endpoints are accessed by combining the parent resource URI and the item
unique key.

::
    $ curl -i http://eve-demo.herokuapp.com/people/50acfba938345b0978fccad7/

If enabled by the API mantainer, it is also possibile to access the same item
with a secondary field value:

::
    $ curl -i http://eve-demo.herokuapp.com/people/Doe/

    HTTP/1.0 200 OK
    Etag: 28995829ee85d69c4c18d597a0f68ae606a266cc
    Last-Modified: Wed, 21 Nov 2012 16:04:56 UTC 
    ( ... )

    {
        "response": {
            "links": [
                "<link rel='parent' title='home' href='eve-demo.herokuapp.com' />",
                "<link rel='collection' title='people' href='eve-demo.herokuapp.com/people/' />"
            ],
            "people": {
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
    }


Editing and deleting items
::::::::::::::::::::::::::
Concurrency Control
~~~~~~~~~~~~~~~~~~~
The header provided with the above response contains an ``ETag`` which is very
important, because etags are mandatory for performing edit and delete
operations on the items.  Editing happens at item endpoint and is allowed only
if the request includes an ``ETag`` matching the current representation of the
item on the server. This prevents overwriting the current item with obsolete
versions.

::
    $ curl -X PATCH -i http://localhost:5000/people/50adfa4038345b1049c88a37/ -d 'data={"firstname": "ronald"}'

    HTTP/1.0 403 FORBIDDEN

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>403 Forbidden</title>
    <h1>Forbidden</h1>
    <p>You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.</p>

We did not provide an ETag for the item we are attempting to edit so we got
a nice 403 back. Let's try again:

::
    $ curl -H "If-Match: 1234567890123456789012345678901234567890" -X PATCH -i http://localhost:5000/people/50adfa4038345b1049c88a37/ -d 'data={"firstname": "ronald"}'

    HTTP/1.0 412 PRECONDITION FAILED

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>412 Precondition Failed</title>
    <h1>Precondition Failed</h1>

What went wrong this time? We did provide the mandatory ``If-Match`` header,
but it's value did not match the ETag computed on the representation of the
item on the server, which granted us a 412. Again!

::
    $ curl -H "If-Match: 80b81f314712932a4d4ea75ab0b76a4eea613012" -X PATCH -i http://localhost:5000/people/50adfa4038345b1049c88a37/ -d 'data={"firstname": "ronald"}'

    HTTP/1.0 200 OK
    ETag: 372fbbebf54dfe61742556f17a8461ca9a6f5a11
    Last-Modified: Fri, 23 Nov 2012 08:11:19 UTC
    (...)

    {
        "response": {
            "data": {
                "status": "OK",
                "updated": "Fri, 23 Nov 2012 08:11:19 UTC",
                "_id": "50adfa4038345b1049c88a37",
                "link": "<link rel='self' title='person' href='localhost:5000/people/50adfa4038345b1049c88a37/' />",
                "etag": "372fbbebf54dfe61742556f17a8461ca9a6f5a11"
            }
        }
    }

Right on! This time we got our patch in and the server returned the new ETag.
We also get the new ``updated`` value, which eventually will allow us to
perform ``If-Modified-Since`` requests.

.. _Eve: https://github.com/nicolaiarocci/eve
.. _Cerberus: https://github.com/nicolaiarocci/cerberus
.. _settings.py: https://github.com/nicolaiarocci/eve-demo/blob/master/settings.py
