from redis.connection import Connection, DefaultParser


class CustomConnection(Connection):
    """Manages TCP communication to and from a Redis server

    This object defaults timeouts to 1.0 seconds so that attempting a
    connection to the Redis server doesn't take an extremely long time in cases
    where the	connection cannot be made.
    """

    def __init__(self, host='localhost', port=6379, db=0, password=None,
                 socket_timeout=1.0, socket_connect_timeout=1.0,
                 socket_keepalive=False, socket_keepalive_options=None,
                 socket_type=0, retry_on_timeout=False, encoding='utf-8',
                 encoding_errors='strict', decode_responses=False,
                 parser_class=DefaultParser, socket_read_size=65536,
                 health_check_interval=0, client_name=None, username=None):
        super(CustomConnection, self).__init__(
          host, port, db, password, socket_timeout, socket_connect_timeout,
          socket_keepalive, socket_keepalive_options, socket_type,
          retry_on_timeout, encoding, encoding_errors, decode_responses,
          parser_class, socket_read_size, health_check_interval, client_name,
          username
        )
