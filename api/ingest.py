from pymongo import MongoClient
from datetime import datetime
import json
import os

MONGO_URI = os.environ.get("MONGO_URI")

def handler(request):
    if request.method == "POST":
        try:
            data = request.json()
            client = MongoClient(MONGO_URI)
            db = client["encounter_db"]
            data["timestamp"] = datetime.utcnow().isoformat()
            db["readings"].insert_one(data)
            client.close()
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Reading stored", "device": data.get("device_id")})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }
    return {
        "statusCode": 405,
        "body": json.dumps({"error": "Method not allowed"})
    }