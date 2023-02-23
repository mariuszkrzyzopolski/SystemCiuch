import cv2
import numpy as np
import matplotlib.pyplot as plt


def analyze_image(image: np.ndarray):
    myimage_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    h, l, s = cv2.split(myimage_hls)

    value_counts_h = analyze_layer(h)
    value_counts_l = analyze_layer(l)
    value_counts_s = analyze_layer(s)

    background = find_bg_color(image)

    lower_limit = np.array([0, 0, 0])
    upper_limit = np.array([255, 255, 255])

    h_a, h_b, h_high = find_peak(value_counts_h, "h", background)
    l_a, l_b, l_high = find_peak(value_counts_l, "l", background)
    s_a, s_b, s_high = find_peak(value_counts_s, "s", background)

    if h_high > l_high and h_high > s_high:
        lower_limit[0] = h_a
        upper_limit[0] = h_b
    elif l_high > h_high and l_high > s_high:
        lower_limit[1] = l_a
        upper_limit[1] = l_b
    elif s_high > h_high and s_high > l_high:
        lower_limit[2] = s_a
        upper_limit[2] = s_b

    print("h l s", lower_limit, upper_limit)

    return lower_limit, upper_limit


def analyze_layer(layer):
    unique_values = np.unique(layer)
    sums = np.zeros(len(unique_values))
    value_counts = {i: 0 for i in range(256)}
    for i, value in enumerate(unique_values):
        mask = (layer == value)
        sums[i] = np.sum(mask)
        value_counts[value] = int(sums[i])

    plt.plot(list(value_counts.keys())[1:-1], list(value_counts.values())[1:-1])
    plt.tight_layout()
    plt.show()
    return value_counts


def find_bg_color(myimage):
    myimage = cv2.cvtColor(myimage, cv2.COLOR_BGR2HLS)
    midium = [0, 0, 0]
    weigths = 0
    for y in range(len(myimage)):
        for x in range(len(myimage[y])):
            weigth = euclidean_dist(x, y, len(myimage) / 2, len(myimage[y]) / 2)
            midium = midium + myimage[y, x] * weigth
            weigths += weigth
    result = midium / weigths
    result = [int(result[0]), int(result[1]), int(result[2])]
    return result


def euclidean_dist(ax, ay, bx, by):
    return -np.sqrt(pow((ax - bx), 2) + pow((ay - by), 2))


def find_peak(dictionary: dict, dimension: str, background: list):
    if dimension == "h":
        peak_center = background[0]
    elif dimension == "l":
        peak_center = background[1]
    else:  # dimension == "s"
        peak_center = background[2]

    points = {i: -1 for i in range(-1, 256)}
    keys = {i: -1 for i in range(-1, 256)}
    for r in range(len(dictionary)):
        if peak_center - r < 0:
            peak_center = 0 + r
        elif peak_center + r > 255:
            peak_center = 255 - r
        elif dictionary.get(peak_center + r) > dictionary.get(peak_center - r):
            peak_center += 1
        elif dictionary.get(peak_center + r) < dictionary.get(peak_center - r):
            peak_center -= 1

        points.update({r: score(dictionary, peak_center, r)})
        keys.update({r: peak_center})
        if points.get(r - 1) * 1.001 > points.get(r):
            break
    max_score = max(points.values())
    r = get_key_from_value(points, max_score)
    peak_center = keys.get(r)

    peak_key_in_range = 0
    peak_key_not_in_range = 0

    for key in dictionary:
        if peak_center - r < key < peak_center + r:
            if peak_key_in_range is None or dictionary[key] > dictionary[peak_key_in_range]:
                peak_key_in_range = key
        else:
            if peak_key_not_in_range is None or dictionary[key] > dictionary[peak_key_not_in_range]:
                peak_key_not_in_range = key
    print(peak_center, r)
    print(peak_key_in_range, peak_key_not_in_range)
    if dictionary[peak_key_in_range] > dictionary[peak_key_not_in_range]:
        power = abs(peak_key_not_in_range - peak_key_in_range) / dictionary[peak_key_in_range] * dictionary[
            peak_key_not_in_range]
    else:
        power = abs(peak_key_not_in_range - peak_key_in_range) * dictionary[peak_key_in_range] / dictionary[
            peak_key_not_in_range]

    return peak_center - r, peak_center + r, power


def score(d, key, r):
    return sum(value for k, value in d.items() if abs(key - k) <= r)

def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None


def remove_bacground(myimage, lower_limit: np.array, upper_limit: np.array):
    hsv_frame = cv2.cvtColor(myimage, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(hsv_frame, lower_limit, upper_limit)
    mask = cv2.bitwise_not(mask)
    cv2.imshow("mask", mask)

    result = cv2.bitwise_and(myimage, myimage, mask=mask)
    result[np.where((result == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
    return result


if __name__ == '__main__':
    img = cv2.imread("Assets/1/20230209_191911.jpg", cv2.IMREAD_COLOR)
    img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
    cv2.imshow("img orginal", img)

    lower_limit, upper_limit = analyze_image(img)
    img_without_background = remove_bacground(img, lower_limit, upper_limit)
    cv2.imshow("img_without_background", img_without_background)
    lower_limit, upper_limit = analyze_image(img_without_background)

    while True:
        if cv2.waitKey(1) == 27:
            print(" ")
            break

    cv2.destroyAllWindows()
