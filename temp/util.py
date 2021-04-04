from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, os, random

from temp.values import *

def readJson(file):
    filename = os.path.join(RES_FOLDER, file)

    if not os.path.exists(filename):
        return [{'score': 0, 'name':'File {} Not Found'.format(filename)}]
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    return content

def generate(textFile, fortuneFile):
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
    print(text)
    draw.multiline_text((10,10), text, font=fnt, fill=FONT_COLOR)
    return new

def calculateBox(result):
    sentences = result["content"].split()
    lineNum = len(sentences) + 1
    columnNum = max([len(string) for string in sentences])

    return (0,0,0,0)