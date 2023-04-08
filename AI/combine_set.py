import csv
import random

with open("testdata/test.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)


def findClothes(occasion, category):
    # znajdż wszystkie rzeczy do danej okazji
    occasion_items = set([row for row in data[1:] if row[4] == occasion])

    # znajdź góry w danej okazji
    top_items = set([row for row in occasion_items if row[1] == "top"])
    # wylosuj jedną
    random_item = random.sample(top_items, 1)[0]
    # zapisz jej kolor
    color = random_item[3]

    # jeśli wybrano zestaw monochromatyczny
    if category == "one_color":
        # znajdź rzeczy, które mają tą samą okazję, ten sam kolor i nie są górą
        color_item = set(
            [row for row in occasion_items if row[3] == color and row[1] != "top"]
        )
    # jeśli wybrano zestaw z dwoma kolorami
    if category == "two_colors":
        # znajdź inne kolory w danej okazji
        other_colors = set([row[3] for row in occasion_items if row[3] != color])
        # wylosuj drugi kolor
        second_color = random.sample(other_colors, 1)[0]
        # znajdź rzeczy w tych dwóch kolorach, które nie są górą
        color_item = set(
            [
                row
                for row in occasion_items
                if row[3] == (color or second_color) and row[1] != "top"
            ]
        )
    # jeśli wybrano random rzeczy
    if category == "random":
        # znajdź rzeczy, które nie są górą
        color_item = set([row for row in occasion_items if row[1] != "top"])
    return color_item
