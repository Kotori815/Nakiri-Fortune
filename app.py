from flask import Flask, request, jsonify, render_template
import json
from PIL import Image

from util import *

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
)
app.jinja_env.auto_reload = True

# defining global variable for re-use
# general fortune telling data
def readJson(file):
    filename = os.path.join(RES_FOLDER, file)

    if not os.path.exists(filename):
        return [{'score': 0, 'name':'File {} Not Found'.format(filename)}]
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    return content

FORTUNE_FILE = readJson("fortune.json")
TEXT_FILE = readJson("text.json")
# general background image 
BACKGROUND_IMG = Image.open(os.path.join(RES_FOLDER, "background.png"))
goutu_list = [Image.open(os.path.join(GOUTU_FOLDER, goutu)) for goutu in os.listdir(GOUTU_FOLDER)]

# defining api
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if len(request.form['name']):
        with open("logger", "a", encoding="utf-8") as f:
            f.write("username: {}\n".format(request.form['name']))

    fortune = generateFortune(FORTUNE_FILE, len(goutu_list), TEXT_FILE)
    result = drawImage(BACKGROUND_IMG, goutu_list[fortune['goutu']], fortune)
    dataUrl = PILImage2Base64(result)

    return jsonify({'code': 0,
                    'message': 'hello~',
                    'imgUrl': dataUrl})
