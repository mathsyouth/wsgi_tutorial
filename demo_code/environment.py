# Python's bundled WSGI server
from wsgiref.simple_server import make_server

def application(environ, start_response):
    """The application interface is a callable object

    :param environ: points to a dictionary containing CGI like environment
        variables which is populated by the server for each received request
        from the client.
    :param start_response: is a callback function supplied by the server
        which takes the HTTP status and headers as arguments.
    """
    # Build the response body possibly using the supplied environ dictionary
    # Sorting and stringifying the environment key, value pairs
    response_body = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)
    # Adding strings to the response body
    response_body = [
        'The Beggining\n',
        '*' * 30 + '\n',
        response_body,
        '\n' + '*' * 30 ,
        '\nThe End'
    ]
    # So the content-lenght is the sum of all string's lengths
    content_length = sum([len(s) for s in response_body])

    # HTTP response code and message
    status = '200 OK'

    # HTTP headers expected by the client
    # They must be wrapped as a list of tupled pairs: [(Header name, Header value)].
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(content_length))
    ]

    # Send them to the server using the supplied function
    start_response(status, response_headers)

    # Return the response body. Notice it is wrapped
    # in a list although it could be any iterable.
    return [i.encode("utf-8") for i in response_body]

# Instantiate the server
httpd = make_server(
    'localhost', # The host name
    8051, # A port number where to wait for the request
    application # The application object name, in this case a function
)

# Wait for a single request, serve it and quit
httpd.handle_request()