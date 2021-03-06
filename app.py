import time

import redis
from flask import Flask

import config

app = Flask(__name__)
app.config.from_object(config.Config)
cache = redis.Redis(host=app.config['REDIS_HOST'], port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\nApp version 3'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
