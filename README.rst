Eve-Demo
========

A demostration of a simple REST Web API powered by Eve.

Try it live
-----------
An instance of this code is running at http://eve-demo.herokuapp.com: 

::
    $ curl -H 'Accept: application/json' http://eve-demo.herokuapp.com -i

    HTTP/1.0 200 OK
    Content-Type: application/json; charset=utf-8
    Content-Length: 285
    Server: Werkzeug/0.8.3 Python/2.7.3
    Date: Tue, 20 Nov 2012 10:15:21 GMT

    {
    "response": {"links": ["<link rel='child' title='works' href='<link
    rel='collection' title='works' href='localhost:5000/works/' />' />", "<link
    rel='child' title='people' href='<link rel='collection' title='people'
    href='localhost:5000/people/' />' />"]}}

If you use Chrome, you may also use the phenomenal Advanced REST Client
extension to play with the API.


