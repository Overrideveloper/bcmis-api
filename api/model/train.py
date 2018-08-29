import keras
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pylab as plt
from sklearn.metrics import roc_curve, auc
import numpy as np
import cv2
import PIL

class AccuracyHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.acc = []
        self.loss = []
        self.val_loss = []
        self.val_acc = []

    def on_epoch_end(self, batch, logs={}):
        self.acc.append(logs.get('acc'))
        self.loss.append(logs.get('loss'))
        self.val_loss.append(logs.get('val_loss'))
        self.val_acc.append(logs.get('val_acc'))

history = AccuracyHistory()

# Initialising the CNN
model = Sequential()

# Convolution
model.add(Conv2D(32, (3, 3), input_shape = (25, 25, 3), activation = 'relu'))

# Pooling
model.add(MaxPooling2D(pool_size = (2, 2)))

# Second convolutional layer
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

# Flattening
model.add(Flatten())

# Full connection
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 1, activation = 'sigmoid'))

# Compiling the CNN
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

batchSize = 32
epochs = 30

training_set = train_datagen.flow_from_directory(r'C:\Users\banso\Desktop\bcmis-api\dataset\train',
target_size = (25, 25), batch_size = batchSize, class_mode = 'binary')

test_set = test_datagen.flow_from_directory(r'C:\Users\banso\Desktop\bcmis-api\dataset\test',
target_size = (25, 25), batch_size = batchSize, class_mode = 'binary')

model.fit_generator(training_set, steps_per_epoch = 9200, epochs = epochs, validation_data = test_set, validation_steps = 4200, callbacks=[history])

#Calculate ROC and AUC
y_pred = model.predict_generator(test_set).ravel()
y_test = test_set.classes
fpr, tpr, thresholds = roc_curve(y_test, y_pred)
auc_score = auc(fpr, tpr)

#Plot accuracy graph
plt.style.use("ggplot")
plt.figure(1)
N = epochs
plt.plot(range(0, N), history.loss, label="training loss")
plt.plot(range(0, N), history.val_loss, label="validation loss")
plt.plot(range(0, N), history.acc, label="training accuracy")
plt.plot(range(0, N), history.val_acc, label="validation accuracy")
plt.title("Training and Validation Accuracy/Loss")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="upper left")
plt.show()

#Plot ROC curve
plt.figure(2)
plt.plot(fpr, tpr, label="Area Under Curve(AUC) = {:.3f}".format(auc_score))
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('Receiver Operating Characteristic (ROC) Curve and Area Under Curver (AUC)')
plt.legend(loc="best")
plt.show()

#Save model to file
model_json = model.to_json()
with open("./model.json","w") as json_file:
  json_file.write(model_json)

model.save_weights("./model.h5")
print("Saved model..")
