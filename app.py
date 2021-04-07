from flask import Flask, request, jsonify, render_template
import json

from util import *

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
)
app.jinja_env.auto_reload = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']

    fortune = generateFortune(TEXT_FILE, FORTUNE_FILE)
    result = drawImage(fortune)
    dataUrl = PILImage2Base64(result)

    return jsonify({'code': 0,
                    'message': 'hello~',
                    'imgUrl': dataUrl})
