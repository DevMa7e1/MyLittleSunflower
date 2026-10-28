from flask import Flask

app = Flask(__name__)

@app.route('/users/<id>/statusbar/today')
def send_hours(id):
    return """{
  "data": {
    "grand_total": {
      "total_seconds": 7200,
      "text": "2h 30m / 4h goal"
    },
    "goal": {
      "target_seconds": 14400,
      "tracked_seconds": 9000,
      "completion_percent": 62,
      "complete": false
    }
  }
}"""