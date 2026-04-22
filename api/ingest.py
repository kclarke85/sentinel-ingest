from http.server import BaseHTTPRequestHandler
from pymongo import MongoClient
from datetime import datetime
import json
import os

MONGO_URI = os.environ.get("MONGO_URI")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        client = MongoClient(MONGO_URI)
        db = client["encounter_db"]
        data["timestamp"] = datetime.utcnow().isoformat()
        db["readings"].insert_one(data)
        client.close()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Reading stored"}).encode())