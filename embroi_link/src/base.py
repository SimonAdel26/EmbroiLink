import cv2
import numpy as np


class Base:
    def __init__(self):
        pass

    def image_contour(self, cv_image):
        """function to process the image and find contours"""

        # Convert the image to grayscale +blur to reduce noise
        cv_image = cv_image.astype(np.uint8)
        cv_image_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        cv_image_gray = cv2.GaussianBlur(cv_image_gray, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(cv_image_gray, 50, 150)

        # Morphological operations to close gaps in edges
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=2)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # Find contours in the edge-detected image
        _, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Draw the contours on the new image
        cv_image_result = cv_image.copy()
        cv_image_result[edges != 0] = (0, 0, 0)

        # Show the new image with contours in the QGraphicsView
        return cv_image_result

    def image_Kmeans(self, cv_image, K):
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
