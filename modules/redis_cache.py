import json
from redis import ConnectionPool, Redis
from config import config


class RedisCache:
    pool = None

    def __init__(self):
        """
        Create a connection pool
        Get the decoding format
        """
        self.pool = ConnectionPool(host=config.host, port=config.port, db=config.db)
        self.redis_server_connection = Redis(connection_pool=self.pool)
        self.decoding = config.decoding

    def set_data(self, user_id, dictionary):
        """
        :param user_id: unique user_id with which each key is identified
        :type user_id: string
        :param dictionary: contains epoch time with counter
        :type dictionary: dict
        """
        converted_dictionary = json.dumps(dictionary)
        self.redis_server_connection.set(user_id, converted_dictionary)

    def get_data(self, user_id):
        """
        :param user_id: unique user_id with which each key is identified
        :type user_id: string
        :return: if user found return dictionary or False
        :rtype: dict or bool
        """
        if self.redis_server_connection.exists(user_id):
            return json.loads(self.redis_server_connection.get(user_id).decode(self.decoding))
        return False
