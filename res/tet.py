text = "啊啊啊啊啊啊啊 啊啊啊啊"
text = text.split()
text.reverse()

max_len = max([len(i) for i in text], default=0)
r_text = ["" for _ in range(max_len)]
for i in range(max_len):
    for t in text:
        if len(t) >= i+1:
            r_text[i] += ("  " + t[i])
        else:
            r_text[i] += " "
result = "\n".join(r_text)
print(result)