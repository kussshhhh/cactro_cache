from flask import Flask
import os
import redis 

app = Flask(__name__) 

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise ValueError("REDIS_URL is not set")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

import routes.cache 

@app.route("/")
def home():
    return {"message": "cache api is running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 

