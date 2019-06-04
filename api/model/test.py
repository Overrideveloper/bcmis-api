from keras.models import model_from_json
from keras.preprocessing import image
from keras import backend as K
import numpy as np
import cv2
from PIL import Image

def predict(input_image):
    json_file = open(r'C:\Users\banso\Desktop\Dev\Active\bcmis-api\api\model\model.json', 'r')
    model_json = json_file.read()
    json_file.close()

    model = model_from_json(model_json)
    model.load_weights(r"C:\Users\banso\Desktop\Dev\Active\bcmis-api\api\model\model.h5")

    model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

    img_str = input_image.read()
    img_np = np.fromstring(img_str, np.uint8)
    
    im = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    img = Image.fromarray(im, 'RGB')
    image = np.array(img)

    image = image/255

    a = []
    a.append(image)
    a = np.array(a)
    score = model.predict(a, verbose = 1)
    print(score)

    result = np.argmax(score)
    acc = np.max(score)

    print(result)
    print(acc)

    '''img_str = input_image.read()
    img_np = np.fromstring(img_str, np.uint8)

    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (50, 50))
    img = img.reshape(1, 50, 50, 3)

    result = model.predict(img)
    print(result)'''
    if result == 0:
        response = "negative"
    else:
        response = "positive"

    res = {"response": response, "accuracy": acc}

    '''print(res['response'])
    print(res['accuracy'])'''

    K.clear_session()
    return res
