import cv2
import numpy as np


def analyze_image(image: np.ndarray):
    """
    This function finds the layer and parameter needed to calculate the mask.
    :param image:
    :return:
    """
    myimage_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    h, l, s = cv2.split(myimage_hls)

    value_counts_h = analyze_layer(h)
    value_counts_l = analyze_layer(l)
    value_counts_s = analyze_layer(s)

    # background in hls
    background = find_bg_color(myimage_hls)

    # split point, binary or inv, score
    h_x, h_points = find_peaks(value_counts_h, "h", background)
    l_x, l_points = find_peaks(value_counts_l, "l", background)
    s_x, s_points = find_peaks(value_counts_s, "s", background)

    if h_points > l_points and h_points > s_points:
        layer = h
        cut_off_point = h_x
        method = find_method(h, h_x)
    elif l_points > h_points and l_points > s_points:
        layer = l
        cut_off_point = l_x
        method = find_method(l, l_x)
    else:
        layer = s
        cut_off_point = s_x
        method = find_method(s, s_x)

    return layer, cut_off_point, method


def find_method(layer: np.ndarray, cut_off_point: int):
    rights = []
    lefts = []
    height = len(layer)
    width = len(layer[0])
    for x in range(width):
        for y in range(height):
            distance = modified_euclidean_dist(x, y, width, height)
            if layer[y, x] > cut_off_point:
                rights.append(distance)
            else:
                lefts.append(distance)
    if np.average(lefts) > np.average(rights):
        return cv2.THRESH_BINARY
    else:
        return cv2.THRESH_BINARY_INV


def analyze_layer(layer: np.ndarray):
    """
    Returns a graph of the number of pixels for each value.
    :param layer:
    :return:
    """
    unique_values = np.unique(layer)
    sums = np.zeros(len(unique_values))
    value_counts = {i: 0 for i in range(256)}
    for i, value in enumerate(unique_values):
        mask = layer == value
        sums[i] = np.sum(mask)
        value_counts[value] = int(sums[i])

    # plt.plot(list(value_counts.keys())[:], list(value_counts.values())[:])
    # plt.tight_layout()
    # plt.show()
    return value_counts


def find_bg_color(myimage: np.ndarray):
    """
    Predict background color.
    :param myimage:
    :return:
    """
    result = [0, 0, 0]
    weigths = 0
    height = len(myimage)
    width = len(myimage[0])
    for x in range(width):
        for y in range(height):
            weight = modified_euclidean_dist(x, y, width, height)
            result = result + myimage[y, x] * weight
            weigths += weight
    result = result / weigths
    result = [int(result[0]), int(result[1]), int(result[2])]

    return result


def modified_euclidean_dist(x: int, y: int, width: int, height: int):
    """
    Support function - Euclidean distance.
    :param x:
    :param y:
    :param width:
    :param height:
    :return:
    """
    norm_x = abs(x / width - 1 / 2)
    norm_y = abs(y / height - 1 / 2)
    return np.sqrt(pow(norm_x, 2) + pow(norm_y, 2))


def find_peak(dictionary: dict, peak_center: int):
    """
    Find the peak center, range and number of pixels in peak.
    :param dictionary:
    :param peak_center:
    :return:
    """
    points = {i: 0 for i in range(256)}
    keys = {i: 0 for i in range(256)}
    start = 0
    stop = 0
    for r in range(1, len(dictionary)):
        if peak_center - r <= 0:
            peak_center = 0 + r
        elif peak_center + r >= 255:
            peak_center = 255 - r
        elif dictionary.get(peak_center + r) > dictionary.get(peak_center - r):
            peak_center += 1
        elif dictionary.get(peak_center + r) < dictionary.get(peak_center - r):
            peak_center -= 1
        start = peak_center - r
        stop = peak_center + r

        keys.update({r: peak_center})
        points.update(
            {r: sum(value for k, value in dictionary.items() if start <= k <= stop)}
        )
        if points.get(r) / (stop - start) > 3 * (points.get(r) - points.get(r - 1)):
            break
    pixel_counter = max(points.values())
    return start, peak_center, stop, pixel_counter


def find_peaks(dictionary: dict, dimension: str, background: list):
    """
    Predict two peaks in the chart.
    :param dictionary:
    :param dimension:
    :param background:
    :return:
    """
    if dimension == "h":
        bg_peak = background[0]
    elif dimension == "l":
        bg_peak = background[1]
    else:  # dimension == "s"
        bg_peak = background[2]

    # Find backgraung peak
    bg_start, bg_center, bg_stop, bg_pixel_counter = find_peak(dictionary, bg_peak)

    # Find foreground peak
    dictionary_without_background = {
        key: 0 if bg_start <= key <= bg_stop else dictionary[key] for key in dictionary
    }
    second_peak_center = get_key_from_value(
        dictionary_without_background, max(dictionary_without_background.values())
    )
    fg_start, fg_center, fg_stop, fg_pixel_counter = find_peak(
        dictionary_without_background, second_peak_center
    )

    # Predicting layer importance
    if bg_pixel_counter < fg_pixel_counter:
        power = bg_pixel_counter * (bg_stop - bg_start + fg_stop - fg_start)
    else:
        power = fg_pixel_counter * (bg_stop - bg_start + fg_stop - fg_start)

    # Finding best cut-off point
    if bg_center < fg_center:
        cut_off_point = int(abs((fg_start + bg_stop) / 2))
    else:
        cut_off_point = int(abs((fg_stop + bg_start) / 2))

    return cut_off_point, power


def get_key_from_value(d: dict, val: int):
    """
    Support function to find key in dict via value.
    :param d:
    :param val:
    :return:
    """
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None


def cv2_remove_backgound(img: np.ndarray):
    """
    Function to remove background using openCV and own heuristic.
    :param img:
    :return:
    """
    # Find mask
    layer, x, method = analyze_image(img)
    ret, thresh = cv2.threshold(layer, x, 255, method)
    thresh = cv2.medianBlur(thresh, 11)
    # cv2.imshow("mask", thresh)
    # Remove background
    result = cv2.bitwise_and(img, img, mask=thresh)
    result[np.where((result == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
    return result


'''
if __name__ == '__main__':
    """
    Simple test to check how work remove_backgound()
    """
    # Read & resize image
    img = cv2.imread('Assets/1/20230209_191911.jpg')
    img = fimg.resize_cv(img)
    img_without_bg = cv2_remove_backgound(img)
    cv2.imshow("img", img)
    cv2.imshow("img_without_background", img_without_bg)

    # De-allocate any associated memory usage
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()

        img = cv2.imread('Assets/1/20230209_192338.jpg')
        img = fimg.resize_cv(img)
        img_without_bg = cv2_remove_backgound(img)
        cv2.imshow("img", img)
        cv2.imshow("img_without_background", img_without_bg)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        img = cv2.imread('Assets/1/20230209_192954.jpg')
        img = fimg.resize_cv(img)
        img_without_bg = cv2_remove_backgound(img)
        cv2.imshow("img", img)
        cv2.imshow("img_without_background", img_without_bg)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()

        img = cv2.imread('Assets/1/20230209_191819.jpg')
        img = fimg.resize_cv(img)
        img_without_bg = cv2_remove_backgound(img)
        cv2.imshow("img", img)
        cv2.imshow("img_without_background", img_without_bg)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
'''
