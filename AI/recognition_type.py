import os
import random
import time

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from matplotlib import pyplot as plt


def load_data(dest_path, img_size=(64, 64)):
    classes = os.listdir(dest_path)
    x, y = [], []
    for class_name in classes:
        class_path = os.path.join(dest_path, class_name)
        filepaths = []
        for root, dirs, files in os.walk(class_path):
            for file in files:
                filepath = os.path.join(root, file)
                filepaths.append(filepath)
        random.shuffle(filepaths)
        for i, filepath in enumerate(filepaths):
            img = cv2.imread(filepath)
            img = cv2.resize(img, img_size)
            img = img.transpose(2, 0, 1)
            img = img / 255
            label = np.zeros(len(classes))
            label[classes.index(class_name)] = 1
            x.append(img)
            y.append(label)
            if i >= 1000:
                break
    x = np.array(x)
    y = np.array(y)
    return x, y, classes


class Net(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 3, kernel_size=3, stride=1)  # 3x62x62
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)  # 3x31x31
        self.conv2 = nn.Conv2d(3, 1, kernel_size=3, stride=1)  # 1x28x28
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)  # 1x28x28
        self.fc1 = nn.Linear(196, num_classes)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = F.relu(self.conv2(x))
        x = self.pool2(x)
        x = x.view(-1, 196)
        x = self.fc1(x)
        if not self.training:
            x = F.softmax(x, dim=1)
        return x


def check_gpu():
    """Checking available GPU with CUDA for training and disabling it"""
    if torch.cuda.is_available():
        # print("Num GPUs Available: ", torch.cuda.device_count())
        return torch.device("cuda")
    else:
        return torch.device("cpu")


def train_and_save_model(
    x_train, y_train, x_test, y_test, num_epochs=10, batch_size=32, learning_rate=0.0007
):
    train_loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(torch.Tensor(x_train), torch.Tensor(y_train)),
        batch_size=batch_size,
        shuffle=True,
    )
    test_loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(torch.Tensor(x_test), torch.Tensor(y_test)),
        batch_size=batch_size,
        shuffle=False,
    )

    """Creation and compilation of custom model, adjusted to fashion minst dataset problem"""
    device = check_gpu()
    model = Net(np.shape(y_train)[-1]).to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    """Train model with base time benchmark"""
    epochs = 500
    train_losses = []
    test_losses = []
    accuracy = []
    start = time.time()
    for epoch in range(epochs):
        epoch_train_loss = 0.0
        epoch_test_loss = 0.0
        total = 0.0
        correct = 0.0
        for images, labels in train_loader:
            # prepare data
            images, labels = images.to(device), labels.to(device)
            images = images.view(-1, 3, 64, 64)
            # reset gradients
            optimizer.zero_grad()
            # compute model predictions
            outputs = model(images)
            # compute loss function
            loss = loss_function(outputs, labels)
            # compute gradients
            loss.backward()
            # update model weights using optimizer
            optimizer.step()
            epoch_train_loss += loss.item()

        """Benchmark of accuracy, with dependency of epoch"""
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                images = images.view(-1, 3, 64, 64)
                outputs = model(images)
                loss = loss_function(outputs, labels)
                _, predicted = torch.max(outputs.data, 1)
                correct += (predicted == torch.argmax(labels, dim=1)).sum().item()
                total += labels.size(0)
                epoch_test_loss += loss.item()

        print(f"Epoch {epoch}, test loss", 100 * correct / total, "%")
        print("time: ", time.time() - start, "s")
        train_losses.append(epoch_train_loss / len(train_loader))
        test_losses.append(epoch_test_loss / len(test_loader))
        accuracy.append(correct / total)
    plt.plot(list(range(epochs)), train_losses)
    plt.plot(list(range(epochs)), test_losses)
    plt.plot(list(range(epochs)), accuracy)
    plt.title("Training and validation accuracy")
    plt.legend(["train_losses", "test_losses", "accuracy"])
    plt.show()

    """Save the model"""
    torch.save(model.state_dict(), "recognition_type_torch_model.pth")


def recognize_type(img, class_names):
    # load model
    device = check_gpu()
    model = Net(len(class_names)).to(device)
    model.load_state_dict(torch.load("recognition_type_torch_model.pth"))

    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_AREA)
    img = img / 255
    img_tensor = torch.Tensor(img).to(device)
    img_tensor = img_tensor.view(-1, 3, 64, 64)

    # make a prediction
    model.eval()
    with torch.no_grad():
        result = model(img_tensor)
    predicted_class = torch.argmax(result).item()

    return class_names[predicted_class]


"""
import Common.image_functions as fimg
from PIL import ImageOps
from PIL import Image
import PIL.Image
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    class_names = ['skirt', 'outwear', 'top', 'jumpsuit', 'pants', 'dress', 'shoes']
    dest_path = "../Images/Assets"
    images, labels, class_names = load_data(dest_path)
    x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)
    #train_and_save_model(x_train, y_train, x_test, y_test)

    img = Image.open("../Images/Assets/shoes/24351901.jpg")
    img = ImageOps.exif_transpose(img)
    cv2_img = fimg.pil_to_cv2(img)
    print(recognize_type(cv2_img, class_names))
"""
