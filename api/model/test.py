from keras.models import model_from_json
from keras.preprocessing import image
from keras import backend as K
import numpy as np
import cv2

def predict(input_image):
    json_file = open('model/model.json', 'r')
    model_json = json_file.read()
    json_file.close()

    model = model_from_json(model_json)
    model.load_weights("model/model.h5")

    model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

    img_str = input_image.read()
    img_np = np.fromstring(img_str, np.uint8)

    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (25, 25))
    img = img.reshape(1, 25, 25, 3)

    result = model.predict(img)
    if result is 0:
        response = "positive"
    else:
        response = "negative"
    K.clear_session()
    return response
