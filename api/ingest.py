from pymongo import MongoClient
from datetime import datetime
import json
import os

MONGO_URI = os.environ.get("MONGO_URI")

def handler(request, response):
    data = json.loads(request.body)
    try:
        client = MongoClient(MONGO_URI)
        db = client["encounter_db"]
        data["timestamp"] = datetime.utcnow().isoformat()
        db["readings"].insert_one(data)
        client.close()
        response.status_code = 200
        return json.dumps({"message": "Reading stored", "device": data.get("device_id")})
    except Exception as e:
        response.status_code = 500
        return json.dumps({"error": str(e)})