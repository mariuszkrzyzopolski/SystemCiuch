import time

import cv2
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28 * 28, 784)
        self.fc2 = nn.Linear(784, 256)
        self.fc3 = nn.Linear(256, 64)
        self.fc4 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = F.relu(x)
        x = self.fc4(x)
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


def train_and_save_model():
    """Prepare test and train datasets"""
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
    )
    train_set = datasets.FashionMNIST("./Assets/FashionMNIST", train=True, download=True, transform=transform)
    test_set = datasets.FashionMNIST("./Assets/FashionMNIST", train=False, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=32, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=32, shuffle=False)

    """Creation and compilation of custom model, adjusted to fashion minst dataset problem"""
    device = check_gpu()
    model = Net().to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())

    """Train model with base time benchmark"""
    epochs = 15
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
            images = images.view(-1, 28 * 28)
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
        accuracy.append(correct / total)
    plt.plot(list(range(epochs)), train_losses)
    plt.plot(list(range(epochs)), test_losses)
    plt.plot(list(range(epochs)), accuracy)
    plt.title("Training and validation accuracy")
    plt.legend(["train_losses", "test_losses", "accuracy"])
    plt.show()

    """Save the model"""
    torch.save(model.state_dict(), "recognition_type_torch_model.pth")


def recognize_type(img):
    # load model
    device = check_gpu()
    model = Net().to(device)
    model.load_state_dict(torch.load("recognition_type_torch_model.pth"))

    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    img = img / 255
    img_tensor = torch.Tensor(img).to(device)
    img_tensor = img_tensor.view(-1, 28 * 28)

    # make a prediction
    model.eval()
    with torch.no_grad():
        result = model(img_tensor)
    predicted_class = torch.argmax(result).item()

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

    return class_names[predicted_class]


"""
import Common.image_functions as fimg
from PIL import ImageOps
from PIL import Image
import PIL.Image

if __name__ == '__main__':
    train_and_save_model()
    img = Image.open("../Images/Assets/top/118073904.jpg")
    img = ImageOps.exif_transpose(img)
    cv2_img = fimg.pil_to_cv2(img)
    recognize_type(cv2_img)
"""
