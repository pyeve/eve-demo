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

