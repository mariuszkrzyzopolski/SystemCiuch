import csv
import random
import torch
from sklearn.preprocessing import LabelEncoder


def findClothes(occasion, category):
    bottom_items = set()
    shoes_items = set()

    # znajdż wszystkie rzeczy do danej okazji
    occasion_items = set([tuple(row) for row in data[1:] if row[4] == occasion])

    # znajdź góry w danej okazji
    top_items = set([row for row in occasion_items if row[1] == "top"])
    # wylosuj jedną
    random_item = random.sample(list(top_items), 1)[0]
    # zapisz jej kolor
    color = random_item[3]

    # jeśli wybrano zestaw monochromatyczny
    match category:
        case "one_color":
            bottom_items = [
                row for row in occasion_items if row[3] == color and row[1] == "bottom"
            ]
            shoes_items = [
                row for row in occasion_items if row[3] == color and row[1] == "shoes"
            ]
        case "two_colors":
            # znajdź inne kolory w danej okazji
            other_colors = set([row[3] for row in occasion_items if row[3] != color])
            if len(other_colors) > 0:
                # wylosuj drugi kolor
                second_color = random.sample(list(other_colors), 1)[0]
            else:
                # jeśli nie ma inncyh kolorów w tej okazji, to użyj tylko tego pierwszego
                second_color = color
            # znajdź rzeczy w tych dwóch kolorach, które nie są górą
            bottom_items = [
                row
                for row in occasion_items
                if row[3] in (color, second_color) and row[1] == "bottom"
            ]
            shoes_items = [
                row
                for row in occasion_items
                if row[3] in (color, second_color) and row[1] == "shoes"
            ]
        case "random":
            bottom_items = [row for row in occasion_items if row[1] == "bottom"]
            shoes_items = [row for row in occasion_items if row[1] == "shoes"]

    return bottom_items, shoes_items


def chooseClothes(bottom_items, shoes_items):
    # Kodowanie kategoryczne dla kolumn 'category', 'type', 'color', 'occasion'
    le_category = LabelEncoder().fit(
        list(set([row[1] for row in bottom_items] + [row[1] for row in shoes_items]))
    )
    le_type = LabelEncoder().fit(
        list(set([row[2] for row in bottom_items] + [row[2] for row in shoes_items]))
    )
    le_color = LabelEncoder().fit(
        list(set([row[3] for row in bottom_items] + [row[3] for row in shoes_items]))
    )
    le_occasion = LabelEncoder().fit(
        list(set([row[4] for row in bottom_items] + [row[4] for row in shoes_items]))
    )

    # Konwersja wartości na typ float
    bottom_tensors = [
        torch.tensor(
            [
                le_category.transform([row[1]])[0],
                le_type.transform([row[2]])[0],
                le_color.transform([row[3]])[0],
                le_occasion.transform([row[4]])[0],
            ],
            dtype=torch.float,
        )
        for row in bottom_items
    ]

    shoes_tensors = [
        torch.tensor(
            [
                le_category.transform([row[1]])[0],
                le_type.transform([row[2]])[0],
                le_color.transform([row[3]])[0],
                le_occasion.transform([row[4]])[0],
            ],
            dtype=torch.float,
        )
        for row in shoes_items
    ]

    # Sieć neuronowa
    model = torch.nn.Sequential(
        torch.nn.Linear(4, 8),
        torch.nn.ReLU(),
        torch.nn.Linear(8, 4),
        torch.nn.ReLU(),
        torch.nn.Linear(4, 1),
        torch.nn.Sigmoid(),
    )

    # Uczenie modelu
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = torch.nn.MSELoss()
    for epoch in range(1000):
        for i in range(len(bottom_tensors)):
            optimizer.zero_grad()
            bottom_output = model(bottom_tensors[i])
            shoes_output = model(shoes_tensors[i])
            loss = criterion(bottom_output, shoes_output)
            loss.backward()
            optimizer.step()
    # Wybór elementów z bottom_items i shoes_items
    with torch.no_grad():
        bottom_choice = bottom_items[model(torch.stack(bottom_tensors)).argmax().item()]
        shoes_choice = shoes_items[model(torch.stack(shoes_tensors)).argmax().item()]
    return bottom_choice, shoes_choice


if __name__ == "__main__":
    with open("testdata/test.csv", "r") as file:
        reader = csv.reader(file)
        data = list(reader)
    bottom_items, shoes_items = findClothes("casual", "two_colors")
    print(bottom_items, shoes_items)
    bottom_choice, shoes_choice = chooseClothes(bottom_items, shoes_items)
    print(bottom_choice, shoes_choice)
