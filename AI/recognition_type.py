import os
import time
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2
import numpy as np

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

    model.save("Assets/typer")


def recognize_type(img_path):
    model = keras.models.load_model("Assets/typer")
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28, 28), interpolation = cv2.INTER_AREA)
    img = cv2.bitwise_not(img)
    img = img / 255
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img = img[np.newaxis]
    result = model.predict(img)

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    print("Rozpoznana klasa:", class_names[np.argmax(result)])
    return "t-shirt"

if __name__ == '__main__':
    #train_and_save_model()
    recognize_type("Assets/Images/product-17996.jpg")
    recognize_type("Assets/Images/product-17997.jpg")
    recognize_type("Assets/Images/ant-tshirt-ant-blu-m.jpg")

