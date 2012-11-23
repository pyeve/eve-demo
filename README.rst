Eve-Demo
========

A fully featured RESTful Web API built, deployed and powered by Eve_ 
                                                       
Try it live
-----------
An instance of this code is running live at http://eve-demo.herokuapp.com. You
can consume the API by using cURL (see the examples below) or, if you are on
Chrome, you might want to give a shot at the phenomenal Advanced REST Client
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
a ``people`` resource available:

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

