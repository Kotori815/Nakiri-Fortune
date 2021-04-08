from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, os, random, io, base64

RES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
GOUTU_FOLDER = "goutu"

BACKGROUND_FILE = "background.png"
FORTUNE_FILE = "fortune.json"
TEXT_FILE = "text.json"
FONT_NAME = "ZhanKuKuaiLeTi2016XiuDingBan.ttf"

FONT_SIZE_TITLE = 108
FONT_SIZE_TEXT = 36
POS_TITLE = (300,150)
POS_TEXT_REF = (135,300)
BOX_GOUTU = (275, 300, 525, 700)

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

    backgroundPath = os.path.join(RES_FOLDER, GOUTU_FOLDER)
    result['goutu'] = random.choice(os.listdir(backgroundPath))

    return result

def drawImage(result):
    base_img = Image.open(os.path.join(RES_FOLDER, BACKGROUND_FILE))
    new = base_img.copy()
    draw = ImageDraw.Draw(new)
    # write title and text
    fnt_title = ImageFont.truetype(os.path.join(RES_FOLDER, FONT_NAME), size=FONT_SIZE_TITLE)
    draw.text(POS_TITLE, result['name'], fill="white", font=fnt_title, anchor="mm")
    fnt_text = ImageFont.truetype(os.path.join(RES_FOLDER, FONT_NAME), size=FONT_SIZE_TEXT)
    new_text = textTranspose(result['content'])
    w, _ = draw.textsize(new_text, font=fnt_text)
    pos_text = (POS_TEXT_REF[0] - w/2, POS_TEXT_REF[1])
    draw.multiline_text(pos_text, new_text, fill="black", font=fnt_text)
    
    return new

def textTranspose(text):
    text = text.split()
    text.reverse()

    max_len = max([len(i) for i in text], default=0)
    r_text = ["" for _ in range(max_len)]
    for i in text:
        for k,char in enumerate(i):
            r_text[k] += (" " + char)
    result = "\n".join(r_text)
    return result

def PILImage2Base64(image):
    outputBuffer = io.BytesIO()
    image.save(outputBuffer, format='PNG')
    byteData = outputBuffer.getvalue()
    dataStr = str(base64.b64encode(byteData))
    base64str = 'data:image/png;base64,' + dataStr[2:-1]

    return base64str
