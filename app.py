from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["traffic_monitoring"]
collection = db["requests"]

@app.route('/api/requests', methods=['GET'])
def get_requests():
    data = list(collection.find({}, {'_id': False}))  # Fetch all requests and exclude _id field
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
