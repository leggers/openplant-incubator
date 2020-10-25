#!/usr/env/bin python

import os

def get_connection_string():
    components = [
        os.environ['DB_DRIVER'], '://',
        os.environ['DB_USER'], ':',
        os.environ['DB_PASSWORD'], '@',
        os.environ['DB_HOST'], ':',
        os.environ['DB_PORT'], '/',
        os.environ['DB_NAME']
    ]
    connection_string = ''.join(components)
<<<<<<< HEAD
    print(connection_string)
=======
>>>>>>> 734680c73235e67b40072fbdf403f1a9a47e9ca7
    return connection_string
