import extcolors
import pandas as pd
import matplotlib.pyplot as plt

from colormap import rgb2hex
from PIL import Image
from PIL import ImageColor

input_name = 'example.jpg'
output_width = 900                   #set the output size
img = Image.open(input_name)
wpercent = (output_width/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((output_width,hsize), Image.ANTIALIAS)

#save
resize_name = 'resize_' + input_name  #the resized image name
img.save(resize_name)                 #output location can be specified before resize_name

#read
plt.figure(figsize=(9, 9))
img_url = resize_name
img = plt.imread(img_url)
plt.imshow(img)
plt.axis('off')
# plt.show()

colors_x = extcolors.extract_from_path(img_url, tolerance = 12, limit = 12)
#print(colors_x)

def color_to_df(input):
    colors_pre_list = str(input).replace('([(', '').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]

    # convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                           int(i.split(", ")[1]),
                           int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

    df = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])
    return df


df_color = color_to_df(colors_x)
top_color = df_color.head(1)

# print(top_color)
top_hex = top_color.iloc[0]['c_code']
# print(top_hex)

top_color_rgb = ImageColor.getcolor(df_color.iloc[0]['c_code'], "RGB")
# print(top_color_rgb)


# list_color = list(df_color['c_code'])
# list_precent = [int(i) for i in list(df_color['occurence'])]
# text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(list_color,
#                                                                                list_precent)]
# fig, ax = plt.subplots(figsize=(90,90),dpi=10)
# wedges, text = ax.pie(list_precent,
#                       labels= text_c,
#                       labeldistance= 1.05,
#                       colors = list_color,
#                       textprops={'fontsize': 120, 'color':'black'}
#                      )
# plt.setp(wedges, width=0.3)

#plt.show()

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
        (115, 59, 36): "Brązowy"
    }

    r, g, b = code
    min_distance = float("inf")
    closest_color = None
    for color_value, color_name in color_map.items():
        distance = (color_value[0] - r) ** 2 + (color_value[1] - g) ** 2 + (color_value[2] - b) ** 2
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name

    return closest_color


print(rgb_to_color_name(top_color_rgb))





