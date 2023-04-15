import extcolors
import pandas as pd


def color_to_df(image):
    colors, pixel_count = extcolors.extract_from_image(image, tolerance=12, limit=12)
    df_colors = []
    df_occurrence = []
    for color in colors:
        df_colors.append(list(color[0]))
        df_occurrence.append(color[1])
    df = pd.DataFrame(zip(df_colors, df_occurrence), columns=["rgb", "occurrence"])
    return df


def rgb_to_color_name(code):
    color_map = {
        (255, 255, 255): "Biały",
        (0, 0, 0): "Czarny",
        (255, 0, 0): "Czerwony",
        (0, 255, 0): "Zielony",
        (0, 0, 255): "Niebieski",
        (255, 255, 0): "Żółty",
        (0, 255, 255): "Turkusowy",
        (255, 0, 255): "Fioletowy",
        (192, 192, 192): "Srebrny",
        (128, 128, 128): "Szary",
        (128, 0, 0): "Bordowy",
        (128, 128, 0): "Oliwkowy",
        (0, 128, 0): "Zielony",
        (128, 0, 128): "Purpurowy",
        (0, 128, 128): "Błękitny",
        (245, 245, 220): "Ecru",
        (115, 59, 36): "Brązowy",
        (255, 215, 0): "Złoty"
    }

    r, g, b = code
    min_distance = float("inf")
    closest_color = None
    for color_value, color_name in color_map.items():
        distance = (
            (color_value[0] - r) ** 2
            + (color_value[1] - g) ** 2
            + (color_value[2] - b) ** 2
        )
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name

    return closest_color


"""
if __name__ == '__main__':
    input_name = 'example.jpg'
    input_name = "Assets/1/20230209_183057.jpg"

    img = cv2.imread(input_name)
    img = fimg.resize_cv(img)
    img = rmbg.cv2_remove_backgound(img)
    pil_img = fimg.cv2_to_pil(img)
    df_color = color_to_df(pil_img)

    if tuple(df_color['rgb'].iloc[0]) != (255, 255, 255):
        top_color_rgb = df_color.iloc[0]['rgb']
    else:
        top_color_rgb = df_color.iloc[1]['rgb']

    print(top_color_rgb, rgb_to_color_name(top_color_rgb))
"""
