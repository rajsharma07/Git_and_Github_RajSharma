import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, url_for
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
MONGO_URI = os.getenv("MONGO_URI")
if(not MONGO_URI):
    raise ValueError("MONGO_URI is not set please add in .env file")

client = MongoClient(MONGO_URI)
db = client["todo_database"]
todos = db["todos"]

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


@app.route("/", methods=["GET"])
def get_frontend():
    return "<h1>My Todo App</h1>"

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    todos.insert_one(todo)

    return jsonify({
        "message": "To-Do item submitted successfully"
    }), 201

@app.route("/api", methods=["GET"])
def get_api_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            return jsonify({"error": "Data file contents are invalid."}), 500

        return jsonify(data)

    except FileNotFoundError:
        return jsonify({"error": "Data file not found."}), 404

    except json.JSONDecodeError:
        return jsonify({"error": "Data file contains invalid JSON."}), 500

    except OSError as exc:
        return jsonify({"error": f"Unable to read data file: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
