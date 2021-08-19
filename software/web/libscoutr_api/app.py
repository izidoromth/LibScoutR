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
        result.append({
                    "name": row["title"],
                    "ucode": row["id"] + ' {:04d}'.format(int(row["lib_id"])),
                    "category": row["category"],
                })
    return json.dumps(result)


@app.route("/ordered_books")
def ordered_books():
    result = {}
    for row in dbf.get_ordered_books():
        if row["category"] in result.keys():
            result[row["category"]].append(row["id"] + ' {:04d}'.format(int(row["lib_id"])))
        else:
            result[row["category"]] = [row["id"] + ' {:04d}'.format(int(row["lib_id"]))]

    return json.dumps(result)

# request is like {
#                     '1st floor': {
#                                     'Wrong Shelve': ['7542.69', '7543.69'],
#                                     'Out of Order': ['2321.23'],
#                                     'category': 'Adventure'
#                                 },
#                     '2nd floor': {
#                                     'Wrong Shelve': ['7542.69', '7543.69'],
#                                     'Out of Order': ['2321.23'],
#                                     'category': 'Romance'
#                                 }
#                 }
@app.route('/update_books', methods = ['POST'])
def update_books():
    data = request.get_json()
    for floor in data:
        for status in data[floor]:
            for id in data[floor][status]:
                if status == "Wrong Shelve":
                    print(data[floor]['category'], "1", id)
                    dbf.update_book(data[floor]['category'], "1", id)
                if status == "Out of Order":
                    print(data[floor]['category'], "2", id)
                    dbf.update_book(data[floor]['category'], "2", id)
    return data, 200

if __name__ == "__main__":
    app.run(host="10.0.0.169", port=5001)
