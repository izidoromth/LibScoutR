from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import json
import dbFunctions as dbf


app = Flask(__name__, static_url_path="")
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/books")
def books():
    result = []
    for row in dbf.get_books():
        result.append(dict(row))
    return json.dumps(result)


@app.route("/ordered_books")
def ordered_books():
    result = {}
    for row in dbf.get_ordered_books():
        if row["current_category"] in result.keys():
            result[row["current_category"]].append(row["id"])
        else:
            result[row["current_category"]] = [row["id"]]

    return json.dumps(result)


# @app.route('/update_books', methods = ['POST'])
# def update_books():
#     data = request.get_json()
#     return data['books'][0]


if __name__ == "__main__":
    app.run(host="localhost", port=5001)
