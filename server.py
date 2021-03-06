from queuecontroller import QueueController
from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
queue = QueueController()
queue.start()

@app.route("/")
def index():
	return render_template("index.html", animation_duration=queue.duration)

@app.route("/pat")
def pat():
	queue.enqueue()
	return "ok"

if __name__ == "__main__":
	with app.app_context():
		queue.controller.dance()

	app.run(host="0.0.0.0", port=4000)
