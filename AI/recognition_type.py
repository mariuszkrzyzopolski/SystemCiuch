import os
import time
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image, ImageOps

import AI.remove_background as rmbg
import Common.image_functions as fimg


def train_and_save_model():
    tf.keras.utils.disable_interactive_logging()

    """Checking available GPU with CUDA for training and disabling it"""
    tf.config.list_physical_devices('GPU')
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    """ Prepare test and train datasets """
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    """Creation and compilation of custom model, adjusted to fashion minst dataset problem"""
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    """Train model with base time benchmark"""
    start = time.time()
    history = model.fit(train_images, train_labels, epochs=10)
    print("time: ", time.time() - start, "s")

    """Benchmark of accuracy, with dependency of epoch"""
    plt.plot(list(range(10)), history.history["accuracy"], 'bo', label='Training acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.show()

    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    print('\nTest accuracy:', test_acc)

    """Creation and compilation of custom, smaller model for comparison"""
    model_smaller = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])

    model_smaller.compile(optimizer='adam',
                          loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                          metrics=['accuracy'])

    """Train model with base time benchmark"""
    start = time.time()
    history_smaller = model_smaller.fit(train_images, train_labels, epochs=10)
    print("time: ", time.time() - start, "s")

    """Benchmark of accuracy, with dependency of epoch"""
    plt.plot(list(range(10)), history_smaller.history["accuracy"], 'bo', label='Training acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.show()

    test_loss, test_acc = model_smaller.evaluate(test_images, test_labels, verbose=2)
    print('\nTest accuracy:', test_acc)

    model.save("Models")


def recognize_type(img):
    model = keras.models.load_model("Models")
    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    img = img / 255
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img = img[np.newaxis]
    result = model.predict(img)

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    print("Rozpoznana klasa:", class_names[np.argmax(result)])
    return class_names[np.argmax(result)]

"""
if __name__ == '__main__':
    # train_and_save_model()
    img = Image.open("Assets/Images/product-17997.jpg")
    img = ImageOps.exif_transpose(img)
    img = fimg.resize_img(img)
    cv2_img = fimg.pil_to_cv2(img)
    cv2_img = rmbg.cv2_remove_backgound(cv2_img)
    cv2.imshow("img", cv2_img)
    recognize_type(cv2_img)
"""