import cv2

from embroi_link.src.image_processing import ImageProcessing
from embroi_link.src.embrodery_obj import PROJECT_DIR

IMAGES_SOURCE_DIR_PATH = PROJECT_DIR / "images"


def test_image_Kmeans():
    imageprocessing = ImageProcessing()
    cv_image = cv2.imread(str(IMAGES_SOURCE_DIR_PATH / "poza.jpeg"))
    K = 10

    cv_image, colors = imageprocessing.image_Kmeans(cv_image, K)

    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    pixels = cv_image.reshape(-1, 3)
    list_colors = set(map(tuple, pixels))

    assert len(list_colors) == len(colors) == K
