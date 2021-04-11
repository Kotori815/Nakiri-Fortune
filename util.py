from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, os, random, io, base64

RES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
GOUTU_FOLDER = os.path.join(RES_FOLDER, "goutu")
FONT_NAME = "ZhanKuKuaiLeTi2016XiuDingBan.ttf"

FONT_SIZE_TITLE = 54    #pt
FONT_SIZE_TEXT = 18     #pt
POS_TITLE = (150,75)            # middle-middle        
POS_TEXT_REF = (67.5, 150)      # middle-top
GOUTU_ANCHOR = (202.5, 385)     # middle-bottom

PROB_DIST = [0.05, 0.18, 0.18, 0.18, 0.18, 0.18, 0.05]

# goutu / GOUTU refers to the paintings of nakiri-ayame

def generateFortune(fortuneList, goutu_num, textDict):
    """
    Randomly generate a fortune-telling result and refer to a goutu.
    """
    result = dict()
    # random choose fortune level
    fortune = np.random.choice(fortuneList, p=PROB_DIST)
    score = fortune['score']
    result['name'] = fortune['name']
    # random choose text for the level
    text_list = textDict[fortune['name']]
    result['content'] = random.choice(text_list)
    # random choose a goutu
    result['goutu'] = random.randint(0, goutu_num-1)

    return result

def drawImage(background_img, goutu, result):
    """
    Draw a fortune-telling card according to the result generated in last step.
    """
    new = background_img.copy()
    draw = ImageDraw.Draw(new)
    # write title
    fnt_title = ImageFont.truetype(os.path.join(RES_FOLDER, FONT_NAME), size=FONT_SIZE_TITLE)
    draw.text(POS_TITLE, result['name'], fill="white", font=fnt_title, anchor="mm")
    # draw goutu
    arr = np.array(goutu)
    mask = Image.fromarray(arr[:,:,3] != 0)
    w, h = goutu.size
    goutu_box = ((int)(GOUTU_ANCHOR[0] - w/2), (int)(GOUTU_ANCHOR[1] - h), (int)(GOUTU_ANCHOR[0] + w/2), (int)(GOUTU_ANCHOR[1]))
    new.paste(goutu, box=goutu_box, mask=mask)
    # write text
    fnt_text = ImageFont.truetype(os.path.join(RES_FOLDER, FONT_NAME), size=FONT_SIZE_TEXT)
    new_text = textTranspose(result['content'])
    w, _ = draw.textsize(new_text, font=fnt_text)
    pos_text = (POS_TEXT_REF[0] - w/2, POS_TEXT_REF[1])
    draw.multiline_text(pos_text, new_text, fill="black", font=fnt_text)

    return new

def textTranspose(text):
    """
    Transpose the multi-line text.\n
    e.g. 'abc\n123' => 'a 1\nb 2\nc 3'\n
    PIL need extra library to change the direction of text, and with this process we can ignore it.
    """
    text = text.split()
    text.reverse()

    max_len = max([len(i) for i in text], default=0)
    r_text = ["" for _ in range(max_len)]
    for i in range(max_len):
        for t in text:
            if len(t) >= i+1:
                r_text[i] += (" " + t[i])
            else:
                r_text[i] += "   "
    result = "\n".join(r_text)
    return result

def PILImage2Base64(image):
    """
    Encode PIL image to base64 data url for https transmission
    """
    outputBuffer = io.BytesIO()
    image.save(outputBuffer, format='PNG')
    byteData = outputBuffer.getvalue()
    dataStr = str(base64.b64encode(byteData))
    base64str = 'data:image/png;base64,' + dataStr[2:-1]

    return base64str
