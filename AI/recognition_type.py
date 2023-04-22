import tensorflow as tf
from PIL import ImageOps
from PIL.Image import Image
from tensorflow import keras


import os
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28 * 28, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        if not self.training:
            x = F.softmax(x, dim=1)
        return x

def train_and_save_model2():
    """ Prepare test and train datasets """
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    train_set = datasets.FashionMNIST('./Assets/FashionMNIST', train=True, download=True, transform=transform)
    test_set = datasets.FashionMNIST('./Assets/FashionMNIST', train=False, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=32, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=32, shuffle=False)

    """Creation and compilation of custom model, adjusted to fashion minst dataset problem"""
    model = Net()
    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())

    """Train model with base time benchmark"""
    epochs = 3
    train_losses = []
    test_losses = []
    start = time.time()
    for epoch in range(epochs):
        epoch_train_loss = 0.0
        epoch_test_loss = 0.0
        for inputs, labels in train_loader:
            # przygotuj dane
            inputs = inputs.view(-1, 28 * 28)
            # wyzeruj gradienty
            optimizer.zero_grad()
            # policz predykcje modelu
            outputs = model(inputs)
            # policz funkcje błędu
            loss = loss_function(outputs, labels)
            # policz gradienty
            loss.backward()
            # zaktualizuj wagi modelu korzystając z optymalizatora
            optimizer.step()
            epoch_train_loss += loss.item()
        """Benchmark of accuracy, with dependency of epoch"""
        total = 0
        correct = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images = images.view(-1, 28 * 28)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)
                epoch_test_loss += loss.item()

        print(f"Epoch {epoch}, test loss", 100 * correct / total, "%")
        print("time: ", time.time() - start, "s")
        train_losses.append(epoch_train_loss / len(train_loader))
        test_losses.append(epoch_test_loss / len(test_loader))
    plt.plot(list(range(epochs)), train_losses)
    plt.plot(list(range(epochs)), test_losses)
    plt.title("Training and validation accuracy")
    plt.legend()
    plt.show()

    """Save the model"""
    #torch.save(model.state_dict(), "Models3")

def check():
    """Checking available GPU with CUDA for training and disabling it"""
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("Num GPUs Available: ", torch.cuda.device_count())
    else:
        device = torch.device("cpu")
def train_and_save_model():
    tf.keras.utils.disable_interactive_logging()

    """Checking available GPU with CUDA for training and disabling it"""
    tf.config.list_physical_devices("GPU")
    print("Num GPUs Available: ", len(tf.config.list_physical_devices("GPU")))
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    """ Prepare test and train datasets """
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    """Creation and compilation of custom model, adjusted to fashion minst dataset problem"""
    model = keras.Sequential(
        [
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(10, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    """Train model with base time benchmark"""
    start = time.time()
    history = model.fit(train_images, train_labels, epochs=10)
    print("time: ", time.time() - start, "s")

    """Benchmark of accuracy, with dependency of epoch"""
    plt.plot(list(range(10)), history.history["accuracy"], "bo", label="Training acc")
    plt.title("Training and validation accuracy")
    plt.legend()
    plt.show()

    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    print("\nTest accuracy:", test_acc)

    """Creation and compilation of custom, smaller model for comparison"""
    model_smaller = keras.Sequential(
        [
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(16, activation="relu"),
            keras.layers.Dense(10, activation="softmax"),
        ]
    )

    model_smaller.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    """Train model with base time benchmark"""
    start = time.time()
    history_smaller = model_smaller.fit(train_images, train_labels, epochs=10)
    print("time: ", time.time() - start, "s")

    """Benchmark of accuracy, with dependency of epoch"""
    plt.plot(
        list(range(10)), history_smaller.history["accuracy"], "bo", label="Training acc"
    )
    plt.title("Training and validation accuracy")
    plt.legend()
    plt.show()

    test_loss, test_acc = model_smaller.evaluate(test_images, test_labels, verbose=2)
    print("\nTest accuracy:", test_acc)

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

    class_names = [
        "T-shirt/top",
        "Trouser",
        "Pullover",
        "Dress",
        "Coat",
        "Sandal",
        "Shirt",
        "Sneaker",
        "Bag",
        "Ankle boot",
    ]
    print("Rozpoznana klasa:", class_names[np.argmax(result)])
    return class_names[np.argmax(result)]


if __name__ == '__main__':
    #train_and_save_model()
    train_and_save_model2()
    '''
    img = Image.open("Assets/Images/product-17997.jpg")
    img = ImageOps.exif_transpose(img)
    img = fimg.resize_img(img)
    cv2_img = fimg.pil_to_cv2(img)
    cv2_img = rmbg.cv2_remove_backgound(cv2_img)
    cv2.imshow("img", cv2_img)
    recognize_type(cv2_img)
    '''