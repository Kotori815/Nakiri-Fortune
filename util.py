from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, os, random, io, base64

RES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
GOUTU_FOLDER = "goutu"
FONT_NAME = "ZhanKuKuaiLeTi2016XiuDingBan.ttf"

FONT_SIZE_TITLE = 54
FONT_SIZE_TEXT = 18
POS_TITLE = (150,75)
POS_TEXT_REF = (67.5, 150)
BOX_GOUTU = (137.5, 150, 262.5, 350)

def generateFortune(fortuneFile, textFile):
    result = dict()
    
    fortune = random.choice(fortuneFile)
    score = fortune['score']
    result['name'] = fortune['name']

    text_list = textFile[fortune['name']]
    result['content'] = random.choice(text_list)

    backgroundPath = os.path.join(RES_FOLDER, GOUTU_FOLDER)
    result['goutu'] = random.choice(os.listdir(backgroundPath))

    return result

def drawImage(background_img, result):
    new = background_img.copy()
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
