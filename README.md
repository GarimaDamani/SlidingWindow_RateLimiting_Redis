## Rate limiting using sliding window method 

A function that validates whether the request has crossed the rate limit or not by printing ACCEPTED or REJECTED.

## Setup
* python 3.8 is required as f'' formatting is used while printing and logging.
* Install redis locally using [link](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298)
* Create a virtualenv inside `SlidingWindowRateLimiting` directory. Installation steps [here](https://medium.com/@garimajdamani/https-medium-com-garimajdamani-installing-virtualenv-on-ubuntu-16-04-108c366e4430)

## Run Test cases
```
python -m unittest test/rateLimit_test.py
```
