# -*- coding: utf-8 -*-

"""
    Eve Demo
    ~~~~~~~~

    A demostration of a simple API powered by Eve REST API.

    The live demo is available at eve-demo.herokuapp.com. Please keep in mind
    that the it is running on Heroku's free tier using a free MongoHQ
    sandbox, which menas that the first request to the service will probably
    take some time, and the overall performance will probably be poor. Also,
    the database gets a reset every now and then.

    :copyright: (c) 2012 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os
from eve import Eve

if __name__ == '__main__':
    # Heroku support: bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app = Eve()
    app.run(host='0.0.0.0', port=port)
