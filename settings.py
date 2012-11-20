# -*- coding: utf-8 -*-

"""
    eve-demo settings
    ~~~~~~~~~~~~~~~~~

    Settings file for our little demo.

    PLEASE NOTE: We don't need to create the two collections in MongoDB.
    Actually, we don't even need to create the database: GET requests on an
    empty/non-existant DB will be served correctly ('200' OK with an empty
    collection); DELETE/PATCH will receive appropriate responses ('404' Not
    Found), and POST requests will create database and collections when needed.
    Keep in mind however that such an auto-managed database will most likely
    perform poorly since it lacks any sort of optimized index.

    :copyright: (c) 2012 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os

# We want to seamlessy run ouw API both locally and on Heroku so:
if os.environ.get('PORT'):
    # We're hosted on Heroku!
    # Use the MongoHQ sandbox as our backend.
    MONGO_HOST = 'alex.mongohq.com:10047/app9346575'
    MONGO_PORT = 10047
    MONGO_USERNAME = 'evedemo'
    MONGO_PASSWORD = 'evedemo'

    # also, correctly set the API entry point
    SERVER_NAME = 'eve-demo.herokuapp.com'
else:
    # Running on local machine.
    # Let's just use the local mongod instance as our backend.
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'user'
    MONGO_PASSWORD = 'user'

    # let's not forget the API entry point
    SERVER_NAME = 'localhost:5000'

MONGO_DBNAME = 'evedemo'

# Enable both reads (GET) and multiple inserts (POST) at resource level
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the resource endpoint).
RESOURCE_METHODS = ['GET', 'POST']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (if you omits this, it will default to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these settings later, at resource detail.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Our API will expose two resources: 'people' and 'works'.
# In order to allow for proper data validation, let's define their beaviour
# and structure (the 'scheme').

people = {
    # the value of the 'title' tag when referencing an individual resource
    # item in a link.
    'item_title': 'person',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point so clients can also use
    # '/people/person/<lastname>/'.
    'additional_lookup': {
        'url': '[\w]+',
        'field': 'lastname'
    },

    # finally, let's define the field schema.
    'schema': {
        'firstname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 10,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,

            # talk about hard constraints! But in this demo 'lastname' is also
            # an item entry-point so we want them to be unique.
            'unique': True,
        },
        # 'role' is a list, and can only contain values from 'allowed'.
        'role': {
            'type': 'list',
            'allowed': ["author", "contributor", "copy"],
        },
        # An embedded 'strongly-typed' dictionary.
        'location': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'}
            },
        },
        'born': {
            'type': 'datetime',
        },
    }
}

works = {
    # if 'item_title' is not provided Eve will just strip the final
    # 's' from resource name and use if as title, which is fine here.
    #'item_title': 'work',

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        'title': {
            'type': 'string',
            'required': True,
        },
        'description': {
            'type': 'string',
        },
        'owner': {
            'type': 'objectid',
            'required': True,
        },
        # An optional list of contributors. Each list item is an ObjectId.
        'contributors': {
            'type': [{'type': 'objectid'}]
        },
    }
}
DOMAIN = {
    'people': people,
    'works': works,
}
