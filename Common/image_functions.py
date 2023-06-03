from io import BytesIO

import cv2
import numpy as np
from fastapi import File, UploadFile
from PIL import Image, ImageOps


def resize_img(input_image):
    output_height = 512
    wpercent = output_height / float(input_image.size[0])
    output_width = int((float(input_image.size[1]) * float(wpercent)))
    ret = input_image.resize((output_height, output_width), Image.Resampling.BICUBIC)
    return ret


def resize_cv(img: np.ndarray):
    """
    Simple function to resize image to 512px width using openCV.
    :param img:
    :return:
    """
    output_width = 512
    wpercent = output_width / float(len(img))
    output_hight = int((float(len(img[1])) * float(wpercent)))
    return cv2.resize(img, (output_hight, output_width), interpolation=cv2.INTER_AREA)


def png_to_jpg(png_image):
    jpg_image = Image.new("RGB", png_image.size, (255, 255, 255))
    return jpg_image.paste(png_image, mask=png_image.split()[3])


def pil_to_cv2(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv2_image):
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2_image)
    return pil_img.convert("RGB")


def api_to_pil(updated_image: UploadFile = File(...)):
    pil_img = Image.open(BytesIO(updated_image.file.read()))
    pil_img = ImageOps.exif_transpose(pil_img)
    return pil_img


def api_to_cv2(updated_image: UploadFile = File(...)):
    cv2_img = Image.open(BytesIO(updated_image.file.read()))
    cv2_img = ImageOps.exif_transpose(cv2_img)
    cv2_img = cv2.cvtColor(np.array(cv2_img), cv2.COLOR_RGB2BGR)
    return cv2_img


def save_image(img: Image, path: str):
    img.save(path)
