import os
from keras.preprocessing.image import load_img, img_to_array
import cv2
from keras.models import model_from_json

#disable AVX warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

model_path = os.path.abspath("models/model.json")
weight_path = os.path.abspath("models/model.h5")
json_file = open(model_path, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(weight_path)
print("Loaded model. Proceeding....")

loaded_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
path = os.path.abspath("../dataset/test/malignant/SOB_M_DC-14-16875-40-014.png")
test_image = cv2.imread(path)
img = cv2.resize(test_image, (50, 50))
img = img.reshape(1, 50, 50, 3)

result = loaded_model.predict(img)
print(result)
if result == 0:
    print("Benign")
else:
    print("Malignant")
