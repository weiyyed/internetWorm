from PIL import Image
import pytesseract

image = Image.open('file/english.png')
content = pytesseract.image_to_string(image)  # 解析图片
print(content)