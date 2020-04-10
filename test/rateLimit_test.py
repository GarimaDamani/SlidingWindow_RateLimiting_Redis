import unittest
from time import sleep
from modules.rateLimit import SlidingWindowRateLimit
from config import config


class RateLimitTest(unittest.TestCase):
    """
    Class to test the rate limiting function
    """
    def setUp(self):
        """
        Function to setup variables, data for testing rate limiting
        :return: None
        :rtype: None
        """
        self.threshold = config.threshold
        self.window_size = config.window_size
        self.accepted = "ACCEPTED"
        self.rejected = "REJECTED"
        self.user_id = "GG23b5i"     # Some random string
        self.slidingwindowratelimiter = SlidingWindowRateLimit(self.threshold, self.window_size)
        self.sleep_values = [0, 5, 30, 0, 10, 0, 16, 0]     # For testing purpose only

    def tearDown(self):
        """
        Function to cleanup variables, data was allocated for testing rate limiting
        :return: None
        :rtype: None
        """
        del self.threshold
        del self.window_size
        del self.accepted
        del self.rejected
        del self.user_id
        del self.slidingwindowratelimiter
        del self.sleep_values

    def test_rate_limit_1(self):
        """
        Call send_request function in a loop to produce the effect of many requests
        are send to the rate limiting function
        """
        # Sending 100 req at a time
        print(f'Considering threshold : {self.threshold}')
        for i in range(100):
            self._send_request(i, 0)

    def test_rate_limit_2(self):
        """
        Call send_request function in a loop to produce the effect of many requests
        are send to the rate limiting function
        """
        # Sending few requests with sleep
        for _ in range(1):
            for number, sleep_time in zip(range(len(self.sleep_values)), self.sleep_values):
                self._send_request(number, sleep_time)

    def _send_request(self, number, sleep_seconds):
        """
        :param number: request number
        :type number: int
        :param sleep_seconds: for long the process should sleep for
        :type sleep_seconds: int
        """
        print(f'Request {number} send')
        response = self.slidingwindowratelimiter.validate_request_rate_limit(user_id=self.user_id)
        print(self.accepted) if response == 200 else print(self.rejected)
        print(f'sleep {sleep_seconds}s')
        sleep(sleep_seconds)


if __name__ == "__main__":
    """
    Call the main for testing
    """
    unittest.main()
