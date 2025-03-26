from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import logging
from typing import Dict, List
from processors.processStructured import process_structured_transactions
from processors.processUnstructured import process_unstructured_transactions, read_unstructured_file
from risk_entry import risk_entry
# --- Configure Logging ---
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def process_transactions(input_file_path: str) -> List[Dict]:
    """Determines file type and processes transactions accordingly."""
    try:
        if input_file_path.endswith('.csv'):
            return process_structured_transactions(input_file_path)
        elif input_file_path.endswith('.txt'):
            unstructured_data = read_unstructured_file(input_file_path)
            return process_unstructured_transactions(unstructured_data)
        else:
            logger.error(f"Unsupported file type: {input_file_path}")
            return []
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return []


@app.route('/')
def home():
    return jsonify({
        "message": "Flask application is running successfully!",
        "status": "ok"
    })


@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint to upload a file and process transactions."""
    if 'file' not in request.files:
        logger.warning("No file part in request")
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        logger.warning("No file selected")
        return jsonify({"error": "No selected file"}), 400

    # Validate file type before saving
    if not (file.filename.endswith('.csv') or file.filename.endswith('.txt')):
        logger.warning(f"Unsupported file type uploaded: {file.filename}")
        return jsonify({"error": "Unsupported file type. Please upload a .csv or .txt file."}), 400

    # Save the uploaded file temporarily
    os.makedirs('uploads', exist_ok=True)  # Ensure uploads directory exists
    input_file_path = os.path.join('uploads', file.filename)
    file.save(input_file_path)
    logger.info(f"File saved: {input_file_path}")

    # Process transactions
    processed_data = process_transactions(input_file_path)

    if processed_data:
        os.makedirs('data', exist_ok=True)  # Ensure data directory exists
        output_filename = f"processed_{os.path.splitext(file.filename)[0]}.json"
        output_file_path = os.path.join('data', output_filename)

        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2)
            logger.info(f"Processed transactions saved to {output_file_path}")
            print(processed_data)
            risk_stuff = risk_entry()
            response = {}
            response["transaction"] = risk_stuff
            return jsonify({"message": "File processed successfully", "output_json": response}), 200
        except IOError as e:
            logger.error(f"Failed to write output file: {str(e)}")
            return jsonify({"error": "Failed to write output"}), 500

    logger.error("No data processed from file")
    return jsonify({"error": "No data processed"}), 500


if __name__ == "__main__":
    # Allow external access if needed
    app.run(host='0.0.0.0', port=8002, debug=True) 