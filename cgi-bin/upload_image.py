#!/usr/bin/env python3
import common
import os
import sys
from multipart import MultipartParser, parse_options_header
import tempfile

@common.cgi_tb
def handle_file_upload():
    # Get content length and content type from environment variables
    content_length = int(os.environ.get("CONTENT_LENGTH", 0))
    content_type = os.environ.get("CONTENT_TYPE", "")

    # Check if content type is multipart/form-data
    if "multipart/form-data" not in content_type:
        print("Status: 400 Bad Request")
        print("Content-Type: text/plain\n")
        print("Invalid content type.")
        return

    # Parse boundary from content type
    _, params = parse_options_header(content_type)
    boundary = params.get("boundary")
    if not boundary:
        print("Status: 400 Bad Request")
        print("Content-Type: text/plain\n")
        print("Missing boundary in content type.")
        return

    # Read the request body (file upload data) from stdin
    body = sys.stdin.buffer.read(content_length)

    # Parse the multipart form data
    parser = MultipartParser(io.BytesIO(body), boundary)

    # Process each part of the form
    for part in parser:
        if part.filename:  # It's a file part
            # Save the file to a temporary location
            temp_file_path = os.path.join(tempfile.gettempdir(), part.filename)
            with open(temp_file_path, "wb") as f:
                f.write(part.file.read())

            # Output the temporary file path
            print("Content-Type: text/html\n")
            print(f"<html><body>File uploaded to: {temp_file_path}</body></html>")
            return

    # If no file was uploaded
    print("Content-Type: text/html\n")
    print("<html><body>No file uploaded.</body></html>")

if __name__ == "__main__":
    handle_file_upload()
