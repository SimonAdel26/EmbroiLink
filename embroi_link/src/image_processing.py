import cv2
import numpy as np


class ImageProcessing:
    @staticmethod
    def image_Kmeans(cv_image, K):
        """function to apply K-means clustering to the image"""

        cv_image_reshaped = cv_image.reshape((-1, 3))
        cv_image_reshaped = np.float32(cv_image_reshaped)

        # Define criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)

        # Apply K-means clustering
        _, label, center = cv2.kmeans(
            data=cv_image_reshaped,
            K=K,
            bestLabels=None,
            criteria=criteria,
            attempts=10,
            flags=cv2.KMEANS_PP_CENTERS,  #  KMEANS_PP_CENTERS KMEANS_RANDOM_CENTERS
        )

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        cv_image_result = center[label.flatten()]
        cv_image_result = cv_image_result.reshape((cv_image.shape))

        # Return the new Image with K-means and list of colors
        colors = [color.tolist() for color in center]
        return cv_image_result, colors
