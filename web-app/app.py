"""
app.py file that helps serve as the front end of our application
"""

import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests

app = Flask(__name__, template_folder="templates")

# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017/")
db = client["ml_database"]
collection = db["transcription"]


@app.route("/test_render_template")
def test_render_template():
    """
    Request received for /test_render_template
    """
    print("Request received for /test_render_template")
    return render_template("root.html")


@app.route("/")
def root_page():
    """
    Template to render root page
    """
    return render_template("root.html")


@app.route("/results")
def display_results():
    """
    Function to render the results page for a specific audio analysis
    """
    my_transcript = collection.find_one(sort=[("_id", -1)])

    if not my_transcript:
        return jsonify({"error": "Result not found"}), 404

    return render_template(
        "results.html", transcription_result=my_transcript, activePage="results.html"
    )


@app.route("/analyzeData", methods=["POST"])
def analyze_data():
    """
    Function to send generated audio file to the machine learning client
    """
    try:
        if "audio" not in request.files:
            return jsonify({"status": "error", "message": "No audio file provided"})

        audio_file = request.files["audio"]
        ml_client_url = "http://backend:5001/analyzeAudio"
        # Use the converted audio file
        response = requests.post(
            ml_client_url, files={"audio": audio_file}, timeout=100
        )
        print("sent over")

        # pylint: disable=R1705
        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            return (
                jsonify(
                    {"error": "Failed to send and process audio. Please try again."}
                ),
                500,
            )
    except FileNotFoundError as e:
        return jsonify({"status": "error", "message": f"File not found: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
