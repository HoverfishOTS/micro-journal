import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.microjournal
entries_collection = db.entries

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/entries', methods=['GET'])
def get_entries():
    entries = list(entries_collection.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(entries)

@app.route('/api/entries', methods=['POST'])
def add_entry():
    data = request.get_json()
    content = data.get('content')
    
    if not content:
        return jsonify({"error": "Content is required"}), 400
        
    entry = {
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    }
    entries_collection.insert_one(entry)
    
    # Remove _id before returning to client
    entry.pop('_id', None)
    return jsonify(entry), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)