from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np

json_file = open('model.json', 'r')
model_json = json_file.read()
json_file.close()

model = model_from_json(model_json)
model.load_weights("model.h5")

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

img = image.load_img(r"C:\Users\banso\Desktop\bcmis-api\dataset\train\non-idc\8863_idx5_x351_y401_class0.png", target_size=(25, 25))
img = image.img_to_array(img)
img = np.expand_dims(img, axis = 0)

print(model.predict(img))
