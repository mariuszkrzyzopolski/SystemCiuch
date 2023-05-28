import random

import torch
from sklearn.preprocessing import LabelEncoder


def findClothes(category, data):
    bottom_items = set()
    shoes_items = set()

    # znajdź góry
    top_items = set([tuple(row) for row in data[1:] if "Upper garment" in row])
    # wylosuj jedną
    top_choice = random.sample(list(top_items), 1)[0]
    # zapisz jej kolor
    color = top_choice[data[0].index("color")]

    # jeśli wybrano zestaw monochromatyczny
    match category:
        case "one_color":
            bottom_items = [
                row
                for row in data[1:]
                if row[data[0].index("color")] == color and "Lower garment" in row
            ]
            shoes_items = [
                row
                for row in data[1:]
                if row[data[0].index("color")] == color and "Footwear" in row
            ]
        case "two_colors":
            # znajdź inne kolory w danej okazji
            other_colors = set(
                [row[3] for row in data[1:] if row[data[0].index("color")] != color]
            )
            if len(other_colors) > 0:
                # wylosuj drugi kolor
                second_color = random.sample(list(other_colors), 1)[0]
            else:
                raise ValueError(
                    "Mam problem z odnalezieniem drugiego koloru, "
                    "dodaj więcej rzeczy w innnych kolorach lub spróbuj ponownie"
                )

            # znajdź rzeczy w tych dwóch kolorach, które nie są górą
            bottom_items = [
                row
                for row in data[1:]
                if row[data[0].index("color")] in (color, second_color)
                and row[1] == "Lower garment"
            ]
            shoes_items = [
                row
                for row in data[1:]
                if row[data[0].index("color")] in (color, second_color)
                and row[1] == "Footwear"
            ]
        case "random":
            bottom_items = [row for row in data[1:] if "Lower garment" in row]
            shoes_items = [row for row in data[1:] if "Footwear" in row]

    if len(bottom_items) == 0:
        raise ValueError(
            "Brak dołów, z których można wybierać. Dodaj więcej i spróbuj ponownie."
        )
    if len(shoes_items) == 0:
        raise ValueError(
            "Brak butów, z których można wybierać. Dodaj więcej i spróbuj ponownie."
        )

    return bottom_items, shoes_items, top_choice


def chooseClothes(bottom_items, shoes_items, color_index, type_index, category_index):
    # Kodowanie kategoryczne dla kolumn 'category', 'type', 'color'
    le_category = LabelEncoder().fit(
        list(
            set(
                [row[category_index] for row in bottom_items]
                + [row[category_index] for row in shoes_items]
            )
        )
    )
    le_type = LabelEncoder().fit(
        list(
            set(
                [row[type_index] for row in bottom_items]
                + [row[type_index] for row in shoes_items]
            )
        )
    )
    le_color = LabelEncoder().fit(
        list(
            set(
                [row[color_index] for row in bottom_items]
                + [row[color_index] for row in shoes_items]
            )
        )
    )

    # Konwersja wartości na typ float
    bottom_tensors = [
        torch.tensor(
            [
                le_category.transform([row[category_index]])[0],
                le_type.transform([row[type_index]])[0],
                le_color.transform([row[color_index]])[0],
            ],
            dtype=torch.float,
        )
        for row in bottom_items
    ]

    shoes_tensors = [
        torch.tensor(
            [
                le_category.transform([row[category_index]])[0],
                le_type.transform([row[type_index]])[0],
                le_color.transform([row[color_index]])[0],
            ],
            dtype=torch.float,
        )
        for row in shoes_items
    ]

    # Sieć neuronowa
    model = torch.nn.Sequential(
        torch.nn.Linear(3, 8),
        torch.nn.ReLU(),
        torch.nn.Linear(8, 3),
        torch.nn.ReLU(),
        torch.nn.Linear(3, 1),
        torch.nn.Sigmoid(),
    )

    # Uczenie modelu
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_funcion = torch.nn.MSELoss()
    for epoch in range(1000):
        tensor_len = (
            len(shoes_tensors)
            if len(shoes_tensors) < len(bottom_tensors)
            else len(bottom_tensors)
        )
        for i in range(tensor_len):
            optimizer.zero_grad()
            bottom_output = model(bottom_tensors[i])
            shoes_output = model(shoes_tensors[i])
            loss = loss_funcion(bottom_output, shoes_output)
            loss.backward()
            optimizer.step()
    # Wybór elementów z bottom_items i shoes_items
    with torch.no_grad():
        bottom_choice = bottom_items[model(torch.stack(bottom_tensors)).argmax().item()]
        shoes_choice = shoes_items[model(torch.stack(shoes_tensors)).argmax().item()]
    return bottom_choice, shoes_choice


# if __name__ == "__main__":
#     with open("testdata/test.csv", "r") as file:
#         reader = csv.reader(file)
#         data = list(reader)
#     bottom_items, shoes_items, top_choice = findClothes("one_color", data)
#     print(bottom_items)
#     print(shoes_items)
#     print(top_choice)
#     bottom_choice, shoes_choice = chooseClothes(bottom_items, shoes_items)
#     print(bottom_choice, shoes_choice)
