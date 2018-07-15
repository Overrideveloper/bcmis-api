from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from keras import optimizers
import sys
import os

#disable AVX warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

classifier = Sequential()

classifier.add(Conv2D(32, (3, 3), input_shape = (50, 50, 3), activation = 'relu'))

classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Conv2D(32, (2, 2), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Flatten())

classifier.add(Dense(units = 128, activation = 'relu'))

classifier.add(Dense(units = 1, activation = 'sigmoid'))

classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)
training_path = os.path.abspath("../dataset/training")
test_path = os.path.abspath("../dataset/test")
training_set = train_datagen.flow_from_directory(training_path, target_size = (50, 50), batch_size = 32, class_mode = 'binary')
test_set = test_datagen.flow_from_directory(test_path, target_size = (50, 50), batch_size = 32, class_mode = 'binary')


classifier.fit_generator(training_set, steps_per_epoch = 3970, epochs = 16, validation_data = test_set, validation_steps = 990)


target_dir = './models/'
if not os.path.exists(target_dir):
    os.mkdir(target_dir)
model_json = classifier.to_json()

with open("./models/model.json", "w") as json_file:
    json_file.write(model_json)

classifier.save_weights('./models/model.h5')
print("Training done. Saved models")
