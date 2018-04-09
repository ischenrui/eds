
import requests,time
from json import JSONDecoder
from PIL import Image, ImageDraw




def faceDetect(path,toPath):

    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    data = {
        "api_key": "mCfBN23JWgwYFHyhlEWoB7mpIVh8HuW5",
        "api_secret": "x44kBrjgCVddv6MynjXryXjT9hjjkxYN"
    }

    f = open(path, "rb")
    files = {"image_file": f}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    response.close()
    req_dict = JSONDecoder().decode(req_con)
    f.close()
    if "error_message" in req_dict.keys():
        print("发生了错误：")
        print(req_dict)
        return

    img = Image.open(path)
    img_d = ImageDraw.Draw(img)
    face = req_dict["faces"]
    for f in face:
        face_rectangle = f["face_rectangle"]
        img_d.rectangle((face_rectangle['left'], face_rectangle['top'],
                         face_rectangle['left'] + face_rectangle['width'],
                         face_rectangle['top'] + face_rectangle['height']), outline="red")
    img.save(toPath)
    img.close()
    time.sleep(5)

faceDetect("pic/2-2.jpg","2-2.jpg")