from flask import request, jsonify
from server import app, redis_client

MAX_CACHE_SIZE = 200 

@app.route("/cache", methods=["POST"])
def set_cache():
    data = request.json
    key, value = data.get("key"), data.get("value")

    if not key or not value:
        return jsonify({"error": "key and value are required"}), 400
    
    if redis_client.dbsize() >= MAX_CACHE_SIZE:
        return jsonify({"error": "cache limit reached delete some items"}), 400
    
    redis_client.set(key, value)

    return jsonify({"message": "key added succesfully"}), 201

@app.route("/cache/<key>", methods=["GET"])
def get_cache(key):
    value = redis_client.get(key) 
    if value is None:
        return jsonify({"error": "key not found"}), 404
    
    return jsonify({"key": key, "value": value}), 200

@app.route("/cache/<key>", methods=["DELETE"])
def delete_cache(key):
    deleted = redis_client.delete(key)
    if deleted == 0:
        return jsonify({"error": "key not found"}), 404
    
    return jsonify({"message": f"key '{key}' deleted succesfully"}), 200