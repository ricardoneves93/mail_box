from flask import Flask, render_template
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_mail', methods=['POST'])
def publish_hello():
    sse.publish({"message": "New Mail!"}, type='greeting')
    return "Message sent!"

@app.route('/turn_on', methods=['POST'])
def result():
    print ("Turned on")
    return "Received!"
