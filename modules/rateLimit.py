import time
import logging
from logging.config import fileConfig
from modules.redis_cache import RedisCache


class SlidingWindowRateLimit:
    def __init__(self, threshold, window_size):
        """
        For initialization of class objects
        """
        logging.config.fileConfig('config/logging.cfg')
        self.threshold = threshold
        self.window_size = window_size
        self.rediscache = RedisCache()

    def validate_request_rate_limit(self, user_id):
        """
        Check if the incoming request has crossed the limit
        :return: 429 or 200
        :rtype: Bool
        """
        try:
            users_redis_data = self.rediscache.get_data(user_id=user_id)
            total_request_count = 1
            if users_redis_data:
                current_epoch = int(time.time())
                for epoch, count in users_redis_data.copy().items():
                    if int(epoch) < int(current_epoch - self.window_size):
                        del users_redis_data[str(epoch)]
                        continue
                    else:
                        total_request_count += count
                if total_request_count > self.threshold:
                    return 429
                else:
                    if str(current_epoch) in users_redis_data:
                        users_redis_data[str(current_epoch)] = users_redis_data[str(current_epoch)] + 1
                    else:
                        users_redis_data[str(current_epoch)] = 1
                    self.rediscache.set_data(user_id=user_id, dictionary=users_redis_data)
            else:
                self.rediscache.set_data(user_id=user_id, dictionary={int(time.time()): 1})
            print(f'total_request_count : {total_request_count}')
            print(f'Redis view: {self.rediscache.get_data(user_id=user_id)}')
        except KeyError as ke:
            logging.error(f'KeyError {ke}')
            return 429
        except RuntimeError as re:
            logging.error(f'RuntimeError {re}')
            return 429
        except Exception as e:
            logging.error(f'Exception caught {e}')
            return 429
        return 200
