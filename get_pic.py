from PIL import Image, ImageGrab

# 保存剪切板内图片
im = ImageGrab.grabclipboard()

if isinstance(im, Image.Image):
    im = im.crop((345, 190, 1035, 885))
    im.save("1.png")
    print(im.size)
elif im:
    for filename in im:
        im = Image.open(filename)
else:
    print("clipboard is empty")
