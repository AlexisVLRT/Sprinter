import json
import os
import logging
import time

import uuid as uuid
from bottle import Bottle, HTTPResponse

import config

app = Bottle()
uuid = str(uuid.uuid4())


@app.route("/", method=["POST"])
def main():
    # Busy sleep
    start = time.time()
    while time.time() - start < 10:
        pass

    return HTTPResponse(status=200, body=json.dumps({"message": uuid}))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
