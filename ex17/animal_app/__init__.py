from flask import Flask
import random, redis

Red = redis.StrictRedis()
app = Flask(__name__)
app.secret_key = hex(random.randrange(1<<128))  # 128 bits of randomness

import animal_app.views


