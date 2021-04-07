from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, os, random, io, base64

RES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
BACK_FOLDER = "backgrounds"
PANEL_IMG = "panel.png"

FORTUNE_FILE = "fortune.json"
TEXT_FILE = "text.json"

FONT_NAME = "ZhanKuKuaiLeTi2016XiuDingBan.ttf"
FONT_SIZE = 28
FONT_COLOR = (0, 0, 0)

def readJson(file):
    filename = os.path.join(RES_FOLDER, file)

    if not os.path.exists(filename):
        return [{'score': 0, 'name':'File {} Not Found'.format(filename)}]
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    return content

def generateFortune(textFile, fortuneFile):
    result = dict()
    
    allScore = readJson(fortuneFile)
    fortune = random.choice(allScore)
    score = fortune['score']
    result['name'] = fortune['name']

    allText = readJson(textFile)
    candidates = [entry for entry in allText if entry['score'] == score]
    text = random.choice(candidates)
    result['content'] = text['content']

    backgroundPath = os.path.join(RES_FOLDER, BACK_FOLDER)
    result['background'] = random.choice(os.listdir(backgroundPath))

    return result

def drawImage(result):
    base_img = Image.open(os.path.join(RES_FOLDER, BACK_FOLDER, result['background']))
    panel_img = Image.open(os.path.join(RES_FOLDER, PANEL_IMG))

    box = calculateBox(result)
    
    new = base_img.copy()
    new.paste(panel_img, box)

    fnt = ImageFont.truetype(os.path.join(RES_FOLDER, FONT_NAME), size=FONT_SIZE)

    draw = ImageDraw.Draw(new)
    text = "\n".join([result['name']] + result["content"].split())
    draw.multiline_text((10,10), text, font=fnt, fill=FONT_COLOR)

    return new

def calculateBox(result):
    """
    sentences = result['content'].split()
    lineNum = len(sentences) + 1
    columnNum = max([len(string) for string in sentences])
    """
    return (75, 50, 225, 350)

def PILImage2Base64(image):
    outputBuffer = io.BytesIO()
    image.save(outputBuffer, format='PNG')
    byteData = outputBuffer.getvalue()
    dataStr = str(base64.b64encode(byteData))
    base64str = 'data:image/png;base64,' + dataStr[2:-1]

    return base64str
