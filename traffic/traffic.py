from cv2 import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow import keras
import re

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 3
TEST_SIZE = 0.4

def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")
    
    # Get image arrays and labels for all image files (massage the data)
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    path = os.walk(data_dir)
    img_list = []
    label_list = []

    for root, dirs, files in path:
        for fname in files:
            if re.search('.ppm', fname):
                new_path = os.path.join(root, fname)
            else:
                continue
            # print(new_path)
            num = root.replace('gtsrb-small/', '')

            # load a color image, setting flag to 1
            new_img = cv2.imread(new_path, 1)

            # resize image
            img_output = cv2.resize(new_img, (IMG_WIDTH, IMG_HEIGHT))

            # add img array and labels as tuples into a list
            img_list.append(img_output)
            label_list.append(num)

    #print(img_list, label_list)
    return (img_list, label_list)
    raise NotImplementedError

def test_load ():
    img = cv2.imread('gtsrb-small/0/00015_00010.ppm')
    cv2.imshow('Image', img)
    while True:
        exit_key = ord('q')
        if cv2.waitKey(exit_key):
            cv2.destroyAllWindows()
            break

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    model = keras.Sequential ([

        # set 32 filters and a 3*3 kernel
        tf.keras.layers.Conv2D(
            32, (3,3), activation = 'relu', input_shape = (IMG_WIDTH, IMG_HEIGHT,3),
        ),

        # max-pooling using a 2*2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),

        # Add an output with output units equal to the num of categories
        keras.layers.Dense(NUM_CATEGORIES, activation = 'softmax')
    ])

    model.compile(
        optimizer = 'adam',
        #loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        loss="categorical_crossentropy",
        metrics = ['accuracy']
    )

    return model
    raise NotImplementedError


if __name__ == "__main__":
    main()
