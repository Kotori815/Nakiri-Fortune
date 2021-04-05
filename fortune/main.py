from flask import request, jsonify, render_template
import json

from fortune import app
import fortune.util as util
from fortune.values import *

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']

    fortune = util.generateFortune(TEXT_FILE, FORTUNE_FILE)
    result = util.drawImage(fortune)
    dataUrl = util.PILImage2Base64(result)

    return jsonify({'code': 0,
                    'message': 'hello~',
                    'imgUrl': dataUrl})