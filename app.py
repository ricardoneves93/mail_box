from flask import Flask, render_template
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_mail', methods=['POST'])
def publish_new_mail():
    sse.publish({"message": "New Mail!"}, type='new_mail')
    return "Message sent!"

@app.route('/open_door', methods=['POST'])
def publish_opened_door():
    sse.publish({"message": "Opened Door!"}, type='open_door')
    return "Message sent!"

@app.route('/turn_on', methods=['POST'])
def result():
    print ("Turned on")
    return "Received!"
