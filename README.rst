Eve-Demo
========

A fully featured RESTful Web API powered by Eve_. With Eve setting up an API is
very simple. You just need a launch script (run.py_) and a configuration file
(settings.py_). Check out the settings.py_ module in this repo to get an idea
of how configuration is handled. Don't forget to visit Eve_ website for
a complete list of features and examples. 

If you need a gentle introduction to the wondeful world of RESTful WEB APIs,
check out my EuroPython 2012 talk: `Developing RESTful Web APIs with Python,
Flask and MongoDB
<https://speakerdeck.com/nicola/developing-restful-web-apis-with-python-flask-and-mongodb>`_

There is also a sample client application available. It uses the Requests
library to consume the demo. In fact it has been quickly hacked together to
reset the API every once in a while. Check it out at
https://github.com/nicolaiarocci/eve-demo-client.
 
*Note*. The demo is currently running v0.0.4 of the Eve framework. Eve-Demo is
only updated when major Eve updates are released. Please refer to the official
Eve repository for an up-to-date features list. 

.. _Eve: http://python-eve.org
.. _run.py: https://github.com/nicolaiarocci/eve-demo/blob/master/run.py
.. _settings.py: https://github.com/nicolaiarocci/eve-demo/blob/master/settings.py
