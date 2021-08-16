from flask import Flask, request
import json
from robot import Robot
import threading

# UML was made using this software
# https://www.planttext.com

app = Flask(__name__)


@app.route("/guide_user", methods=["POST"])
# {
# 	"name": "Sherlock",
#   "universal_code": "123.x",
# 	"current_category": "Science Fiction"
# }
def hello_world():
    book = json.loads(request.data)
    return f"Searching for the book: {robot.user_want_book(book)}"


robot = Robot()
threading.Thread(target=robot.main).start()

