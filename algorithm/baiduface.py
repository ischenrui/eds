import  os,time
from aip import AipFace
from PIL import Image, ImageDraw

""" 你的 APPID AK SK """
APP_ID = '10909628'
API_KEY = 'sInxLcVbCLSg6rNXVDXR4sHD'
SECRET_KEY = 'e2zgNstc7GEhhvFOfCVKDW2itVf0iID4'

filepath ="pic"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

pathDir = os.listdir(filepath)
for path in pathDir:
    pic=filepath+'/'+path
    pic3="pic3/"+path
    image = get_file_content(pic)

    """ 调用人脸检测 """
    client.detect(image)
    """ 如果有可选参数 """
    options = {}
    options["max_face_num"] = 10
    options["face_fields"] = "age"

    """ 带参数调用人脸检测 """
    res=client.detect(image, options)
    try:
        result=res["result"]
    except:
        print(res)
    img = Image.open(pic3)
    img_d = ImageDraw.Draw(img)
    for f in result:
        face_rectangle = f["location"]
        img_d.rectangle((face_rectangle['left'], face_rectangle['top'],
                         face_rectangle['left'] + face_rectangle['width'],
                         face_rectangle['top'] + face_rectangle['height']), outline="red")
    img.save(pic3)
    img.close()
    print("sleep")
    time.sleep(2)


