import os

from flask import Flask, request, render_template
from google.cloud import storage
from werkzeug.utils import secure_filename

app = Flask(__name__)

GCS_BUCKET_NAME = "data_stream_gcs"
GCS_PREFIX = "003_loading_data_from_www_page_to_bq"

storage_client = storage.Client()


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        filename = secure_filename(file.filename)
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(f"{GCS_PREFIX}/{filename}")
        blob.upload_from_file(file)
        return f"File {filename} uploaded to {GCS_BUCKET_NAME}/{GCS_PREFIX}."
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
