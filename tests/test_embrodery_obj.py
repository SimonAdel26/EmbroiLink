import json
from pathlib import Path

import cv2

from embroi_link.src.embrodery_obj import EmbroderyObj
from embroi_link.src.embrodery_obj import (
    PROJECT_DIR,
    IMAGES_DIR_PATH,
    HISTORY_FILE_PATH,
)

IMAGES_SOURCE_DIR_PATH = PROJECT_DIR / "images"


def test_constructor():
    obj = EmbroderyObj()

    assert obj.image_path is None
    assert obj.cv_image is None
    assert obj.cv_image_result is None
    assert len(obj.list_colors) == 0


def test_load_and_save_image():
    obj = EmbroderyObj()

    image_source = str(IMAGES_SOURCE_DIR_PATH / "poza.jpeg")
    obj.load_image(image_source, True)

    assert obj.image_path == IMAGES_DIR_PATH / Path(image_source).name
    assert obj.cv_image is not None
    assert obj.cv_image_result is None
    assert len(obj.list_colors) == 0

    with open(HISTORY_FILE_PATH, "r") as f:
        data = json.load(f)

    assert str(obj.image_path) in data.keys()

    # obj.save_image()
    # assert obj._get_generated_file() is None


def test_colors():
    obj = EmbroderyObj()

    list_colors = [[0, 0, 0], [20, 159, 78], [23, 56, 159]]

    obj.load_image(str(IMAGES_DIR_PATH / "poza.jpeg"), False)
    obj.colors(list_colors, True)

    assert obj.list_colors is not None

    with open(HISTORY_FILE_PATH, "r") as f:
        data = json.load(f)

    assert list_colors == data[str(obj.image_path)]["colors"]


def test_click_zone():
    obj = EmbroderyObj()
    obj.cv_image_result = cv2.imread(IMAGES_SOURCE_DIR_PATH / "poza.jpeg")

    x = 420
    y = 28

    select_image = obj.click_zone(x, y, None)
    assert select_image[y, x] is not obj.cv_image_result[y, x]
