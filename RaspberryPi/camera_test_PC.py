print('Loading dependencies')
from picamera import PiCamera
import datetime as dt
import numpy as np
import time
import h5py

#import tensorflow as tf
from tensorflow.keras.models import Sequential #, load_model
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
#import tensorflow_hub as hub

# Set up the camera
print('Loading camera')
camera = PiCamera()
camera.resolution = (100, 100)
camera.framerate = 10

print('Loading model')

model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(100,100,3)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(264, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(95, activation='softmax'))

print(model.summary())



model.load_weights('./trained_model.h5')
print('Finished loading model')
print('Starting predictions...')

while True:
#for i in range(10):
    #time.sleep(2)
    output = np.empty((128, 112, 3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    fruit = model.predict_classes(np.expand_dims(output[:100,:100,:], axis=0))
    print(fruit)

camera.close()
