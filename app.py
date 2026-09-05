import json
import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


@app.route("/", methods=["GET"])
def get_frontend():
    return render_template("index.html")


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
